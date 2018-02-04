"""Picks out all the different datasets from supernovae within the Union2.1 \
dataset ('All SNe Union2.1.txt') and lists them in a text file ('All SNe \
Union2.1 Unique Datasets.txt'), along with the frequency/size of each dataset.
"""

with open("All SNe Union2.1.txt", 'r') as f:
    data = f.readlines()


discoverers = {}
for line in data[1:]:
    line = line.strip('\n').split(' , ')
    if line[-1] not in discoverers:
        discoverers[line[-1]] = 1
    else:
        discoverers[line[-1]] += 1
dict_keys = sorted(list(discoverers.keys()))

with open('All SNe Union2.1 Unique Datasets.txt', 'w') as f:
    f.write('#Dataset : Size\n')
    for discoverer in dict_keys:
        f.write(discoverer + ' : ' + str(discoverers[discoverer]) + '\n')
