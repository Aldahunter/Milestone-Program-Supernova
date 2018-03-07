folder_final="/media/alex/Shared/University/Physics/Year 3/Physics Problem Solving/Computing Project/Programming/Milestone-Program-Supernova/Final Program/"
import dill as pickle, numpy as np, matplotlib.pyplot as plt, matplotlib.cm as cm
from textwrap import wrap
from scipy.stats import norm
from final_program_imports import *
print('{:#^100}'.format(' Imports Loaded ')+'\n')

print('{:#^100}'.format(' Import Calculated Data ')+'\n')
calculated_data = pickle.load(open(folder_final+"final_data.p", "rb"))
for variable, var_data in calculated_data.items():
    exec(variable + ' = var_data')
print('Imported Variables are:\n  · ', end='')
print(' ; '.join(sorted([i for i in calculated_data]))+'\n')



# d88888b d888888b  d888b        .d8b.  d888888b d888888b d8888b.
# 88'       `88'   88' Y8b      d8' `8b `~~88~~' `~~88~~' 88  `8D
# 88ooo      88    88           88ooo88    88       88    88oobY'
# 88~~~      88    88  ooo      88~~~88    88       88    88`8b
# 88        .88.   88. ~8~      88   88    88       88    88 `88.
# YP      Y888888P  Y888P       YP   YP    YP       YP    88   YD
print('{:-^100}'.format(' Setup Figures and Axes ')+'\n')

figsize = (6.5,5.0) #Inches
x_lim = (-0.0, 2.0)
y_lim = (-1.25, 0.55)
y_lim_res = (-20,25)
x_lim_occ = (0,60)
dpi = 1000
bin_width = 1.0
x_label = r'Redshift, $z$'
y_label = r'Deceleration Parameter, $q$'
y_label_res = r'Norm. Residual'
x_label_occ = r'Occurrence'
alpha = 0.0
ls = {'-':(0, ()), '..':(0, (1, 5)), ':':(0, (1, 1)), '--':(0, (5, 5)),
      '-.':(0, (3, 5, 1, 5)), '-..':(0, (3, 4, 1, 4, 1, 4)),
      '--.':(0, (3, 4, 3, 4, 1, 4)), '|-.':(0, (5, 4, 3, 4, 1, 4))}
markers = ['o', '^', '1', 'p', 's', '*', '+', 'x', 'd', r'$\ast $']
cmap = cm.autumn



#  .o88b.  .d8b.  db       .o88b. .d8888.
# d8P  Y8 d8' `8b 88      d8P  Y8 88'  YP
# 8P      88ooo88 88      8P      `8bo.
# 8b      88~~~88 88      8b        `Y8b.
# Y8b  d8 88   88 88booo. Y8b  d8 db   8D
#  `Y88P' YP   YP Y88888P  `Y88P' `8888Y'
print('{:-^100}'.format(' Perform Required calculations ')+'\n')

num_models = 3
model_z = np.linspace(x_lim[0]+0.001, x_lim[1]-0.001, 500)

label_ΩΛ = r'$\Omega_{D.E.}$: %.2f  ;  $\omega_{D.E.}$: %.2f' % (ΩΛ,-1.00)
decl_ΩΛ = decelerate_param(ΩΛ, model_z, w = -1.00)

label_Ω_DE0 = r'$\Omega_{D.E.}$: %.2f  ;  $\omega_{D.E.}$: %.2f'
label_Ω_DE0 = label_Ω_DE0 % (Ω_DE0['Ω_DE'],Ω_DE0['ω_DE'])
decl_Ω_DE0 = decelerate_param(Ω_DE0['Ω_DE'], model_z, w = Ω_DE0['ω_DE'])

label_Ω_DE1 = r'$\Omega_{D.E.}$: %.2f  ;  $\omega_{D.E.}$: %.2f'
label_Ω_DE1 = label_Ω_DE1 % (Ω_DE1['Ω_DE'],Ω_DE1['ω_DE'])
decl_Ω_DE1 = decelerate_param(Ω_DE1['Ω_DE'], model_z, w = Ω_DE1['ω_DE'])

label_ωΩ = r'$\Omega_{D.E.}$: %.2f  ;  $\omega_{D.E.}$: %.2f' % (ωΩ[1],ωΩ[0])
decl_ωΩ = decelerate_param(ωΩ[1], model_z, w = ωΩ[0])

label_allΛ = r'$\Omega_{D.E.}$: %.2f  ;  $\omega_{D.E.}$: %.2f' % (1.00,-1.00)
label_allω = r'$\Omega_{D.E.}$: %.2f  ;  $\omega_{D.E.}$: %.2f' % (1.00, ωΩ[0])
label_noΛ = r'$\Omega_{D.E.}$: %.2f' % (0.00)
decl_allΛ = decelerate_param(1.00, model_z, w = -1.00)
decl_allω = decelerate_param(1.00, model_z, w = ωΩ[0])
decl_noΛ = decelerate_param(0.00, model_z, w = 0.0)



# d8888b. db       .d88b.  d888888b d888888b d888888b d8b   db  d888b
# 88  `8D 88      .8P  Y8. `~~88~~' `~~88~~'   `88'   888o  88 88' Y8b
# 88oodD' 88      88    88    88       88       88    88V8o 88 88
# 88~~~   88      88    88    88       88       88    88 V8o88 88  ooo
# 88      88booo. `8b  d8'    88       88      .88.   88  V888 88. ~8~
# 88      Y88888P  `Y88P'     YP       YP    Y888888P VP   V8P  Y888P
print('{:-^100}'.format(' Setup Top Plot ')+'\n')

### Set Up.
fig = plt.figure(figsize=figsize)
ax = fig.add_subplot(111)  # Add axes on top half of the vertical.
ax.tick_params(axis = 'both',  # Set tick marks inside and outside of x-axis.
                top = True, bottom = True, left = True, right = True,
                direction = 'in', length = 3)
ax.set_xlabel(x_label, labelpad=+4, fontsize=13)
ax.xaxis.set_label_position('bottom')
ax.set_ylabel(y_label, labelpad=+4, fontsize=13)



### Plot.
colours = cmap(np.linspace(0.0, 0.85, num_models))
ax.plot(model_z, decl_ΩΛ, c='blue', label = label_ΩΛ,
        zorder=2, ls=':')
ax.plot([0.652423, 0.652423], [0.0, y_lim[1]], c='blue', ls=':', zorder=1)

ax.plot(model_z, decl_Ω_DE1, c='green', label = label_Ω_DE1,
        zorder=2, ls='-')
ax.plot([0.698713, 0.698713], [0.0, y_lim[1]], c='green', ls='-', zorder=1)

ax.plot(model_z, decl_ωΩ, c='purple', label = label_ωΩ,
        zorder=2, ls='-.')
ax.plot([0.273385, 0.273385], [0.0, y_lim[1]], c='purple', ls='-.', zorder=1)

ax.plot(model_z, decl_allΛ, c='grey', label = label_allΛ,
        zorder=2, ls='--')
ax.plot(model_z, decl_noΛ, c='grey', label = label_noΛ,
        zorder=2, ls='--')

ax.axhline(y=0, c='black', ls=ls['-'], zorder=0)





### Set Axes Limits and Title.
ax.set_xlim(x_lim)
ax.invert_xaxis()

ax.set_ylim(y_lim)
ax.invert_yaxis()

fig.patch.set_alpha(alpha)

# Add Time Scale.
axω_time = ax.twiny()
axω_time.invert_xaxis()
axω_time.set_xlabel(r'Time, Gyr ($\omega_{D.E.} = -2.08$)', labelpad=7,
                    fontsize=13)
axω_time.tick_params('x', colors='black')
axω_time.tick_params(axis='x', direction='out', top = True, bottom = False,
                     labeltop = True, labelbottom = False)
xticks = ax.get_xticks()
axω_time.set_xticks(xticks)
xticks = [time_btwn_z(0.0, i, *ωΩ[::-1])/1e9 for i in xticks]
xticks = ["%.2f" % i for i in xticks]
axω_time.set_xticklabels(xticks)

axΛ_time = ax.twiny()
axΛ_time.invert_xaxis()
axΛ_time.set_xlabel(r'Time, Gyr ($\omega_{\Lambda} = -1.0$)', labelpad=-30,
                    fontsize=13)
axΛ_time.tick_params('x', colors='black')
axΛ_time.tick_params(axis='x', direction='in', top = True, bottom = False,
                     labeltop = True, labelbottom = False, pad=-17)
xticks = ax.get_xticks()
axΛ_time.set_xticks(xticks)
xticks = [time_btwn_z(0.0, i, ΩΛ, -1.0)/1e9 for i in xticks]
xticks = ["%.2f" % i for i in xticks]
xticks[0], xticks[-1] = "", ""
axΛ_time.set_xticklabels(xticks)




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
    fig.savefig(folder_final+'decl_vs_redshift.png', format='png',
                bbox_inches='tight', pad_inches=0, dpi = dpi)
    print('{:-^100}'.format(' Graph Saved ')+'\n')
# plt.show()
print('{:#^100}'.format(' Program Complete '))
