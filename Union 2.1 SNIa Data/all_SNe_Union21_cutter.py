"""Picks out suitable 'uncut' Supernovae from the Union2.1 dataset \
'SCPUnion2.1_AllSNe_table.tex' and puts their: SN Name, Redshift, \
Effective Magnitude, Magnitude Error and the Original Dataset, into a new file \
called 'All SNe Union2.1.txt'. Data is from: http://supernova.lbl.gov/Union/, \
under: 'Cosmology Tables' > 'Full Table of All SNe'.
"""

folder = '/media/alex/Shared/University/Physics/Year 3/Physics Problem Solving/Computing Project/Programming/Milestone-Program-Supernova/Union 2.1 SNIa Data/'
with open(folder+"../SuperNova Data.txt", 'r') as f:
    data = f.readlines()
old_data, old_SNe_names, counter = [], {}, 0
for line in data:
    if (line[0] != '#') and (line.strip('\n') != ''):
        line = line[:-1].split(' ')
        old_data.append(line)
        old_SNe_names[line[0].upper()] = counter
        counter += 1
with open(folder+"SCPUnion2.1_AllSNe_table.tex", 'r') as f:
    data = f.readlines()


all_Union_uncut = []
for line in data:
    line = line[:-3].split(' & ')
    if line[-1] == '\\nodata':
        name, rdshft = line[:2]
        eff_mag, err_mag = line[2][:-1].split('(')
        all_Union_uncut.append([name, rdshft, eff_mag, err_mag, '----'])
        if name.upper() in old_SNe_names:
            del old_SNe_names[name.upper()]
for SN, n in old_SNe_names.items():
    line = old_data[n]
    line.append('----')
    all_Union_uncut.append(line)


with open(folder+'All SNe Union2.1.txt', 'w') as f:
    f.write('#SN_name , Redshift , eff_mag , err_mag , dataset\n')
    for name, rdshft, eff_mag, err_mag, dataset in all_Union_uncut:
        f.write('{0} , {1} , {2} , {3} , {4}\n'.format(name, rdshft, eff_mag,
                                                       err_mag, dataset))
