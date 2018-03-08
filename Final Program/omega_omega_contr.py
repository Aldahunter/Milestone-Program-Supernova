folder_final="/media/alex/Shared/University/Physics/Year 3/Physics Problem \
Solving/Computing Project/Programming/Milestone-Program-Supernova/Final \
Program/cont_data/"
import dill as pickle, numpy as np, matplotlib.pyplot as plt, matplotlib.cm as cm
from textwrap import wrap
from scipy.stats import norm
from final_program_imports import *
print('{:#^100}'.format(' Imports Loaded ')+'\n')

print('{:#^100}'.format(' Import Calculated Data ')+'\n')
calculated_data = pickle.load(open(folder_final[:-10]+"final_data.p", "rb"))
for variable, var_data in calculated_data.items():
    exec(variable + ' = var_data')
print('Imported Variables are:\n  · ', end='')
# Lp; Lp_err; chi_Lp; chi_ΩΛ; chi_ωΩ; Ω_DE0; Ω_DE1; ΩΛ; ΩΛ_err; ωΩ; ωΩ_err.
print(' ; '.join(sorted([i for i in calculated_data]))+'\n')



# d88888b d888888b  d888b        .d8b.  d888888b d888888b d8888b.
# 88'       `88'   88' Y8b      d8' `8b `~~88~~' `~~88~~' 88  `8D
# 88ooo      88    88           88ooo88    88       88    88oobY'
# 88~~~      88    88  ooo      88~~~88    88       88    88`8b
# 88        .88.   88. ~8~      88   88    88       88    88 `88.
# YP      Y888888P  Y888P       YP   YP    YP       YP    88   YD
print('{:-^100}'.format(' Setup Figures and Axes ')+'\n')

figsize = (17, 5) #Inches
dpi = 100
x_label = r'Redshift, $z$'
y_label = r'Deceleration Parameter, $q$'
cmap = cm.autumn

mapp_definition = 25 # Number of point calulated between x and y limits.
chi_contours2D = [0, 2.3, 6.18]

ωx_lim = (0.20, 0.70)
ωy_lim = (0.20, 0.70)

Λx_lim = (0.50, 0.90)
Λy_lim = (0.10, 0.50)

Ωx_lim = (0.50, 0.90)
Ωy_lim = (0.10, 0.50)


alpha = 0.0
ls = {'-':(0, ()), '..':(0, (1, 5)), ':':(0, (1, 1)), '--':(0, (5, 5)),
      '-.':(0, (3, 5, 1, 5)), '-..':(0, (3, 4, 1, 4, 1, 4)),
      '--.':(0, (3, 4, 3, 4, 1, 4)), '|-.':(0, (5, 4, 3, 4, 1, 4))}
markers = ['o', '^', '1', 'p', 's', '*', '+', 'x', 'd', r'$\ast $']



#  .o88b.  .d8b.  db       .o88b. .d8888.
# d8P  Y8 d8' `8b 88      d8P  Y8 88'  YP
# 8P      88ooo88 88      8P      `8bo.
# 8b      88~~~88 88      8b        `Y8b.
# Y8b  d8 88   88 88booo. Y8b  d8 db   8D
#  `Y88P' YP   YP Y88888P  `Y88P' `8888Y'
print('{:-^100}'.format(' Perform Required calculations ')+'\n')

data = all_data[np.where(all_data['dataset'] != 'Outlier')]
def ΩΩ2chi(Ω_D, Ω_M, w, z, Lp, obs_data, err_data):
    ΩΩ2mag = lambda ΩΩ, w, z, Lp: omega2mag(ΩΩ[0], z, Lp, w=w, om_M0=ΩΩ[1])
    ΩD_ΩM, ΩΩ2mag_params = (Ω_D, Ω_M), (w, z, Lp)
    return minimise_fn(ΩD_ΩM, ΩΩ2mag, ΩΩ2mag_params, obs_data, err_data)

ω_ΩDs = np.linspace(*ωx_lim, mapp_definition)
ω_ΩMs = np.linspace(*ωy_lim, mapp_definition)
ω_χs = map2D(ΩΩ2chi, ω_ΩDs, ω_ΩMs, fn_args=(ωΩ[0], data['z'], Lp,
                                            data['mag'], data['m_err']))
np.savetxt(folder_final+"omega_omega_w_contour_data.txt", ω_χs)
ω_minargs = np.where(ω_χs == ω_χs.min())

Λ_ΩDs = np.linspace(*Λx_lim, mapp_definition)
Λ_ΩMs = np.linspace(*Λy_lim, mapp_definition)
Λ_χs = map2D(ΩΩ2chi, Λ_ΩDs, Λ_ΩMs, fn_args=(-1.0, data['z'], Lp,
                                            data['mag'], data['m_err']))
np.savetxt(folder_final+"omega_omega_L_contour_data.txt", Λ_χs)
Λ_minargs = np.where(Λ_χs == Λ_χs.min())

Ω_ΩDs = np.linspace(*Ωx_lim, mapp_definition)
Ω_ΩMs = np.linspace(*Ωy_lim, mapp_definition)
Ω_χs = map2D(ΩΩ2chi, Ω_ΩDs, Ω_ΩMs, fn_args=(Ω_DE1['ω_DE'], data['z'], Lp,
                                            data['mag'], data['m_err']))
np.savetxt(folder_final+"omega_omega_O_contour_data.txt", Ω_χs)
Ω_minargs = np.where(Ω_χs == Ω_χs.min())



# d8888b. db       .d88b.  d888888b d888888b d888888b d8b   db  d888b
# 88  `8D 88      .8P  Y8. `~~88~~' `~~88~~'   `88'   888o  88 88' Y8b
# 88oodD' 88      88    88    88       88       88    88V8o 88 88
# 88~~~   88      88    88    88       88       88    88 V8o88 88  ooo
# 88      88booo. `8b  d8'    88       88      .88.   88  V888 88. ~8~
# 88      Y88888P  `Y88P'     YP       YP    Y888888P VP   V8P  Y888P
print('{:-^100}'.format(' Setup Top Plot ')+'\n')

### Set Up.
fig = plt.figure(figsize=figsize)
ωax = fig.add_axes([0.05, 0.05, 0.26, 0.90])  # Add axes for ω cont plot.
Λax = fig.add_axes([0.37, 0.05, 0.26, 0.90])  # Add axes for Λ cont plot.
Ωax = fig.add_axes([0.68, 0.05, 0.26, 0.90])  # Add axes for Ω cont plot.


ωax.scatter(ω_ΩDs[ω_minargs[0]], ω_ΩMs[ω_minargs[1]], marker='o',
            color='purple', zorder=4)
ω_levels = [cont + ω_χs.min() for cont in chi_contours2D]
ω_contrs = ωax.contourf(ω_ΩDs, ω_ΩMs, ω_χs.T,
                        alpha=0.5, zorder=3, levels=ω_levels,
                        colors = cm.Purples(np.linspace(0.3, 0.7,
                                                        len(ω_levels))))

Λax.scatter(Λ_ΩDs[Λ_minargs[0]], Λ_ΩMs[Λ_minargs[1]], marker='o',
            color='purple', zorder=4)
Λ_levels = [cont + Λ_χs.min() for cont in chi_contours2D]
Λ_contrs = Λax.contourf(Λ_ΩDs, Λ_ΩMs, Λ_χs.T,
                        alpha=0.5, zorder=3, levels=Λ_levels,
                        colors = cm.Purples(np.linspace(0.3, 0.7,
                                                        len(Λ_levels))))

Ωax.scatter(Ω_ΩDs[Ω_minargs[0]], Ω_ΩMs[Ω_minargs[1]], marker='o',
            color='purple', zorder=4)
Ω_levels = [cont + Ω_χs.min() for cont in chi_contours2D]
Ω_contrs = Ωax.contourf(Ω_ΩDs, Ω_ΩMs, Ω_χs.T,
                        alpha=0.5, zorder=3, levels=Ω_levels,
                        colors = cm.Purples(np.linspace(0.3, 0.7,
                                                        len(Ω_levels))))

# ax.tick_params(axis = 'both',  # Set tick marks inside and outside of x-axis.
#                 top = True, bottom = True, left = True, right = True,
#                 direction = 'in', length = 3)
# ax.set_xlabel(x_label, labelpad=+4, fontsize=13)
# ax.xaxis.set_label_position('bottom')






# .d8888.  .d8b.  db    db d88888b      dD .d8888. db   db  .d88b.  db   d8b   d
# 88'  YP d8' `8b 88    88 88          d8' 88'  YP 88   88 .8P  Y8. 88   I8I   8
# `8bo.   88ooo88 Y8    8P 88ooooo    d8'  `8bo.   88ooo88 88    88 88   I8I   8
#   `Y8b. 88   88 `8b  d8' 88        d8'     `Y8b. 88   88 88    88 Y8   I8I   8
# db   8D 88   88  `8bd8'  88.      d8'    db   8D 88   88 `8b  d8' `8b d8'8b d8
# `8888Y' YP   YP    YP    Y88888P C8'     `8888Y' YP   YP  `Y88P'   `8b8' `8d8'

save = 'y'
while save.upper() not in ['Y', 'N']:
    save = input('Would you like to save this graph? (y/n): ')
if save.upper() == 'Y':
    fig.savefig(folder_final+'omega_vs_omega.png', format='png',
                bbox_inches='tight', pad_inches=0, dpi = dpi)
    print('{:-^100}'.format(' Graph Saved ')+'\n')
# plt.show()
print('{:#^100}'.format(' Program Complete '))
