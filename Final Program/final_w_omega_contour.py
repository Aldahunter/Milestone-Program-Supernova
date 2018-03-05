folder_final="/media/alex/Shared/University/Physics/Year 3/Physics Problem Solving/Computing Project/Programming/Milestone-Program-Supernova/Final Program/"
import dill as pickle, numpy as np, matplotlib.pyplot as plt, matplotlib.cm as cm
from textwrap import wrap
from final_program_imports import *
print('{:#^100}'.format(' Imports Loaded ')+'\n')


# Import Calculated Data #
print('{:#^100}'.format(' Import Calculated Data ')+'\n')
calculated_data = pickle.load(open(folder_final+"final_data.p", "rb"))
for variable, var_data in calculated_data.items():
    exec(variable + ' = var_data')
print('Imported Variables are:\n  · ', end='')
print(' ; '.join(sorted([i for i in calculated_data]))+'\n')



### Figure & Axis Attributes ###
load_ωΩ_χmap = 'y'
load_q_map = 'y'
load_age_map = 'y'
figsize = (7,14) #Inches
x_lim = (0.0, 1.0, 500) # Omega_DE.
y_lim = (-2.15, -0.92, 500) # w_DE.
dpi = 100
age_units = "Gyr"
chi_contours = [0, 2.3, 4.61] # Added onto minimum χ².
q_contours = [-0.7, -0.8, -0.9, -1.0, -1.1, -1.2]
age_contours = [11.1, 11.3, 11.5, 11.7, 11.9]


### Calculations ###
print('{:-^100}'.format(' Perform Required calculations ')+'\n')
def ωΩ2chi(Ω, ω, z, Lp, obs_data, err_data):
    ωΩ2mag = lambda ωΩ, z, Lp: omega2mag(ωΩ[1], z, Lp, ωΩ[0])
    ωΩ_params, ωΩ2mag_params = (ω, Ω), (z, Lp)
    return minimise_fn(ωΩ_params, ωΩ2mag, ωΩ2mag_params, obs_data, err_data)

# Calculate X & Y Values #
data = all_data[np.where(all_data['dataset'] != 'Outlier')]
omegas = np.linspace(*x_lim) # X values.
ws = np.linspace(*y_lim) # Y values.


## Calculate χ² Values ##
if load_ωΩ_χmap.upper() == 'Y':
    χ_ωΩ = np.loadtxt("w_omega_contour_data(old_hd).txt")
    print('{:~^100}'.format(' χ² Values Loaded ')+'\n')
else:
    χ_ωΩ = map2D(ωΩ2chi, omegas, ws, fn_args=(Lp, data['mag'], data['m_err']))
    np.savetxt("w_omega_contour_data(new).txt", χ_ωΩ)
    print('{:~^100}'.format(' χ² Values Calculated and Saved ')+'\n')

# if load_ΩΛ_χmap.upper() == 'Y':
#     χ_ΩΛ = np.loadtxt("w_omega_contour_data(old_hd).txt")
#     print('{:~^100}'.format(' χ² Values Loaded ')+'\n')
# else:
#     χ_ΩΛ = map2D(ωΩ2chi, omegas, ws, fn_args=(Lp, data['mag'], data['m_err']))
#     np.savetxt("w_omega_contour_data.txt", χ_ΩΛ)
#     print('{:~^100}'.format(' χ² Values Calculated and Saved ')+'\n')

min_chi, chi_red = np.nanmin(χ_ωΩ), np.nanmin(χ_ωΩ) / float(data['mag'].size)
chi_contours = [cont + min_chi for cont in chi_contours]
string = "The min χ² is: {:.2f} (reduced: {:.2f}),".format(min_chi, chi_red)
string +=  " with contours: " + ", ".join(['%.2f'%(i,) for i in chi_contours])
print(string, '\n')


## Calculate Deceleration Parameters ##
if load_q_map.upper() == 'Y':
    qs = np.loadtxt("w_omega_contour_data_q.txt")
    print('{:~^100}'.format(' Deceleration Map Loaded ')+'\n')
else:
    decel_fn = lambda Ω, ω, z : decelerate_param(Ω, z, w=ω)
    qs = map2D(decel_fn, omegas, ws, fn_args=(0.0,))
    np.savetxt("w_omega_contour_data_q.txt", qs)
    print('{:~^100}'.format(' Deceleration Map Calculated and Saved ')+'\n')


## Calulate Universe Age Values ##
if load_age_map.upper() == 'Y':
    ages = np.loadtxt("w_omega_contour_data_age.txt")
    print('{:~^100}'.format(' Universe Age Map Loaded ')+'\n')
else:
    age_fn = lambda Ω, ω: universe_age(Ω, w = ω)
    ages = map2D(age_fn, omegas, ws)
    np.savetxt("w_omega_contour_data_age.txt", ages)
    print('{:~^100}'.format(' Universe Age Map Calculated and Saved ')+'\n')
ages = ages / 1e9 #Convert to Gyrs.



### Plot Contour Graph ###
print('{:-^100}'.format(' Plotting Graph ')+'\n')

# Setup Figure and Axes #
fig = plt.figure()
ax = fig.add_subplot(111)

# Plot on Axes #
chi_colours = cm.Oranges(np.linspace(0.3, 0.7, len(chi_contours)))
chicont = ax.contourf(omegas[::-1], ws[::-1], χ_ωΩ, levels=chi_contours,
                      colors = chi_colours, zorder=2, alpha=0.5)

q_colors = cm.gray(np.linspace(0.0, 1.0, len(q_contours)))
qcont = ax.contour(omegas[::-1], ws[::-1], qs, levels=q_contours[::-1],
                   colors=q_colors, linestyles='--', zorder=1, alpha=1, )
ax.clabel(qcont, inline=True, fontsize=10, fmt="%.1f")

age_colors = cm.bone(np.linspace(0.0, 1.0, len(age_contours)))
agecont = ax.contour(omegas[::-1], ws[::-1], ages, levels=age_contours,
                     colors=age_colors, linestyles=':', zorder=0, alpha=1.0)
agecont.colors = cm.bone(np.linspace(0.0, 1.0, len(agecont.levels)))
ax.clabel(agecont, inline=True, fontsize=10, fmt="%.1f Gyr")


# ω_err, Ω_err = abs(ωΩ[0] - -2.11668), abs(ωΩ[1] - 0.419249)
# ωΩ_err = (ω_err, Ω_err)
# ax.axhline(y=ωΩ[0]+ωΩ_err[0], c='orange', ls='-', zorder=2)
# ax.axhline(y=ωΩ[0]-ωΩ_err[0], c='orange', ls='-', zorder=2)
# ax.axvline(x=ωΩ[1]-ωΩ_err[1], c='orange', ls='-', zorder=2)


# Figure and Axes Final Corrections #
ax.set_xlim(*x_lim[:-1])
ax.set_ylim(*y_lim[:-1])
plt.show()

print('{:#^100}'.format(' Program Complete '))
