The '_\*.txt_', '_\*.tex_' and '_\*.pdf_' files in this directory all holder data on Supernovae (SNe). The **primary** Supernovae **files** are:
 - '*All SNe 1953-2015.txt*' (**All SNe dsicovered 1953-2015**, http://www.cbat.eps.harvard.edu/lists/Supernovae.html)

 - '*SCPUnion2.1_AllSNe_table.tex*' (**Union2.1**, http://supernova.lbl.gov/Union/)

 - '*All SNe SNLS.txt*' (**Supernova Legacy Survey**,  https://arxiv.org/pdf/astro-ph/0510447.pdf
                           \>> Table 9: '_SNLS Type Ia supernovae_')

 - '*All SNe HST Riess.txt*' (**HST Riess et al.**, https://arxiv.org/pdf/astro-ph/0611572.pdf
                                \>> Table 1: '_SN Discovery Data_')

 - '*All SNe SDSS-II.txt*' (**Sloan Digital Sky Survey II**, https://arxiv.org/pdf/0802.3220.pdf
                              \>> Table 2: '_SDSS-II SN Spectroscopic Follow-up   Observations_')

 - '*All SNe Essence.txt*' (**ESSENCE**, https://arxiv.org/pdf/1603.03823.pdf
                              \>> Table 6: '_Transient Objects Considered for Follow-up Observations by the ESSENCE Survey_')

 - '*All SNe HST CSS.txt*' (**HST Cluster Supernova Survey**, https://arxiv.org/pdf/0908.3928.pdf
                              \>> Table 3: '_SNe hosted by spectroscopically confirmed cluster members_',
                                  Table 4: '_SNe hosted by field galaxies and galaxies with unknown redshift_')
 - '*All SNe CalanTololo.txt*' (**Calan/Tololo Supernova Survey**, https://arxiv.org/pdf/astro-ph/9609062.pdf
                                                \>> Table 1: '_Colors and Magnitudes of the Calan/Tololo Supernovae Ia_')'


The python scripts '_all_SNe_\*.py_' in this directory manipulate these primary files to produce the other secondary text files, '_All SNe \*.txt_'. The **order** in which these **python files** are **run** are:

 1. *all_SNe_Ia_selector.py* : Picks out all type 'Ia' (or unknown) SNe discovered between 1953 and 2015.
                               **['All SNe 1953-2015.txt'
                                    \>> 'All SNe Ia.txt']**

 2. *all_SNe_Union2.1_cutter.py* : Picks out suitable SNe from the Union2.1 dataset.
                                   **['SCPUnion2.1_AllSNe_table.tex'
                                        \>> 'All SNe Union2.1.txt']**
 3. *all_SNe_Union2.1_exceptions_handler.py* : Handles known exceptions/errors with the Union2.1 dataset, such as incorrect naming schemes.
                                               **['All SNe Union2.1.txt'
                                                  'All SNe HST CSS.txt'
                                                    />> 'All SNe Union2.1.txt']**

 4. *all_SNe_Union2.1_dataset_tagger.py* : Tags SNe from Union2.1 with their Discoverer(s).
                                           **['*All SNe Union2.1.txt*',
                                              '*All SNe Ia.txt*',
                                              '*All SNe SNLS.txt*',
                                              '*All SNe HST Riess.txt*',
                                              '*All SNe SDSS-II.txt*',
                                              '*All SNe Essence.txt*',
                                              '*All SNe CalanTololo.txt*',
                                                \>> '*All SNe Union2.1.txt*']**

 5. *all_SNe_Union2.1_dataset_abbreviator.py* : Abbreviates the datasets of the Union2.1 data, to give a more uniform set of datasets.
                                                **['*All SNe Union2.1.txt*',
                                                  \>> '*All SNe Union2.1.txt*']**

 6. *all_SNe_Union2.1_dataset_lister.py* : (Optional) Lists all the different datasets and their frequency in a text file.
                                           **['*All SNe Union2.1.txt*',
                                                \>> '*All SNe Union2.1 Unique Datasets.txt*']**


There are some **exceptions** to the SNe names, the related exceptions are:
 1. SN name error: '2003XX' -> '2003lv' (https://ned.ipac.caltech.edu/forms/byname.html
                                           \>> Set 'Object Name' to 'SN2003lv' then click 'Submit Query'
                                             \>> Go to section 'ESSENTIAL NOTE for SN 2003lv'.)
 2. SN name to SDSS-II name '2005mm' -> '11206' (https://ned.ipac.caltech.edu/forms/byname.html
                                                   \>> Set 'Object Name' to 'SN2005mm' then click 'Submit Query'
                                                     \>> Go to section 'CROSS-IDENTIFICATIONS for SN 2005mm'
                                                       \>> Under column 'Object Names'.)
 3. SNe incorrect CSS naming: '[A-Z]-[0-9]{3,3}' -> 'SCP[0-9]{2,2}[A-Z][0-9]{2,2}' (https://arxiv.org/pdf/0908.3928.pdf
                                    e.g. 'A-004' -> 'SCP06A4'                         \>> Table 3 : '_SNe hosted by spectroscopically confirmed cluster members_'
                                                                                          Table 4 : '_SNe hosted by field galaxies and galaxies with unknown redshift_')
                                                                                    ***Note:** this is known as these papers (https://arxiv.org/pdf/1110.6442.pdf) written by the SNe Cosmology Project who put together the Union2.1 dataset have the same properties as the SNe with the incorrect naming scheme.*
