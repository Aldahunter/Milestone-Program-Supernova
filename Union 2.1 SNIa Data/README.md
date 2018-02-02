The '_\*.txt_', '_\*.tex_' and '_\*.pdf_' files in this directory all holder data on
Supernovae (SNe). The **primary** Supernovae **files** are:
 - '*All SNe 1953-2015.txt*' (http://www.cbat.eps.harvard.edu/lists/Supernovae.html)
 - '*SCPUnion2.1_AllSNe_table.tex*' (http://supernova.lbl.gov/Union/)


The python scripts '_all_SNe_\*.py_' in this directory manipulate these primary
files to produce the other secondary text files, '_All SNe \*.txt_'. The **order** in
which these **python files** are **run** are:

 1. *all_SNe_Ia_selector.py* : Picks out all type 'Ia' (or unknown) SNe.
                             ['All SNe 1953-2015.txt'
                               \>> 'All SNe Ia.txt']
 2. *all_SNe_Union2.1_cutter.py* : Picks out suitable SNe from the Union2.1
                                 dataset.
                                 **['SCPUnion2.1_AllSNe_table.tex'
                                    \>> 'All SNe Union2.1.txt']**
 3. *all_SNe_Union2.1_IAUC_dataset_tagger.py* : Tags SNe from Union2.1 with their
                                              Discoverer(s).
                                              **['*All SNe Union2.1.txt*',
                                               '*All SNe Ia.txt*'
                                                \>> '*All SNe Union2.1.txt*']**
 4. *all_SNe_Union2.1_no_dataset_cutter.py* : Picks out SNe from Union2.1 with no
                                            Discoverer then orders them by
                                            naming style.
                                            **['*All SNe Union2.1.txt*'
                                              \>> '*All SNe Union2 No Dataset.txt*']**
