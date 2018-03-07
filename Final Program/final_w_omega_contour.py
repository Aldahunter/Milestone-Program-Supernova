import dill as pickle, numpy as np, matplotlib.pyplot as plt,  matplotlib.cm as cm
from textwrap import wrap
from final_program_imports import *
from matplotlib.ticker import FormatStrFormatter
print('{:#^100}'.format(' Imports Loaded ')+'\n')
folder_final="/media/alex/Shared/University/Physics/Year 3/Physics Problem \
Solving/Computing Project/Programming/Milestone-Program-Supernova/\
Final Program/cont_data/"

## Import Calculated Data
print('{:#^100}'.format(' Import Calculated Data ')+'\n')
calculated_data = pickle.load(open(folder_final[:-10]+"final_data.p", "rb"))
for variable, var_data in calculated_data.items():
    exec(variable + ' = var_data')
print('Imported Variables are:\n  · ', end='')
print(' ; '.join(sorted([i for i in calculated_data]))+'\n')



# d88888b d888888b  d888b        .d8b.  d888888b d888888b d8888b. d8888b.
# 88'       `88'   88' Y8b      d8' `8b `~~88~~' `~~88~~' 88  `8D 88  `8D
# 88ooo      88    88           88ooo88    88       88    88oobY' 88oooY'
# 88~~~      88    88  ooo      88~~~88    88       88    88`8b   88~~~b.
# 88        .88.   88. ~8~      88   88    88       88    88 `88. 88   8D
# YP      Y888888P  Y888P       YP   YP    YP       YP    88   YD Y8888P'
figsize = (6.0, 5.5) #Inches #7,14
thread_calcs = False
load_ωΩ_χmap = 'y'
load_q_map = 'y'
load_age_map = 'y'
x_range = (0.35, 0.75) # Omega_DE.
y_range = (-2.33, -0.95) # w_DE.
cb_range = (-2.5, 0.0)
smx_range = (0.685, 0.715)
smy_range = (-1.02, -0.96)
x_lim = (0.0, 1.0, 1000) # For contour plots.
y_lim = (-2.33, -0.9, 1100) # For contour plots.
dpi = 1000
age_units = "Gyr"
x_label = r"Dark Energy Critical Density Parameter, $\Omega_{D.E.}$"
y_label = r"Dark Energy Equation of State Parameter, $\omega_{D.E.}$"
cb_label = r"Deceleration Parameter, $q$"
chi_contours2D = [0, 2.3, 6.18] # Added onto minimum χ².
q_contours = [-0.7, -0.8, -0.9, -1.0, -1.1, -1.2]
age_contours = np.arange(10.0, 15.5, 0.5)
chi_contours1D = [0, 1.0, 4.00] # Added onto minimum χ².
age_crange = (0.2,0.9)
age_cntrloc = [(0.373782,-2.1),(0.5561,-2.1),(0.640604,-2.1),(0.705052,-2.1)]




# db       .d88b.   .d8b.  d8888b.      d8888b.  .d8b.  d888888b  .d8b.
# 88      .8P  Y8. d8' `8b 88  `8D      88  `8D d8' `8b `~~88~~' d8' `8b
# 88      88    88 88ooo88 88   88      88   88 88ooo88    88    88ooo88
# 88      88    88 88~~~88 88   88      88   88 88~~~88    88    88~~~88
# 88booo. `8b  d8' 88   88 88  .8D      88  .8D 88   88    88    88   88
# Y88888P  `Y88P'  YP   YP Y8888D'      Y8888D' YP   YP    YP    YP   YP
print('{:-^100}'.format(' Loading Data ')+'\n')

## Preliminary Calulations
data = all_data[np.where(all_data['dataset'] != 'Outlier')]
omegas = np.linspace(*x_lim) # X values.
ws = np.linspace(*y_lim) # Y values.
def ωΩ2chi(Ω, ω, z, Lp, obs_data, err_data):
    ωΩ2mag = lambda ωΩ, z, Lp: omega2mag(ωΩ[1], z, Lp, ωΩ[0])
    ωΩ_params, ωΩ2mag_params = (ω, Ω), (z, Lp)
    return minimise_fn(ωΩ_params, ωΩ2mag, ωΩ2mag_params, obs_data, err_data)


## Ask User for Threads (Only need for Calculations)
if thread_calcs == True:
    threads = int(input("How many threads: "))
    n_thread = int(input("Thread numbers (start at 0): "))
    thread = (n_thread, threads)
else: thread = None


## Load/Calc χ² Values
if load_ωΩ_χmap.upper() == 'Y':
    χ_ωΩ = np.loadtxt(folder_final+"w_omega_contour_data(concat_y).txt")
    print('{:~^100}'.format(' χ² Values Loaded ')+'\n')
else:
    from timeit import default_timer as time
    s = time()
    χ_ωΩ = map2D(ωΩ2chi, omegas, ws, thread=thread,
                fn_args=(data['z'], Lp, data['mag'], data['m_err']))
    np.savetxt((folder_final+"w_omega_contour_data_bottom"+
                str(thread)+".txt").replace(' ',''), χ_ωΩ)

    f = time() - s
    hr = int(f/3600)
    mins = int((f-3600*hr)/60)
    sec = int(f-3600*hr - 60*mins)
    print('Time elapsed: {:.0f}hr {:.0f}m {:.0f}s \n'.format(hr, mins, sec))
    print('{:~^100}'.format(' χ² Values Calculated and Saved ')+'\n')


## Load/Calc Deceleration Parameters
if load_q_map.upper() == 'Y':
    qs = np.loadtxt(folder_final+"w_omega_contour_data_q(concat_y).txt")
    print('{:~^100}'.format(' Deceleration Map Loaded ')+'\n')
else:
    from timeit import default_timer as time
    s = time()
    decel_fn = lambda Ω, ω, z : decelerate_param(Ω, z, w=ω)
    qs = map2D(decel_fn, omegas, ws, fn_args=(0.0,), thread=thread)
    np.savetxt((folder_final+"w_omega_contour_data_bottom_q"
                +str(thread)+".txt").replace(' ',''), qs)

    f = time() - s
    hr = int(f/3600)
    mins = int((f-3600*hr)/60)
    sec = int(f-3600*hr - 60*mins)
    print('Time elapsed: {:.0f}hr {:.0f}m {:.0f}s \n'.format(hr, mins, sec))
    print('{:~^100}'.format(' Deceleration Map Calculated and Saved ')+'\n')


## Load/Calc Universe Age Value
if load_age_map.upper() == 'Y':
    ages = np.loadtxt(folder_final+"w_omega_contour_data_age(concat_y).txt")
    print('{:~^100}'.format(' Universe Age Map Loaded ')+'\n')
else:
    from timeit import default_timer as time
    s = time()
    age_fn = lambda Ω, ω: universe_age(Ω, w = ω)
    ages = map2D(age_fn, omegas, ws, thread=thread)
    np.savetxt((folder_final+"w_omega_contour_data_bottom_age"
                +str(thread)+".txt").replace(' ',''), ages)

    f = time() - s
    hr = int(f/3600)
    mins = int((f-3600*hr)/60)
    sec = int(f-3600*hr - 60*mins)
    print('Time elapsed: {:.0f}hr {:.0f}m {:.0f}s \n'.format(hr, mins, sec))
    print('{:~^100}'.format(' Universe Age Map Calculated and Saved ')+'\n')



#  .o88b.  .d8b.  db       .o88b. .d8888.
# d8P  Y8 d8' `8b 88      d8P  Y8 88'  YP
# 8P      88ooo88 88      8P      `8bo.
# 8b      88~~~88 88      8b        `Y8b.
# Y8b  d8 88   88 88booo. Y8b  d8 db   8D
#  `Y88P' YP   YP Y88888P  `Y88P' `8888Y'
print('{:-^100}'.format(' Performing Calculations ')+'\n')

ages = ages / 1e9 #Convert to Gyrs

def argfind_nearest(array, value):
    idx = (np.abs(array-value)).argmin()
    return idx

## Small Plot
smx_argrng = (argfind_nearest(omegas, smx_range[0]),
              argfind_nearest(omegas, smx_range[1])+2)
smy_argrng = (argfind_nearest(ws, smy_range[0]),
              argfind_nearest(ws, smy_range[1])+1)

sm_omegas = omegas[smx_argrng[0] : smx_argrng[1]]
sm_ws = ws[smy_argrng[0] : smy_argrng[1]]

sm_χ = χ_ωΩ[smx_argrng[0] : smx_argrng[1],
            smy_argrng[0] : smy_argrng[1]]

sm_qs = qs[smx_argrng[0] : smx_argrng[1],
           smy_argrng[0] : smy_argrng[1]]
sm_ages = ages[smx_argrng[0] : smx_argrng[1],
               smy_argrng[0] : smy_argrng[1]]


## Large Plot
x_argrng = (argfind_nearest(omegas, x_range[0]),
            argfind_nearest(omegas, x_range[1]))
y_argrng = (argfind_nearest(ws, y_range[0]),
            argfind_nearest(ws, y_range[1]))

omegas = omegas[x_argrng[0] : x_argrng[1]]
ws = ws[y_argrng[0] : y_argrng[1]]

χ_ωΩ = χ_ωΩ[x_argrng[0] : x_argrng[1],
            y_argrng[0] : y_argrng[1]]
qs = qs[x_argrng[0] : x_argrng[1],
        y_argrng[0] : y_argrng[1]]
ages = ages[x_argrng[0] : x_argrng[1],
            y_argrng[0] : y_argrng[1]]

min_chi = χ_ωΩ.min()
minarg = np.where(χ_ωΩ == χ_ωΩ.min())



# d8888b. db       .d88b.  d888888b d888888b d888888b d8b   db  d888b
# 88  `8D 88      .8P  Y8. `~~88~~' `~~88~~'   `88'   888o  88 88' Y8b
# 88oodD' 88      88    88    88       88       88    88V8o 88 88
# 88~~~   88      88    88    88       88       88    88 V8o88 88  ooo
# 88      88booo. `8b  d8'    88       88      .88.   88  V888 88. ~8~
# 88      Y88888P  `Y88P'     YP       YP    Y888888P VP   V8P  Y888P
print('{:-^100}'.format(' Plotting Graph ')+'\n')

def colorbar(mappable):
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    return fig.colorbar(mappable, cax=cax, format="% 4.1f")


## Setup Figure
fig = plt.figure(figsize=figsize)
ax = fig.add_axes([0.05,0.05,0.9,0.9])



## Plot
χ_ωΩ, qs, ages = χ_ωΩ.T, qs.T, ages.T # Flip arrays for matplotlib.

# ,--.  -_ ,. ,-__-.
# |      |_|     |
# |      | |     |
# `--'  `' `' `--'--'
ax.scatter(omegas[minarg[0]], ws[minarg[1]], marker='o',
           color='purple', zorder=4)
chi_contours = [cont + min_chi for cont in chi_contours2D]
chicont = ax.contourf(omegas[::], ws[::], χ_ωΩ, levels=chi_contours,
                      alpha=0.5, zorder=3,
                      colors = cm.Purples(np.linspace(0.3,
                                                      0.7,
                                                      len(chi_contours))))

chi_contours = [cont + chi_ΩΛ * len(data['mag']) for cont in chi_contours1D]
ax.scatter(ΩΛ, -1.0, marker='o', color='blue', zorder=4)
pchicont = ax.contourf(omegas[::], ws[::], χ_ωΩ, levels=chi_contours,
                      colors = cm.Blues(np.linspace(0.0,
                                                    1.0,
                                                    len(chi_contours))),
                      zorder=3, alpha=0.5)


chi_contours = [cont + Ω_DE1['χ²_DE'] * len(data['mag']) for cont in
                chi_contours1D]
ax.scatter(Ω_DE1['Ω_DE'], Ω_DE1['ω_DE'], marker='o', color='green', zorder=4)
chicont = ax.contourf(omegas[::], ws[::], χ_ωΩ, levels=chi_contours,
                      zorder=3, alpha=0.5,
                      colors = cm.Greens(np.linspace(0.0,
                                                      1.0,
                                                      len(chi_contours))))


# ,--.              .
# |   \ ,-. ,-. ,-. |
# |   / |-' |   |-' |
# ^--'  `-' `-' `-' `'
q_cont = ax.imshow(qs,  vmin=cb_range[0], vmax=cb_range[1], cmap=cm.autumn,
                   origin='lower', aspect='auto', zorder=0, extent=[*x_range,
                                                                    *y_range])
q_cb =  colorbar(q_cont)


#    ,.   ,---. .-,--.
#   / |   |  -'  `\__
#  /~~|-. |  ,-'  /
# '   `-' `---|  '`--'
find = lambda l, el_l: sum([[i for i, x in enumerate(l) if x == e]
                            for e in el_l], [])

upage_contours = [i for i in filter(lambda x: x>12, sorted(age_contours))]
upage_pos = find(age_contours, upage_contours)
upage_c = cm.gray(np.linspace(*age_crange, len(age_contours)))[upage_pos]
upage_contrloc = age_cntrloc[2:4]
upagecont = ax.contour(omegas[::], ws[::], ages, levels=upage_contours,
                     linestyles='-', zorder=1, alpha=1.0, colors=upage_c)
ax.clabel(upagecont, inline = True, inline_spacing = 11.0, fmt = "%.1f Gyr",
          fontsize = 10, manual = upage_contrloc)

mdage_contours = [i for i in filter(lambda x: 11<=x<=12, sorted(age_contours))]
mdage_pos = find(age_contours, mdage_contours)
mdage_c = cm.gray(np.linspace(*age_crange, len(age_contours)))[mdage_pos]
mdage_contrloc = [age_cntrloc[1]]
mdagecont = ax.contour(omegas[::], ws[::], ages, levels=mdage_contours,
                     linestyles=':', zorder=1, alpha=1.0, colors=mdage_c)
ax.clabel(mdagecont, inline = True, inline_spacing = 11.0, fmt = "%.1f Gyr",
          fontsize = 10, manual = mdage_contrloc)

loage_contours = [i for i in filter(lambda x: x<11, sorted(age_contours))]
loage_pos = find(age_contours, loage_contours)
loage_c = cm.gray(np.linspace(*age_crange, len(age_contours)))[loage_pos]
loage_contrloc = [age_cntrloc[0]]
loagecont = ax.contour(omegas[::], ws[::], ages, levels=loage_contours,
                     linestyles='--', zorder=1, alpha=1.0, colors=loage_c)
ax.clabel(loagecont, inline = True, inline_spacing = 11.0, fmt = "%.1f Gyr",
          fontsize = 10, manual = loage_contrloc)


# -,--.     .      .
# '|__/ ,-. |- ,-. |-.
# ,|    ,-| |  |   | |
# `'    `-^ `' `-' ' '
χ_ωΩ, qs, ages = χ_ωΩ.T, qs.T, ages.T #Flip arrays back.
pchx_range = (0.3995, 0.5395)
pchy_range = (-1.600, -1.400)
pchx_argrng = (argfind_nearest(omegas, pchx_range[0]),
               argfind_nearest(omegas, pchx_range[1]))
pchy_argrng = (argfind_nearest(ws, pchy_range[0]),
               argfind_nearest(ws, pchy_range[1]))
pch_omegas = omegas[pchx_argrng[0] : pchx_argrng[1]]
pch_ws = ws[pchy_argrng[0] : pchy_argrng[1]]
pch_qs = qs[pchx_argrng[0] : pchx_argrng[1],
            pchy_argrng[0] : pchy_argrng[1]]
χ_ωΩ, qs, ages = χ_ωΩ.T, qs.T, ages.T #Flip arrays back.

ax.imshow(pch_qs.T,  vmin=cb_range[0], vmax=cb_range[1], cmap=cm.autumn,
             origin='lower', aspect='auto', zorder=2, alpha=0.75,
             extent=[*pchx_range, *pchy_range])




χ_ωΩ, qs, ages = χ_ωΩ.T, qs.T, ages.T #Flip arrays back.



## Figure Limits
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.set_xlabel(x_label, fontsize=13) #labelpad=+4,
ax.set_ylabel(y_label, fontsize=13, labelpad=0.0)
ax.yaxis.set_major_formatter(FormatStrFormatter('% 4.1f'))
q_cb.set_label(cb_label, rotation=270, fontsize=13, labelpad=+18)


# .d8888. db    db d8888b.        d8888b. db       .d88b.  d888888b
# 88'  YP 88    88 88  `8D        88  `8D 88      .8P  Y8. `~~88~~'
# `8bo.   88    88 88oooY'        88oodD' 88      88    88    88
#   `Y8b. 88    88 88~~~b. C8888D 88~~~   88      88    88    88
# db   8D 88b  d88 88   8D        88      88booo. `8b  d8'    88
# `8888Y' ~Y8888P' Y8888P'        88      Y88888P  `Y88P'     YP
sm_χ, sm_qs, sm_ages = sm_χ.T, sm_qs.T, sm_ages.T #Flip arrays for pyplot.

sm_ax = fig.add_axes([0.13,0.57,0.35,0.35])

sm_ax.scatter(ΩΛ, -1.0, marker='o', color='blue', zorder=5)
sm_ax.hlines(-1.0, 0.6879195, 0.6977100, colors='blue', linestyles='--',
             zorder=4)
chi_contours = [cont + chi_ΩΛ*len(data['mag']) for cont in chi_contours1D]
sm_ax.contourf(sm_omegas[::], sm_ws[::], sm_χ, levels=chi_contours, zorder=3,
            alpha=0.5, colors = cm.Blues(np.linspace(0.0,
                                                     1.0,
                                                     len(chi_contours))))

sm_ax.scatter(Ω_DE1['Ω_DE'], Ω_DE1['ω_DE'], marker='o', color='green', zorder=5)
sm_ax.vlines(0.71, -1.001387, -0.969, colors='green', linestyles='--', zorder=4)
chi_contours = [cont + Ω_DE1['χ²_DE']*len(data['mag']) for cont in [0, 2.3,
                                                                    4.61]]
sm_ax.contourf(sm_omegas[::], sm_ws[::], sm_χ, levels=chi_contours, zorder=3,
               alpha=0.5, colors = cm.Greens(np.linspace(0.0,
                                                         1.0,
                                                         len(chi_contours))))

sm_ax.imshow(sm_qs,  vmin=cb_range[0], vmax=cb_range[1], cmap=cm.autumn,
             origin='lower', aspect='auto', zorder=0, extent=[*smx_range,
                                                              *smy_range])

sm_χ, sm_qs, sm_ages = sm_χ.T, sm_qs.T, sm_ages.T #Flip arrays back.



## Figure Limits
sm_ax.set_xlim(*smx_range)
sm_ax.set_ylim(*smy_range)
sm_ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
sm_ax.xaxis.set_ticks([0.69, 0.70, 0.71])



# .d8888.  .d8b.  db    db d88888b      dD .d8888. db   db  .d88b.  db   d8b   d
# 88'  YP d8' `8b 88    88 88'         d8' 88'  YP 88   88 .8P  Y8. 88   I8I   8
# `8bo.   88ooo88 Y8    8P 88ooooo    d8'  `8bo.   88ooo88 88    88 88   I8I   8
#   `Y8b. 88~~~88 `8b  d8' 88~~~~~   d8'     `Y8b. 88~~~88 88    88 Y8   I8I   8
# db   8D 88   88  `8bd8'  88.      d8'    db   8D 88   88 `8b  d8' `8b d8'8b d8
# `8888Y' YP   YP    YP    Y88888P C8'     `8888Y' YP   YP  `Y88P'   `8b8' `8d8'
save = 'y'
while save.upper() not in ['Y', 'N']:
    save = input('Would you like to save this graph? (y/n): ')
if save.upper() == 'Y':
    fig.patch.set_alpha(0.0)
    fig.savefig(folder_final[:-10]+'w_vs_omega.png', format='png',
                bbox_inches='tight', pad_inches=0, dpi = dpi)
    fig.patch.set_alpha(1.0)
    print('{:-^100}'.format(' Graph Saved ')+'\n')
# plt.show()
print('{:#^100}'.format(' Program Complete '))
