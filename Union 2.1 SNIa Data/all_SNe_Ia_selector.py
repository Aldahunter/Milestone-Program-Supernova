"""Picks out all type 'Ia' Supernovae from 'All SNe 1953-2015.txt' and puts \
their: Name, Type, Right Ascension, Declination, Effective Magnitude and \
Discoverer(s), into a new file called 'All SNe Ia.txt'. Data is from: \
http://www.cbat.eps.harvard.edu/lists/Supernovae.html."""

with open("All SNe 1953-2015.txt", 'r') as f:
    data = f.readlines()[1:]

SNe_Ia = []
for line in data:
    if len(line) > 5:
        if line[130:132] in ['Ia', '  ']:
            name, SNtype = line[0:6].strip(), line[130:134].strip()
            coords, mag, discoverer = line[87:110], line[64:68], line[144:-1]
            if coords == ' '*23:
                 ra, decl =  'N/A', 'N/A'
            else:
                ra = coords[:11].replace(' ', ':')
                decl = coords[12:].replace(' ', ':')
            if SNtype == '':
                SNtype = 'Ia?'
            SNe_Ia.append([name, SNtype, ra, decl, mag, discoverer])

with open('All SNe Ia.txt', 'w') as f:
    f.write('#SN_name , SN_type , R.A. , Decl. , Eff_Mag , Discoverer(s)\n')
    for name, SNtype, ra, decl, mag, discoverer in SNe_Ia:
        f.write('{0} , {1} , {2} , {3} , {4} , {5}\n'.format(name, SNtype, ra,
                                                             decl, mag,
                                                             discoverer))
