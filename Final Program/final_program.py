"""Supernova Cosmology Program for Physics Problem Solving."""
folder_final="/media/alex/Shared/University/Physics/Year 3/Physics Problem Solving/Computing Project/Programming/Milestone-Program-Supernova/Final Program/"
import numpy as np, matplotlib.pyplot as pyplot, matplotlib.cm as cm
import scipy, tkinter
from final_program_imports import *
print('{:#^100}'.format(' Imports Loaded ')+'\n')

## Remove Ouutliers
data = all_data[np.where(all_data['dataset'] != 'Outlier')]



# db      d8888b. d88888b  .d8b.  db   dD
# 88      88  `8D 88'     d8' `8b 88 ,8P'
# 88      88oodD' 88ooooo 88ooo88 88,8P
# 88      88~~~   88~~~~~ 88~~~88 88`8b
# 88booo. 88      88.     88   88 88 `88.
# Y88888P 88      Y88888P YP   YP YP   YD
print('{:-^100}'.format(' Find Peak Luminosity ')+'\n')
data_lz = data[np.where(data['z'] < 0.1)]
lz_Lps = mag2Lp(data_lz['mag'], data_lz['z'], 0.0, low_z = True)

Lp2mag_params = (data_lz['z'], 0.0, True)
chi_Lp, Lp, Lp_err = minimise_chi_1D(Lp2mag, 3e39, Lp2mag_params,
                                     data_lz['mag'], data_lz['m_err'])
# Print Units to Screen #
adopted_units = (Lp*1e-7, Lp_err*1e-7, (Lp_err/Lp)*100.0, chi_Lp)
string = 'L_peak = {:.2e} ± {:.0e} ({:.2g}%) J·s⁻¹·Å⁻¹ | Reduced χ² = {:.2f}\n'
print(string.format(*adopted_units))



# d88888b d888888b d8b   db d8888b.      d8888b.  .d8b.  d8888b.  .d8b.  .88b  d88. .d8888.
# 88'       `88'   888o  88 88  `8D      88  `8D d8' `8b 88  `8D d8' `8b 88'YbdP`88 88'  YP
# 88ooo      88    88V8o 88 88   88      88oodD' 88ooo88 88oobY' 88ooo88 88  88  88 `8bo.
# 88~~~      88    88 V8o88 88   88      88~~~   88~~~88 88`8b   88~~~88 88  88  88   `Y8b.
# 88        .88.   88  V888 88  .8D      88      88   88 88 `88. 88   88 88  88  88 db   8D
# YP      Y888888P VP   V8P Y8888D'      88      YP   YP 88   YD YP   YP YP  YP  YP `8888Y'
print('{:-^100}'.format(' Find Ω and ω Dark Energy ')+'\n')

## Bestfit Ω for Λ
omega2mag_params = (data['z'], Lp, -1)
chi_ΩΛ, ΩΛ, ΩΛ_err = minimise_chi_1D(omega2mag, 0.50, omega2mag_params,
                                     data['mag'], data['m_err'])
string = 'For ω of -1: Ω_Λ = {:.2e} ± {:.0e} ({:.2g}%) | Reduced χ² = {:.2f}\n'
print(string.format(ΩΛ, ΩΛ_err, (ΩΛ_err/ΩΛ)*100, chi_ΩΛ))


## Bestfit ω for multiple Ω
Ω_DEs, Ω_DE_arr = sorted([ΩΛ, 0.71]), []
for n_Ω in Ω_DEs:
    w2mag = lambda w, omega, z, Lp: omega2mag(omega, z, Lp, w)
    w2mag_params = (n_Ω, data['z'], Lp)
    chi_ωΛ, ωΛ, ωΛ_err = minimise_chi_1D(w2mag, -1.0, w2mag_params,
                                         data['mag'], data['m_err'])
    Ω_DE_arr.append({'Ω_DE':n_Ω, 'χ²_DE':chi_ωΛ, 'ω_DE':ωΛ, 'ω_err':ωΛ_err})
    string = 'For Ω of {:.2g}: ω = {:.3g} ± {:.0g} ({:.2g}%) | Reduced χ² = \
    {:.2f}\n'
    print(string.format(n_Ω, ωΛ, ωΛ_err, (ωΛ_err/ωΛ)*100, chi_ωΛ))


## Bestfit ω & Ω
w_omega2mag = lambda w_omega, z, Lp: omega2mag(w_omega[1], z, Lp, w_omega[0])
w_omega2mag_params = (data['z'], Lp)
chi_ωΩ, ωΩ = minimise_chi_2D(w_omega2mag, (-1.0, 0.70),
                                     w_omega2mag_params, data['mag'],
                                     data['m_err'], err_stats = False)
ωΩ_err = (abs(ωΩ[0] - -2.19136), abs(ωΩ[1] - 0.475499)) # Read off contour plot.
string = 'For Ω of {:.2g} ± {:.0g} ({:.2g}%) : ω = {:.3g} ± {:.0g} ({:.2g}%) | \
Reduced χ² = {:.2f}\n'
print(string.format(ωΩ[1], ωΩ_err[1], (ωΩ_err[1]/ωΩ[1])*100, ωΩ[0], ωΩ_err[0],
                    (ωΩ_err[0]/ωΩ[0])*100, chi_ωΩ))
print('{:-^100}'.format(' Calculations Complete ')+'\n')



# .d8888.  .d8b.  db    db d88888b
# 88'  YP d8' `8b 88    88 88'
# `8bo.   88ooo88 Y8    8P 88ooooo
#   `Y8b. 88~~~88 `8b  d8' 88~~~~~
# db   8D 88   88  `8bd8'  88.
# `8888Y' YP   YP    YP    Y88888P
save = ''
while save.upper() not in ['Y', 'N']:
    save = input('Would you like to save this data? (y/n): ')

if save.upper() == 'Y':
    import dill as pickle
    calculated_data = {}
    calculated_data = {'chi_Lp':chi_Lp, 'Lp':Lp, 'Lp_err':Lp_err,
                       'chi_ΩΛ':chi_ΩΛ, 'ΩΛ':ΩΛ, 'ΩΛ_err':ΩΛ_err,
                       'chi_ωΩ':chi_ωΩ, 'ωΩ':ωΩ, 'ωΩ_err':ωΩ_err}
    for n, Ω_DE_tup in enumerate(Ω_DE_arr):
        calculated_data['Ω_DE'+str(n)] = Ω_DE_tup
    print("Saved Data: ")
    for key in calculated_data:
        print('  · ' + key + ' - ' + str(calculated_data[key]))
    pickle.dump(calculated_data, open(folder_final+"final_data.p", "wb" ))
    print('{:-^100}'.format(' Data Saved ')+'\n')
print('\n'+'{:#^100}'.format(' Program Complete '))
