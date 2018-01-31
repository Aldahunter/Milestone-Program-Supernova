"""Picks out all Supernovae from Union2.1 dataset ('All SNe Union2.1.txt') and \
'tags' their: Discoverer(s) from a file of all SNe Ia discovered called \
'All SNe Ia.txt'. Data is from: \
http://www.cbat.eps.harvard.edu/lists/Supernovae.html and \
http://supernova.lbl.gov/Union/, (under: 'Cosmology Tables' > 'Full Table of \
All SNe')."""

with open("All SNe Union2.1.txt", 'r') as f:
    data = f.readlines()
    Preamble, Un_data = data[0], data[1:]
with open("All SNe Ia.txt", 'r') as f:
    all_data = f.readlines()[1:]


SNe_discoverers = {}
for line in all_data:
    line = line.split(' , ')
    SNe_discoverers[line[0]] = line[-1][:-1]
for n, line in enumerate(Un_data):
    line = line[:-1].split(' , ')
    try:
        line[-1] = SNe_discoverers[line[0]]
    except KeyError:
        try:
            line[-1] = SNe_discoverers[line[0].upper()]
        except KeyError:
            line[-1] = '----'
    line = ' , '.join(line) + '\n'
    Un_data[n]=line


with open('All SNe Union2.1.txt', 'w') as f:
    f.write(Preamble)
    for line in Un_data:
        f.write(line)
