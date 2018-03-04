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
visible_outliers = ['2006cm', '2005a', '2006br', 'm043', 'g055']
invisible_outliers = ['2002hw', '1999gd', '2005mc', '2004gs', '2006gj',
                      '2006os', '2006cc', '2006eq', 'm027', '2002kc', '1997o',
                      'k485', '1994H', '1995at', '1999fm', '03D4ag', '2007s',
                      '2007ca', '2007au', '2006bw', '2006cp', '2006qo',
                      '2001ie', 'g050', '2005ix', '2005hy', 'k411', '2000dk',
                      '2006ej', '1995ak', '2006en', '2003iv',
                      '2005if', '1997y']



for n, line in enumerate(data[1:]):
    line = line.strip('\n').split(' , ')
    for dataset in dataset_dict:
        if dataset in line[-1]:
            line[-1] = dataset_dict[dataset]
            data[n+1] = ' , '.join(line) + '\n'
            break

### Deal with Outliers ###
new_data = [data[0]]
outliers = visible_outliers + invisible_outliers
for n, line in enumerate(data[1:]):
    line = line.strip('\n').split(' , ')
    if line [0] not in outliers:
        new_data.append(' , '.join(line) + '\n')
    elif line[0] in visible_outliers:
        line[-1] = 'Outlier'
        new_data.append(' , '.join(line) + '\n')


with open(folder+"All SNe Union2.1.txt", 'w') as f:
    for line in new_data:
        f.write(line)
