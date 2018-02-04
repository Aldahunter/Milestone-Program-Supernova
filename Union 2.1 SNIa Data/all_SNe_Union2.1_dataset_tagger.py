"""Picks out all Supernovae from Union2.1 dataset ('All SNe Union2.1.txt') and \
'tags' their: Discoverer(s) from a file of all SNe Ia discovered, called \
'All SNe Ia.txt'. If a Supernova is not in this text file, it is then \
compared to the internal names of Supernova from the following datasets: SNLS \
('All SNe SNLS.txt'), HST Riess ('All SNe HST Riess.txt'), SDSS II ('All SNe \
SDSS-II.txt') and Essence ('All SNe Essence.txt') 'tagging' these datasets if \
found within them.

Data is from:
http://supernova.lbl.gov/Union/ (Union2.1, under: 'Cosmology Tables' > 'Full \
Table of All SNe'),
http://www.cbat.eps.harvard.edu/lists/Supernovae.html (All discovered SNe 1953-\
2015),
https://arxiv.org/pdf/astro-ph/0510447.pdf (SNLS, Table 9: 'SNLS Type Ia \
supernovae'),
https://arxiv.org/pdf/astro-ph/0611572.pdf (HST Riess et al., Table 1: 'SN \
Discovery Data'),
https://arxiv.org/pdf/0802.3220.pdf (SDSS II, Table 2: 'SDSS-II SN \
Spectroscopic Follow-up Observations'),
https://arxiv.org/pdf/1603.03823.pdf (ESSENCE, Table 6: Transient Objects \
Considered for Follow-up Observations by the ESSENCE Survey),
https://arxiv.org/pdf/astro-ph/9609062.pdf (Table 1: Colors and Magnitudes of \
the Calan/Tololo Supernovae Ia).
"""

#Load Union2.1 dataset.
with open("All SNe Union2.1.txt", 'r') as f:
    data = f.readlines()
Preamble, Un_data = data[0], data[1:]


# Load other Datasets SN names and put in list.
with open("All SNe Ia.txt", 'r') as f:
    all_data = f.readlines()[1:]
free_dataset_dict, forced_dataset_dict = {}, {}
with open("All SNe SNLS.txt", 'r') as f:
    data = f.readlines()
SNLS_data = []
for line in data[1:]:
    SNLS_data.append(line[:-1].split(' ')[0].split('-')[1])
free_dataset_dict['SNLS'] = SNLS_data
with open("All SNe HST Riess.txt", 'r') as f:
    data = f.readlines()
HSTRiess_data = []
for line in data[1:]:
    HSTRiess_data.append(line[:-1].split(' ')[0].strip('HST'))
free_dataset_dict['HST Riess et al.'] = HSTRiess_data
with open("All SNe SDSS-II.txt", 'r') as f:
    data = f.readlines()
SDSSII_data = []
for line in data[1:]:
    SDSSII_data.append(line[:-1].split(' ')[1])
free_dataset_dict['SDSS II'] = SDSSII_data
with open("All SNe Essence.txt", 'r') as f:
    data = f.readlines()
Ess_data = []
for line in data[1:]:
    Ess_data.append(line[:-1].split(' ')[0])
free_dataset_dict['Essence'] = Ess_data
with open("All SNe HST CSS.txt", 'r') as f:
    data = f.readlines()
CSS_data = []
for line in data[1:]:
    CSS_data.append(line[:-1].split(' ')[0])
free_dataset_dict['HST CSS'] = CSS_data
with open("All SNe CalanTololo.txt", 'r') as f:
    data = f.readlines()
CTSS_data = []
for line in data[1:]:
    CTSS_data.append('19' + line[:-1].split(' ')[0])
forced_dataset_dict['C/TSS'] = CTSS_data

# Tag SNe with Discoverer(s).
SNe_discoverers = {}
for line in all_data:
    line = line.split(' , ')
    SNe_discoverers[line[0]] = line[-1][:-1]
for n, line in enumerate(Un_data):
    line = line[:-1].split(' , ')
    if line[-1] == '----':
        try:
            line[-1] = SNe_discoverers[line[0]]
        except KeyError:
            try:
                line[-1] = SNe_discoverers[line[0].upper()]
            except KeyError:
                for dataset, dataset_SN_names in free_dataset_dict.items():
                    if line[0] in dataset_SN_names:
                        line[-1] = dataset
                        break
    else:
        for dataset, dataset_SN_names in forced_dataset_dict.items():
            if line[0] in dataset_SN_names:
                line[-1] = dataset
                break
    line = ' , '.join(line) + '\n'
    Un_data[n]=line

#Save Data.
with open('All SNe Union2.1.txt', 'w') as f:
    f.write(Preamble)
    for line in Un_data:
        f.write(line)
