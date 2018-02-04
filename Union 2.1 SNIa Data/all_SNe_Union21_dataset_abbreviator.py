"""Picks out all Supernovae from Union2.1 dataset ('All SNe Union2.1.txt') and \
abbreviates the dataset tag to the correct dataset discoverer(s). Data is \
from: https://www.cfa.harvard.edu/supernova/cfasn/bulk/cfalc_allsn.tar.gz \
(Harvard-Smithsonian Center for Astrophysics - CfA), \
https://arxiv.org/pdf/1108.3108.pdf (Carnegie SN Project - CSP, Table 2: \
Photometric/Spectroscopic Properties of 50 SN Ia), \
https://arxiv.org/pdf/astro-ph/9609062.pdf (Calan/Tololo SNe Survey- C/TSS, \
Table 1: Colors and Magnitudes of the Calan/Tololo Supernovae Ia)"""

folder = '/media/alex/Shared/University/Physics/Year 3/Physics Problem Solving/Computing Project/Programming/Milestone-Program-Supernova/Union 2.1 SNIa Data/'
with open(folder+"All SNe Union2.1.txt", 'r') as f:
    data = f.readlines()
dataset_dict = {'Sloan Digital Sky Survey' : 'SDSS II', 'SDSS II' : 'SDSS II',

                'Riess' : 'HST Riess', 'Cluster' : 'HST CSS',

                'High-Z': 'High-Z SS', 'Schmidt' : 'High-Z SS',

                'Supernova Cosmology Project' : 'SCP', 'Perlmutter' : 'SCP',
                'Armstrong' : 'SCP',

                'LOSS' : 'CfA', 'LOTOSS' : 'CfA', 'BAO' : 'CfA', 'Lick' : 'CfA',
                'Pollas' : 'CfA', 'Arbour' : 'CfA', 'Schwartz' : 'CfA',
                'Boles' : 'CfA', 'Johnson' : 'CfA',

                'Quimby' : 'CSP', 'THCA' : 'CSP', 'Itagaki' : 'CSP',
                'Puckett' : 'CSP', 'Nissinen' : 'CSP', 'Prasad':'CSP',
                'Newton' : 'CSP', 'Berlind' : 'CSP', 'Bincoletto' : 'CSP',
                'Brady' : 'CSP', 'Holmes' : 'CSP', 'Kloehr' : 'CSP',
                'Magee' : 'CSP', 'Mitchell' : 'CSP', 'Nicolas' : 'CSP',
                'Peters' : 'CSP', 'Rich': 'CSP',

                'European Supernova Cosmology Consortium' : 'C/TSS',
                'Mueller' : 'C/TSS', 'Antezana' : 'C/TSS', 'GOODS' : 'C/TSS',
                'Wischnjewsky' : 'C/TSS', 'McNaught' : 'C/TSS',
                'Gonzalez' : 'C/TSS', 'Chassagne' : 'C/TSS', 'Yuan' : 'C/TSS',
                'Chornock' : 'C/TSS', 'Fujita' : 'C/TSS', 'Tsvetanov' : 'C/TSS',
                'Wild' : 'C/TSS'}

for n, line in enumerate(data[1:]):
    line = line.strip('\n').split(' , ')
    for dataset in dataset_dict:
        if dataset in line[-1]:
            line[-1] = dataset_dict[dataset]
            data[n+1] = ' , '.join(line) + '\n'
            break


with open(folder+"All SNe Union2.1.txt", 'w') as f:
    for line in data:
        f.write(line)
