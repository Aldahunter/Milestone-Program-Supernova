import dill as pickle
all_graphing_data = pickle.load(open("graphing_data.p", "rb"))  # Load in data for graphing.
for varaible, var_data in all_graphing_data.items():  # Turn each part of dictionary into an actual varaible with same name as the key.
    exec(varaible + ' = var_data')

outlier_SNe = []
def is_valid(s, selection_lim = False):
    if s.upper() == 'Q':
        return False
    else:
        try:
            float(s)
            if selection_lim == True:
                if (float(s) > 10) or (float(s) < 0):
                    return True
        except ValueError:
            return True
        return False


print("Enter 'Q' anytime to quit.")
while True:
    z, mag = '', ''
    while is_valid(z):
        z = input('Redshift, z: ')
    if z.upper() == 'Q': break
    while is_valid(mag):
        mag = input('Effective Mag: ')
    if mag.upper() == 'Q': break
    z = float(z)
    mag = float(mag)

    best_SNe = {}
    for SN in all_arr:
        dist = ((SN['z']-z)/z)**2 + ((SN['eff_m']-mag)/mag)**2
        if len(best_SNe) < 10:
            best_SNe[dist] = (SN['name'], SN['z'], SN['eff_m'])
        else:
            if dist < max(best_SNe):
                best_SNe.pop(max(best_SNe), None)
                best_SNe[dist] = (SN['name'], SN['z'], SN['eff_m'])

    best_matches = sorted([SN for SN in best_SNe])
    for n, SN_dist in enumerate(best_matches):
        name, rs, eff_m = best_SNe[SN_dist]
        print(str(n+1)+'. ', name, '\t\t(',rs,',',eff_m,')')

    user_choice = ''
    while is_valid(user_choice, True):
        user_choice = input('Please select the SN to save (1-10): ')
    if user_choice.upper() == 'Q': break
    n = int(user_choice) - 1
    outlier_SNe.append(best_SNe[best_matches[n]][0])
    print('Choice ' + user_choice + ' was added.')
    print()



print('\nLoop Exited')
print('Outliers were:')
print(outlier_SNe)
