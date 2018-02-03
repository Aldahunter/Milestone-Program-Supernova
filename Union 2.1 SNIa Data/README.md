The '_\*.txt_', '_\*.tex_' and '_\*.pdf_' files in this directory all holder data on
Supernovae (SNe). The **primary** Supernovae **files** are:
 - '*All SNe 1953-2015.txt*' (**All SNe dsicovered 1953-2015**,
                              http://www.cbat.eps.harvard.edu/lists/Supernovae.html)
 - '*SCPUnion2.1_AllSNe_table.tex*' (**Union2.1**,
                                     http://supernova.lbl.gov/Union/)
 - '*All SNe SNLS.txt*' (**Supernova Legacy Survey**,
                         https://arxiv.org/pdf/astro-ph/0510447.pdf
                           \>> Table 9: 'SNLS Type Ia supernovae')
 - '*All SNe HST Riess.txt*' (**HST Riess et al.**,
                              https://arxiv.org/pdf/astro-ph/0611572.pdf
                                \>> Table 1: 'SN Discovery Data')
 - '*All SNe SDSS-II.txt*' (**Sloan Digital Sky Survey II**,
                            https://arxiv.org/pdf/0802.3220.pdf
                              \>> Table 2: 'SDSS-II SN Spectroscopic Follow-up
                                            Observations')
 - '*All SNe Essence.txt*' (**ESSENCE**,
                            https://arxiv.org/pdf/1603.03823.pdf
                              \>> Table 6: 'Transient Objects Considered for
                                            Follow-up Observations by the
                                            ESSENCE Survey')
 - '*All SNe HST CSS.txt*' (**HST Cluster Supernova Survey**,
                            https://arxiv.org/pdf/0908.3928.pdf
                              \>> Table 3: 'SNe hosted by spectroscopically
                                            confirmed cluster members',
                                  Table 4: 'SNe hosted by field galaxies and
                                            galaxies with unknown redshift')


The python scripts '_all_SNe_\*.py_' in this directory manipulate these primary
files to produce the other secondary text files, '_All SNe \*.txt_'. The **order** in
which these **python files** are **run** are:

 1. *all_SNe_Ia_selector.py* : Picks out all type 'Ia' (or unknown) SNe.
                             **['All SNe 1953-2015.txt'
                               \>> 'All SNe Ia.txt']**
 2. *all_SNe_Union2.1_cutter.py* : Picks out suitable SNe from the Union2.1
                                 dataset.
                                 **['SCPUnion2.1_AllSNe_table.tex'
                                   \>> 'All SNe Union2.1.txt']**
 3. *all_SNe_Union2.1_dataset_tagger.py* : Tags SNe from Union2.1 with their
                                           Discoverer(s).
                                           **['*All SNe Union2.1.txt*',
                                              '*All SNe Ia.txt*',
                                              '*All SNe SNLS.txt*',
                                              '*All SNe HST Riess.txt*',
                                              '*All SNe SDSS-II.txt*',
                                              '*All SNe Essence.txt*',
                                             \>> '*All SNe Union2.1.txt*']**
 4. *all_SNe_Union2.1_no_dataset_cutter.py* : Picks out SNe from Union2.1 with no
                                            Discoverer then orders them by
                                            naming style.
                                            **['*All SNe Union2.1.txt*'
                                              \>> '*All SNe Union2 No Dataset.txt*']**


There are some **exceptions** to the SNe names, the related exceptions are:
 1. SN name error: '2003XX' -> '2003lv' (https://ned.ipac.caltech.edu/forms/byname.html
                                           \>> Set 'Object Name' to 'SN2003lv'
                                               then click 'Submit Query'
                                           \>> Go to section 'ESSENTIAL NOTE for
                                               SN 2003lv'.)
 2. SN name to SDSS-II name '2005mm' -> '11206' (https://ned.ipac.caltech.edu/forms/byname.html
                                                   \>> Set 'Object Name' to
                                                       'SN2005mm' then click
                                                       'Submit Query'
                                                   \>> Go to section
                                                       'CROSS-IDENTIFICATIONS
                                                       for SN 2005mm'
                                                   \>> Under column 'Object
                                                       Names'.)
