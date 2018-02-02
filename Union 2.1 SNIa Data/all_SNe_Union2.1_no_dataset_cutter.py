"""Picks out all Supernovae from Union2.1 dataset ('All SNe Union2.1.txt') with \
no Discoverer and orders them by naming style, then puts them into a new file \
called 'All SNe Union2 No Dataset.txt'. Data is from: \
http://supernova.lbl.gov/Union/, (under: 'Cosmology Tables' > 'Full Table of \
All SNe')."""

with open("All SNe Union2.1.txt", 'r') as f:
    data = f.readlines()
    Preamble, Un_data = data[0], data[1:]

SNe_no_discoverers = []
for line in Un_data:
    line = line.strip('\n').split(' , ')
    if line[-1] == '----':
        SNe_no_discoverers.append(line[0])
SNe_no_discoverers = sorted(SNe_no_discoverers)

with open('All SNe Union2 No Dataset.txt', 'w') as f:
    f.write("#SN_name , dataset\n")
    for SN in SNe_no_discoverers:
        f.write("{0} , ----\n".format(SN))
