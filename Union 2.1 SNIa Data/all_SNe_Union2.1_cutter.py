"""Picks out suitable 'uncut' Supernovae from the Union2.1 dataset \
'SCPUnion2.1_AllSNe_table.tex' and puts their: SN Name, Redshift, \
Effective Magnitude, Magnitude Error and the Original Dataset, into a new file \
called 'All SNe Union2.1.txt'. Data is from: http://supernova.lbl.gov/Union/, \
under: 'Cosmology Tables' > 'Full Table of All SNe'.
"""

with open("SCPUnion2.1_AllSNe_table.tex", 'r') as f:
    data = f.readlines()

all_Union_uncut = []
for line in data:
    split_line = line[:-4].split(' & ')
    if split_line[-1] == '\\nodata':
        name, rdshft = split_line[:2]
        eff_mag, err_mag = split_line[2][:-1].split('(')
        all_Union_uncut.append([name, rdshft, eff_mag, err_mag, '----'])

with open('All SNe Union2.1.txt', 'w') as f:
    f.write('#SN_name , Redshift , eff_mag , err_mag , dataset\n')
    for name, rdshft, eff_mag, err_mag, dataset in all_Union_uncut:
        f.write('{0} , {1} , {2} , {3} , {4}\n'.format(name, rdshft, eff_mag,
                                                       err_mag, dataset))
