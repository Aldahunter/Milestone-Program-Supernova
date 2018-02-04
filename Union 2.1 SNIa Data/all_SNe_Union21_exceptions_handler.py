"""Handles all known naming errors/exceptions with in the Union2.1 dataset \
("All SNe Union2.1.txt")' renaming them for dataset 'tagging'. Data is from: \
https://ned.ipac.caltech.edu/forms/byname.html (Nasa NED database) and \
https://arxiv.org/pdf/1010.5786.pdf (HST CSS SN - Table 3)."""

import re
folder = '/media/alex/Shared/University/Physics/Year 3/Physics Problem Solving/Computing Project/Programming/Milestone-Program-Supernova/Union 2.1 SNIa Data/'
with open(folder+"All SNe Union2.1.txt", 'r') as f:
    Un_data = f.readlines()
with open(folder+"All SNe HST CSS.txt", 'r') as f:
    CSS_data = f.readlines()[1:]
exptns_dict = {'2003XX' : '2003lv', #Exception 1 (See README.md); incorrect name.
               '2005mm' : '11206'}  #Exception 2 (See README.md); needs SDSS-II name to be tagged.
RE = re.compile(r'[A-Z]-\d{3,3}')   #Exception 3 (See README.md); incorrect HST CSS naming system.

for n, Un_line in enumerate(Un_data[1:]):
    Un_line = Un_line.split(' , ')

    if Un_line[0] in exptns_dict:
        Un_line[0] = exptns_dict[Un_line[0]]

    if RE.match(Un_line[0]):
        for CSS_line in CSS_data:
            CSS_line = CSS_line.split(' ')
            if Un_line[0][0] + Un_line[0][-2:] == CSS_line[0][-3:]:
                Un_line[0] = CSS_line[0]
            elif Un_line[0][0] + Un_line[0][-1:] == CSS_line[0][-2:]:
                Un_line[0] = CSS_line[0]

    Un_data[n+1] = ' , '.join(Un_line)


with open(folder+"All SNe Union2.1.txt", 'w') as f:
    for Un_line in Un_data:
        f.write(Un_line)
