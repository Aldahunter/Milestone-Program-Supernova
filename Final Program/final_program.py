"""Supernova Cosmology Program for Physics Problem Solving."""
folder="/media/alex/Shared/University/Physics/Year 3/Physics Problem Solving/Computing Project/Programming/Milestone-Program-Supernova/Final Program/"
import numpy as np, matplotlib.pyplot as pyplot, matplotlib.cm as cm
import scipy, tkinter
from final_program_imports import *
print('{:#^100}'.format(' Imports Loaded ')+'\n')

### Remove Ouutliers ###
data = all_data[np.where(all_data['dataset'] != 'Outlier')]



### Find Lpeak ###
data_lz = data[np.where(data['z'] < 0.1)]
lz_Lps = mag2Lp(data_lz['mag'], data_lz['z'], 0.0, low_z = True)

# Calculate minimised χ² and best value and uncertainty for Peak Luminosity #
print('{:-^100}'.format(' Find Peak Luminosity ')+'\n')
Lp2mag_params = (data_lz['z'], 0.0, True)
chi_Lp, Lp, Lp_err = minimise_chi_1D(Lp2mag, 3e39, Lp2mag_params,
                                     data_lz['mag'], data_lz['m_err'])
# Print Units to Screen #
adopted_units = (Lp*1e-7, Lp_err*1e-7, (Lp_err/Lp)*100.0, chi_Lp)
string = 'L_peak = {:.2e} ± {:.0e} ({:.2g}%) J·s⁻¹·Å⁻¹ | Reduced χ² = {:.2f}\n'
print(string.format(*adopted_units))



### Find Ω and ω for D.E. ###
print('{:-^100}'.format(' Find Ω and ω Dark Energy ')+'\n')

# Bestfit Ω for Λ #
omega2mag_params = (data['z'], Lp, -1)
chi_ΩΛ, ΩΛ, ΩΛ_err = minimise_chi_1D(omega2mag, 0.50, omega2mag_params,
                                     data['mag'], data['m_err'])
string = 'For ω of -1: Ω_Λ = {:.2e} ± {:.0e} ({:.2g}%) | Reduced χ² = {:.2f}\n'
print(string.format(ΩΛ, ΩΛ_err, (ΩΛ_err/ΩΛ)*100, chi_ΩΛ))

# Bestfit ω for multiple values of Ω_DE #
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

# Bestfit Ω and ω to SNe #
w_omega2mag = lambda w_omega, z, Lp: omega2mag(w_omega[1], z, Lp, w_omega[0])
w_omega2mag_params = (data['z'], Lp)
chi_ωΩ, ωΩ, ωΩ_err = minimise_chi_2D(w_omega2mag, (-1.0, 0.70),
                                     w_omega2mag_params, data['mag'],
                                     data['m_err'])
string = 'For Ω of {:.2g} ± {:.0g} ({:.2g}%) : ω = {:.3g} ± {:.0g} ({:.2g}%) | \
Reduced χ² = {:.2f}\n'
print(string.format(ωΩ[1], ωΩ_err[1], (ωΩ_err[1]/ωΩ[1])*100, ωΩ[0], ωΩ_err[0],
                    (ωΩ_err[0]/ωΩ[0])*100, chi_ωΩ))
print('{:-^100}'.format(' Calculations Complete ')+'\n')


### Save Results to Pickle ###
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
    pickle.dump(calculated_data, open(folder+"final_data.p", "wb" ))
    print('{:-^100}'.format(' Data Saved ')+'\n')
print('\n'+'{:#^100}'.format(' Program Complete '))
