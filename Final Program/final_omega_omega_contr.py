"""Render Ω_D.E.,(0) vs Ω_M,(0) Contour Plots for Lvl 3 SN Cosmology Report."""
import numpy as np
import dill as pickle
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from textwrap import wrap
from scipy.stats import norm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from final_program_imports import *
print('{:#^100}'.format(' Imports Loaded ')+'\n')

print('{:#^100}'.format(' Import Calculated Data ')+'\n')
folder_final="/media/alex/Shared/University/Physics/Year 3/Physics Problem \
Solving/Computing Project/Programming/Milestone-Program-Supernova/Final \
Program/cont_data/"
calculated_data = pickle.load(open(folder_final[:-10]+"final_data.p", "rb"))
for variable, var_data in calculated_data.items():
    exec(variable + ' = var_data')
print('Imported Variables are:\n  · ', end='')
# Lp; Lp_err; chi_Lp; ωΩ; ωΩ_err; chi_ωΩ; ΩΛ; ΩΛ_err; chi_ΩΛ; Ω_DE0; Ω_DE1.
print(' ; '.join(sorted([i for i in calculated_data]))+'\n')



# d88888b d888888b  d888b        .d8b.  d888888b d888888b d8888b.
# 88'       `88'   88' Y8b      d8' `8b `~~88~~' `~~88~~' 88  `8D
# 88ooo      88    88           88ooo88    88       88    88oobY'
# 88~~~      88    88  ooo      88~~~88    88       88    88`8b
# 88        .88.   88. ~8~      88   88    88       88    88 `88.
# YP      Y888888P  Y888P       YP   YP    YP       YP    88   YD
print('{:-^100}'.format(' Setup Figures and Axes ')+'\n')
load_ω = 'y'
load_Λ = 'y'
load_Ω = 'y'

load_ωq = 'y'
load_Λq = 'y'
load_Ωq = 'y'

load_ωage = 'y'
load_Λage = 'y'
load_Ωage = 'y'

figsize = (14, 5) #Inches
dpi = 1000
x_label = r"Dark Energy Critical Density Parameter, $\Omega_{D.E.}^{(0)}$"
y_label = r"Matter Energy Density Parameter, $\Omega_{M}^{(0)}$"
cb_label =  r"Deceleration Parameter, $q$"
fntsz = 13
cmap = cm.autumn

mapp_definition = 500 # Number of point calulated between x and y limits.
chi_contours2D = [0, 1.0, 4.00, 9.0]
cb_range = (-1.0, -0.4)
age_contours = np.arange(10.0, 15.5, 0.5)
cntr_ls = ['-', ':', '--']
cntr_cmap = cm.gray

ωx_lim = (0.36, 0.48) # (0.35, 0.50)
ωy_lim = (0.52, 0.59) # (0.50, 0.60)

Λx_lim = (0.62, 0.72) # (0.50, 0.75)
Λy_lim = (0.27, 0.36) # (0.25, 0.50)

Ωx_lim = (0.63, 0.73) # (0.50, 0.75)
Ωy_lim = (0.27, 0.36) # (0.25, 0.50)


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



# ,--.  -_ ,. ,-__-.
# |      |_|     |
# |      | |     |
# `--'  `' `' `--'--'
def ΩΩ2chi(Ω_D, Ω_M, w, z, Lp, obs_data, err_data):
    ΩΩ2mag = lambda ΩΩ, w, z, Lp: omega2mag(ΩΩ[0], z, Lp, w=w, om_M0=ΩΩ[1])
    ΩD_ΩM, ΩΩ2mag_params = (Ω_D, Ω_M), (w, z, Lp)
    return minimise_fn(ΩD_ΩM, ΩΩ2mag, ΩΩ2mag_params, obs_data, err_data)

def argfind_nearest(array, value):
    idx = (np.abs(array-value)).argmin()
    return idx

# Optmised ω and Ω Calculations
ω_ΩDs = np.linspace(*ωx_lim, mapp_definition)
ω_ΩMs = np.linspace(*ωy_lim, mapp_definition)
ω_args = (argfind_nearest(ω_ΩDs, ωΩ[1]),
          argfind_nearest(ω_ΩMs, 1.0-ωΩ[1]))

if load_ω.upper() == 'Y':
    ω_χs = np.loadtxt(folder_final+"omega_omega_w_contour_data(HDall_threads).txt")
    print('{:~^100}'.format(' ω χ² Map Loaded ')+'\n')
elif load_ω.upper()== 'N':
    ω_χs = map2D(ΩΩ2chi, ω_ΩDs, ω_ΩMs, fn_args=(ωΩ[0], data['z'], Lp,
                                                data['mag'], data['m_err']))
    np.savetxt(folder_final+"omega_omega_w_contour_data.txt", ω_χs)
    print('{:~^100}'.format(' ω χ² Map Calculated and Saved ')+'\n')

# Constant ω = 1.0 Calculations
Λ_ΩDs = np.linspace(*Λx_lim, mapp_definition)
Λ_ΩMs = np.linspace(*Λy_lim, mapp_definition)
Λ_args = (argfind_nearest(Λ_ΩDs, ΩΛ),
          argfind_nearest(Λ_ΩMs, 1.0-ΩΛ))

if load_Λ.upper() == 'Y':
    Λ_χs = np.loadtxt(folder_final+"omega_omega_L_contour_data(HDall_threads).txt")
    print('{:~^100}'.format(' Λ χ² Map Loaded ')+'\n')
if load_Λ.upper() == 'N':
    Λ_χs = map2D(ΩΩ2chi, Λ_ΩDs, Λ_ΩMs, fn_args=(-1.0, data['z'], Lp,
                                                data['mag'], data['m_err']))
    np.savetxt(folder_final+"omega_omega_L_contour_data.txt", Λ_χs)
    print('{:~^100}'.format(' Λ χ² Map Calculated and Saved ')+'\n')

# Constant Ω = 0.71 Calculations
Ω_ΩDs = np.linspace(*Ωx_lim, mapp_definition)
Ω_ΩMs = np.linspace(*Ωy_lim, mapp_definition)
Ω_args = (argfind_nearest(Ω_ΩDs, Ω_DE1['Ω_DE']),
          argfind_nearest(Ω_ΩMs, 1.0-Ω_DE1['Ω_DE']))

if load_Ω.upper() == 'Y':
    Ω_χs = np.loadtxt(folder_final+"omega_omega_O_contour_data(HDall_threads).txt")
    print('{:~^100}'.format(' Ω χ² Map Loaded ')+'\n')
if load_Ω.upper() == 'N':
    Ω_χs = map2D(ΩΩ2chi, Ω_ΩDs, Ω_ΩMs, fn_args=(Ω_DE1['ω_DE'], data['z'], Lp,
                                                data['mag'], data['m_err']))
    np.savetxt(folder_final+"omega_omega_O_contour_data.txt", Ω_χs)
    print('{:~^100}'.format(' Ω χ² Map Calculated and Saved ')+'\n')


# ,--.              .
# |   \ ,-. ,-. ,-. |
# |   / |-' |   |-' |
# ^--'  `-' `-' `-' `'
decel_fn = lambda ΩD, ΩM, ω, z : decelerate_param(ΩD, z, w=ω, om_M0=ΩM)

if load_ωq.upper() == 'Y':
    ω_qs = np.loadtxt(folder_final+"omega_omega_w_qcontour(HDall_threads).txt")
    print('{:~^100}'.format(' ω Deceleration Map Loaded ')+'\n')
elif load_ωq.upper()== 'N':
    ω_qs = map2D(decel_fn, ω_ΩDs, ω_ΩMs, fn_args=(ωΩ[0], 0.0))
    np.savetxt(folder_final+"omega_omega_w_qcontour.txt", ω_qs)
    print('{:~^100}'.format(' ω Deceleration Map Calculated and Saved ')+'\n')

if load_Λq.upper() == 'Y':
    Λ_qs = np.loadtxt(folder_final+"omega_omega_L_qcontour(HDall_threads).txt")
    print('{:~^100}'.format(' Λ Deceleration Map Loaded ')+'\n')
elif load_Λq.upper()== 'N':
    Λ_qs = map2D(decel_fn, Λ_ΩDs, Λ_ΩMs, fn_args=(-1.0, 0.0))
    np.savetxt(folder_final+"omega_omega_L_qcontour.txt", Λ_qs)
    print('{:~^100}'.format(' Λ Deceleration Map Calculated and Saved ')+'\n')

if load_Ωq.upper() == 'Y':
    Ω_qs = np.loadtxt(folder_final+"omega_omega_O_qcontour(HDall_threads).txt")
    print('{:~^100}'.format(' Ω Deceleration Map Loaded ')+'\n')
elif load_Ωq.upper()== 'N':
    Ω_qs = map2D(decel_fn, Ω_ΩDs, Ω_ΩMs, fn_args=(Ω_DE1['ω_DE'], 0.0))
    np.savetxt(folder_final+"omega_omega_O_qcontour.txt", Ω_qs)
    print('{:~^100}'.format(' Ω Deceleration Map Calculated and Saved ')+'\n')


#    ,.   ,---. .-,--.
#   / |   |  -'  `\__
#  /~~|-. |  ,-'  /
# '   `-' `---|  '`--'
age_fn = lambda ΩD, ΩM, ω: universe_age(ΩD, w = ω, om_M0 = ΩM)

if load_ωage.upper() == 'Y':
    ω_ages = np.loadtxt(folder_final+"omega_omega_w_agecontour(HDall_threads).txt")
    print('{:~^100}'.format(' ω Age Map Loaded ')+'\n')
elif load_ωage.upper()== 'N':
    ω_ages = map2D(age_fn, ω_ΩDs, ω_ΩMs, fn_args=(ωΩ[0],))
    np.savetxt(folder_final+"omega_omega_w_agecontour.txt", ω_ages)
    print('{:~^100}'.format(' ω Age Map Calculated and Saved ')+'\n')

if load_Λage.upper() == 'Y':
    Λ_ages = np.loadtxt(folder_final+"omega_omega_L_agecontour(HDall_threads).txt")
    print('{:~^100}'.format(' Λ Age Map Loaded ')+'\n')
elif load_Λage.upper()== 'N':
    Λ_ages = map2D(age_fn, Λ_ΩDs, Λ_ΩMs, fn_args=(-1.0,))
    np.savetxt(folder_final+"omega_omega_L_agecontour.txt", Λ_ages)
    print('{:~^100}'.format(' Λ Age Map Calculated and Saved ')+'\n')

if load_Ωage.upper() == 'Y':
    Ω_ages = np.loadtxt(folder_final+"omega_omega_O_agecontour(HDall_threads).txt")
    print('{:~^100}'.format(' Ω Age Map Loaded ')+'\n')
elif load_Ωage.upper()== 'N':
    Ω_ages = map2D(age_fn, Ω_ΩDs, Ω_ΩMs, fn_args=(Ω_DE1['ω_DE'],))
    np.savetxt(folder_final+"omega_omega_O_agecontour.txt", Ω_ages)
    print('{:~^100}'.format(' Ω Age Map Calculated and Saved ')+'\n')

ω_ages = ω_ages / 1e9 # Convert yrs to Gyrs.
Λ_ages = Λ_ages / 1e9
Ω_ages = Ω_ages / 1e9



# d8888b. db       .d88b.  d888888b d888888b d888888b d8b   db  d888b
# 88  `8D 88      .8P  Y8. `~~88~~' `~~88~~'   `88'   888o  88 88' Y8b
# 88oodD' 88      88    88    88       88       88    88V8o 88 88
# 88      88      88    88    88       88       88    88 V8o88 88  ooo
# 88      88booo. `8b  d8'    88       88      .88.   88  V888 88.  8
# 88      Y88888P  `Y88P'     YP       YP    Y888888P VP   V8P  Y888P
print('{:-^100}'.format(' Setup Up Figure ')+'\n')

### Set Up.
fig = plt.figure(figsize=figsize)
ωax = fig.add_axes([0.05, 0.05, 0.265, 0.90])  # Add axes for ω cont plot.
Λax = fig.add_axes([0.35, 0.05, 0.265, 0.90])  # Add axes for Λ cont plot.
Ωax = fig.add_axes([0.65, 0.05, 0.265, 0.90])  # Add axes for Ω cont plot.

# ,--.  -_ ,. ,-__-.
# |      |_|     |
# |      | |     |
# `--'  `' `' `--'--'
ωax.scatter(ω_ΩDs[ω_args[0]], ω_ΩMs[ω_args[1]],
            marker='o', color='purple', zorder=4)
ω_levels = [cont + ω_χs[ω_args[0], ω_args[1]] for cont in chi_contours2D]
ω_contrs = ωax.contourf(ω_ΩDs, ω_ΩMs, ω_χs.T,
                        alpha=0.5, zorder=3, levels=ω_levels,
                        colors = cm.Purples(np.linspace(0.3, 0.7,
                                                        len(ω_levels))))

Λax.scatter(Λ_ΩDs[Λ_args[0]], Λ_ΩMs[Λ_args[1]],
            marker='o', color='blue', zorder=4)
Λ_levels = [cont + Λ_χs[Λ_args[0],Λ_args[1]] for cont in chi_contours2D]
Λ_contrs = Λax.contourf(Λ_ΩDs, Λ_ΩMs, Λ_χs.T,
                        alpha=0.5, zorder=3, levels=Λ_levels,
                        colors = cm.Blues(np.linspace(0.3, 0.7,
                                                        len(Λ_levels))))

Ωax.scatter(Ω_ΩDs[Ω_args[0]], Ω_ΩMs[Ω_args[1]],
            marker='o', color='green', zorder=4)
Ω_levels = [cont + Ω_χs[Ω_args[0],Ω_args[1]] for cont in chi_contours2D]
Ω_contrs = Ωax.contourf(Ω_ΩDs, Ω_ΩMs, Ω_χs.T,
                        alpha=0.5, zorder=3, levels=Ω_levels,
                        colors = cm.Greens(np.linspace(0.3, 0.7,
                                                        len(Ω_levels))))


# ,--- .      .    .  .     @        |   @
# |__  |  ,-. |-   |  | .-. . .  ,   |   . ,-. ,-.
# |    |  ,-| |    |  | | | | | /    |   | | | |-'
# '    `- `-^ `'   `--' ' ' ' `'     `-- ' ' ' `-'
ωax.plot(np.array(ωx_lim), 1.0-np.array(ωx_lim), c='black', ls='--', zorder=1)
Λax.plot(np.array(Λx_lim), 1.0-np.array(Λx_lim), c='black', ls='--', zorder=1)
Ωax.plot(np.array(Ωx_lim), 1.0-np.array(Ωx_lim), c='black', ls='--', zorder=1)


# ,--.                   |   @
# \__  ,-. ,-. ,-. ,-.   |   . ,-. ,-.
# /    |   |   | | |     |   | | | |-'
# `--' '   '   `-' '     `-- ' ' ' `-'
# ωx_lerr = [(0.459946, 0.459946), (ωy_lim[0], 0.540054)] # lower error
# ωx_uerr = [(0.466044, 0.466044), (ωy_lim[0], 0.533956)] # upper error
# ωy_uerr = [(ωx_lim[0], 0.459946), (0.540054, 0.540054)] # upper error
# ωy_lerr = [(ωx_lim[0], 0.466044), (0.533956, 0.533956)] # lower error
#
# ωax.plot(ωx_uerr[0], ωx_uerr[1], c='purple', ls=':', zorder=1)
# ωax.plot(ωx_lerr[0], ωx_lerr[1], c='purple', ls=':', zorder=1)
# ωax.plot(ωy_uerr[0], ωy_uerr[1], c='purple', ls=':', zorder=1)
# ωax.plot(ωy_lerr[0], ωy_lerr[1], c='purple', ls=':', zorder=1)
#
#
# Λx_lerr = [(0.686226, 0.686226), (Λy_lim[0], 0.313774)] # lower error
# Λx_uerr = [(0.699389, 0.699389), (Λy_lim[0], 0.300611)] # upper error
# Λy_uerr = [(Λx_lim[0], 0.686226), (0.313774, 0.313774)] # upper error
# Λy_lerr = [(Λx_lim[0], 0.699389), (0.300611, 0.300611)] # lower error
#
# Λax.plot(Λx_lerr[0], Λx_lerr[1], c='blue', ls=':', zorder=1)
# Λax.plot(Λx_uerr[0], Λx_uerr[1], c='blue', ls=':', zorder=1)
# Λax.plot(Λy_uerr[0], Λy_uerr[1], c='blue', ls=':', zorder=1)
# Λax.plot(Λy_lerr[0], Λy_lerr[1], c='blue', ls=':', zorder=1)
#
#
# Ωx_lerr = [(0.687555, 0.687555), (Ωy_lim[0], 0.312445)] # lower error
# Ωx_uerr = [(0.710902, 0.710902), (Ωy_lim[0], 0.289098)] # upper error
# Ωy_uerr = [(Ωx_lim[0], 0.687555), (0.312445, 0.312445)] # upper error
# Ωy_lerr = [(Ωx_lim[0], 0.710902), (0.289098, 0.289098)] # lower error
#
# Ωax.plot(Ωx_lerr[0], Ωx_lerr[1], c='green', ls=':', zorder=1)
# Ωax.plot(Ωx_uerr[0], Ωx_uerr[1], c='green', ls=':', zorder=1)
# Ωax.plot(Ωy_uerr[0], Ωy_uerr[1], c='green', ls=':', zorder=1)
# Ωax.plot(Ωy_lerr[0], Ωy_lerr[1], c='green', ls=':', zorder=1)


# ,--.              .
# |   \ ,-. ,-. ,-. |
# |   / |-' |   |-' |
# ^--'  `-' `-' `-' `'
ωim = ωax.imshow(ω_qs.T, cmap=cmap, vmin=cb_range[0], vmax=cb_range[1],
                 origin='lower', aspect='auto', zorder=0, extent=[*ωx_lim,
                                                                  *ωy_lim])

Λim = Λax.imshow(Λ_qs.T, cmap=cmap, vmin=cb_range[0], vmax=cb_range[1],
                 origin='lower', aspect='auto', zorder=0, extent=[*Λx_lim,
                                                                  *Λy_lim])

Ωim = Ωax.imshow(Ω_qs.T, cmap=cmap, vmin=cb_range[0], vmax=cb_range[1],
                 origin='lower', aspect='auto', zorder=0, extent=[*Ωx_lim,
                                                                  *Ωy_lim])
# Add Colour Bar.
divider = make_axes_locatable(Ωax)
cax = divider.append_axes("right", size="5%", pad=0.05)
q_cb = fig.colorbar(Ωim, cax=cax, format="% 4.1f")


#    ,.   ,---. .-,--.
#   / |   |  -'  `\__
#  /~~|-. |  ,-'  /
# '   `-' `---|  '`--'
def plot_age_contours(axes, ages, Ωxs, Ωys, cntr_lvls, ineqs, cntrlocs,
                      ls,  cmap, fntsz, clr_rng = (0.1, 0.5), zord = 1,
                      fmt = " %.1f Gyr ", label_spc = 15.0):
    flatten = lambda l: [item for sublist in l for item in sublist]
    find = lambda l, el_l: sum([[i for i, x in enumerate(l) if x == e]
                                for e in el_l], [])
    cntrs = []
    clrs = cmap(np.linspace(*clr_rng, len(flatten(cntrlocs))))
    clrs = iter(clrs)
    for n, ineq in enumerate(ineqs):
        lvls = [i for i in filter(ineq, sorted(cntr_lvls))]
        c = [next(clrs) for i in cntrlocs[n]][::-1]
        if len(c) == 0: c = [(0,0,0,0),]
        locns = cntrlocs[n]
        cntrs.append(axes.contour(Ωxs, Ωys, ages, levels=lvls, linestyles=ls[n],
                                  zorder=zord, alpha=1.0, colors=c))
        axes.clabel(cntrs[n], inline = True, inlinespacing = label_spc,
                    fmt = fmt, fontsize=fntsz, manual=locns)

ineqs = (lambda x: x>12, lambda x: 11<=x<=12, lambda x: x<11)

cntr_lvls = np.arange(10, 11.4, 0.25)
ω_cntrlocs = [[], # Old Contour labael positons (contr > 12 Gyr).
              [(0.385,0.5375), (0.4165,0.5625)], # Mid Cntr (11 >= cntr >= 12 Gyr).
              [(0.46,0.585),]] # Low Contour label positions (contr < 11 Gyr).

plot_age_contours(ωax, ω_ages.T, ω_ΩDs, ω_ΩMs, cntr_lvls, ineqs, ω_cntrlocs,
                  cntr_ls,  cntr_cmap, fntsz, fmt = " %.2f Gyr ")

cntr_lvls = np.arange(11, 13.1, 0.5)
Λ_cntrlocs = [[(0.645, 0.2875), (0.645, 0.32)], # Old Contr (contr > 12 Gyr).
              [(0.70, 0.3475),], # Mid Cntr (11 >= cntr >= 12 Gyr).
              []] # Low Contour label positions (contr < 11 Gyr).
plot_age_contours(Λax, Λ_ages.T, Λ_ΩDs, Λ_ΩMs, cntr_lvls, ineqs, Λ_cntrlocs,
                  cntr_ls, cntr_cmap, fntsz)

Ω_cntrlocs = [[(0.6475, 0.285), (0.6475, 0.3175)], # Old Contr (contr > 12 Gyr).
              [(0.71, 0.3475),], # Mid Cntr (11 >= cntr >= 12 Gyr).
              []] # Low Contour label positions (contr < 11 Gyr).
plot_age_contours(Ωax, Ω_ages.T, Ω_ΩDs, Ω_ΩMs, cntr_lvls, ineqs, Ω_cntrlocs,
                  cntr_ls, cntr_cmap, fntsz)


# Set Avis Limits.
ωax.set_xlim(*ωx_lim)
ωax.set_ylim(*ωy_lim)
ωax.set_xticklabels(['0.36', '0.38', '0.40', '0.42', '0.44', '0.46', ''])

Λax.set_xlim(*Λx_lim)
Λax.set_ylim(*Λy_lim)
Λax.set_xticklabels(['0.62', '0.64', '0.66', '0.68', '0.70', ''])

Ωax.set_xlim(*Ωx_lim)
Ωax.set_ylim(*Ωy_lim)
Ωax.set_xticks([0.63, 0.65, 0.67, 0.69, 0.71, 0.73])
Ωax.set_xticklabels(['0.63', '0.65', '0.67', '0.69', '0.71', ''])

q_cb.set_label(cb_label, rotation=270, fontsize=fntsz+5, labelpad=+18)
fig.text(0.5, -0.06, x_label, ha='center', fontsize=fntsz+5)
fig.text(-0.01, 0.5, y_label, va='center', rotation='vertical',
         fontsize=fntsz+5)


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
    fig.patch.set_alpha(0.0)
    fig.savefig(folder_final[:-10]+'omega_vs_omega.png', format='png',
                bbox_inches='tight', pad_inches=0, dpi = dpi)
    fig.patch.set_alpha(1.0)
    print('{:-^100}'.format(' Graph Saved ')+'\n')
# plt.show()
print('{:#^100}'.format(' Program Complete '))
