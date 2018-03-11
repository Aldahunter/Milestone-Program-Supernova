folder_final="/media/alex/Shared/University/Physics/Year 3/Physics Problem Solving/Computing Project/Programming/Milestone-Program-Supernova/Final Program/"
import dill as pickle, numpy as np, matplotlib.pyplot as plt, matplotlib.cm as cm
from textwrap import wrap
from scipy.stats import norm
from final_program_imports import *
print('{:#^100}'.format(' Imports Loaded ')+'\n')

# Import Calculated Data #
print('{:#^100}'.format(' Import Calculated Data ')+'\n')
calculated_data = pickle.load(open(folder_final+"final_data.p", "rb"))
for variable, var_data in calculated_data.items():
    exec(variable + ' = var_data')
print('Imported Variables are:\n  · ', end='')
print(' ; '.join(sorted([i for i in calculated_data]))+'\n')



# d88888b d888888b  d888b        .d8b.  d888888b d888888b d8888b. d8888b.
# 88'       `88'   88' Y8b      d8   8b `~~88~~' `~~88~~' 88  `8D 88  `8D
# 88ooo      88    88           88ooo88    88       88    88oobY' 88oobY'
# 88~~~      88    88  ooo      88   88    88       88    88`8b   88`8b
# 88        .88.   88. ~8~      88   88    88       88    88 `88. 88 `88.
# YP      Y888888P  Y888P       YP   YP    YP       YP    88   YD 88   YD
print('{:-^100}'.format(' Setup Figures and Axes ')+'\n')
figsize = (9,7) #Inches
y_lim = (0.0, 1.43)
x_lim = (-20,25)
y_lim_occ = (0,70)
dpi = 1000
bin_width = 1.0
y_label = r'Redshift, $z$'
x_label = r'Normalised Residual'
y_label_occ = r'Occurrence'
alpha = 0.0
ls = {'-':(0, ()), '..':(0, (1, 5)), ':':(0, (1, 1)), '--':(0, (5, 5)),
      '-.':(0, (3, 5, 1, 5)), '-..':(0, (3, 4, 1, 4, 1, 4))}
markers = ['o', '^', '1', 'p', 's', '*', '+', 'x', 'd', r'$\ast $']
datasets = ['CfA', 'CSP', 'SCP', 'SNLS', 'C/TSS', 'SDSS II', 'Essence',
            'HST CSS', 'High-Z SS', 'HST Riess']



#  .o88b.  .d8b.  db       .o88b. .d8888.
# d8P  Y8 d8' `8b 88      d8P  Y8 88'  YP
# 8P      88ooo88 88      8P      `8bo.
# 8b      88~~~88 88      8b        `Y8b.
# Y8b  d8 88   88 88booo. Y8b  d8 db   8D
#  `Y88P' YP   YP Y88888P  `Y88P' `8888Y'
print('{:-^100}'.format(' Perform Required calculations ')+'\n')

model_z = np.linspace(y_lim[0]+0.001, y_lim[1]-0.001, 400)

def calc_lag(Ω, ω):
    datasets_norm_res, all_norm_res = {}, []
    for dataset in datasets:
        dataset_arr = all_data[np.where(all_data['dataset'] == dataset)]
        dataset_residual = dataset_arr['mag'] - omega2mag(Ω, dataset_arr['z'],
                                                          Lp, w = ω)
        datasets_norm_res[dataset] = dataset_residual / dataset_arr['m_err']
        all_norm_res = np.concatenate((all_norm_res,
                                       datasets_norm_res[dataset]))
    return datasets_norm_res, all_norm_res

def calc_occur(all_norm_res):
    diff = lambda a, b: b-a
    occ_bins = np.linspace(*x_lim, 1+float(diff(*x_lim))/float(bin_width))

    bin_values = np.empty(len(occ_bins[:-1]))
    widths = np.empty(len(occ_bins[:-1]))
    for n, n_bin in enumerate(occ_bins[:-1]):
        low, upp = n_bin, occ_bins[n+1]
        widths[n] = upp - low
        bin_values[n] = all_norm_res[(low<all_norm_res)*(all_norm_res<upp)].size

    norm_y = np.linspace(*x_lim, 500)
    norm_x = norm.pdf(norm_y, all_norm_res.mean(), all_norm_res.std())
    norm_scale = all_norm_res.size*bin_width

    return occ_bins, bin_values, widths, norm_y, norm_x, norm_scale



# d8888b. db       .d88b.  d888888b d888888b d888888b d8b   db  d888b
# 88  `8D 88      .8P  Y8. `~~88~~' `~~88~~'   `88'   888o  88 88' Y8b
# 88oodD' 88      88    88    88       88       88    88V8o 88 88
# 88~~~   88      88    88    88       88       88    88 V8o88 88  ooo
# 88      88booo. `8b  d8'    88       88      .88.   88  V888 88. ~8~
# 88      Y88888P  `Y88P'     YP       YP    Y888888P VP   V8P  Y888P
print('{:-^100}'.format(' Setup Figure & Axes ')+'\n')

fig = plt.figure(figsize=figsize)
ax1 = fig.add_axes([0.05,0.29,43/150,0.66])                # ω Lag Residual.
ax2 = fig.add_axes([0.05,0.05,43/150,0.22], sharex = ax1)  # ω Occurence.

ax3 = fig.add_axes([107/300,0.29,43/150,0.66], sharex = ax1, sharey = ax1)
ax4 = fig.add_axes([107/300,0.05,43/150,0.22], sharex = ax1, sharey = ax2)

ax5 = fig.add_axes([199/300,0.29,43/150,0.66], sharex = ax1, sharey = ax1)
ax6 = fig.add_axes([199/300,0.05,43/150,0.22], sharex = ax1, sharey = ax2)

axes = [ax1, ax2, ax3, ax4, ax5, ax6]
for ax in axes:
    ax.tick_params(axis = 'both',  # Set tick marks inside and outside of x-axis.
                    top = True, bottom = True, left = True, right = True,
                    direction = 'in', length = 3)

plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax3.get_xticklabels(), visible=False)
plt.setp(ax5.get_xticklabels(), visible=False)

plt.setp(ax3.get_yticklabels(), visible=False)
plt.setp(ax4.get_yticklabels(), visible=False)
plt.setp(ax5.get_yticklabels(), visible=False)
plt.setp(ax6.get_yticklabels(), visible=False)

## Plot Function ##
def plot_lag(ax, datasets_norm_res):
    ax.axvline(x=0, c='black', ls=ls['-'], zorder=3)
    ax.plot(np.ones(model_z.shape),  model_z, ls=ls['--'], c='grey', zorder=2)
    ax.plot(-np.ones(model_z.shape), model_z, ls=ls['--'], c='grey', zorder=2)
    ax.fill_betweenx(model_z, np.ones(model_z.shape), -np.ones(model_z.shape),
                     zorder=1, color=(0.82,0.82,0.82,1), alpha=0.4)
    ds_colours = cm.rainbow(np.linspace(0, 1, len(datasets)))
    colours = iter(ds_colours)
    dataset_markers = iter(markers)
    for dataset in datasets:
        dataset_arr = all_data[np.where(all_data['dataset'] == dataset)]
        colour, marker = next(colours), next(dataset_markers)
        ax.scatter(datasets_norm_res[dataset], dataset_arr['z'],
                    c=colour, marker=marker, zorder=0)

def plot_occur(ax, occ_bins, bin_values, widths, norm_y, norm_x, norm_scale):
    ax.axvline(x=0, c='black', ls=ls['-'], zorder=3)
    ax.plot(np.ones(len(y_lim_occ)),  y_lim_occ, ls=ls['--'], c='grey', zorder=2)
    ax.plot(-np.ones(len(y_lim_occ)), y_lim_occ, ls=ls['--'], c='grey', zorder=2)
    ax.fill_betweenx(y_lim_occ, np.ones(len(y_lim_occ)), -np.ones(len(y_lim_occ)),
                     zorder=1, color=(0.82,0.82,0.82,1), alpha=0.4)
    color = cm.rainbow(np.linspace(0, 1, len(datasets)))[7]
    ax.bar(occ_bins[:-1], bin_values, widths, align='edge', facecolor=color,
             edgecolor='black', zorder=0)
    ax.plot(norm_y, norm_scale*norm_x, ls=ls['--'], c='red', zorder=3)


## Plot Lag and Occurence Plots ##
plt_d = {'ω': [ax1, ax2, (ωΩ[1], ωΩ[0])],
         'Λ': [ax3, ax4, (ΩΛ, -1.0)],
         'Ω': [ax5, ax6, (Ω_DE1['Ω_DE'], Ω_DE1['ω_DE'])]}

for plt in plt_d:
    print('{:-^100}'.format(' Setup '+plt+' Plots ')+'\n')
    ds_normres, all_normres = calc_lag(*plt_d[plt][2])
    occur_data = calc_occur(all_normres)
    plot_lag(plt_d[plt][0], ds_normres)
    plot_occur(plt_d[plt][1], *occur_data)


## Text ##
fig.text(0.055,0.9200,'(a)', fontsize=15)
fig.text(0.363,0.9200,'(b)', fontsize=15)
fig.text(0.671,0.9200,'(c)', fontsize=15)
# fig.text(0.760,0.21,'(d)',fontsize=15)


## Set Axes Limits and Title ##
ax1.set_xlim(x_lim)
ax1.set_ylim(y_lim)
ax2.set_ylim(y_lim_occ)

ax1.set_ylabel(y_label, fontsize=13)#, labelpad=+4)
ax2.set_ylabel(y_label_occ, fontsize=13)#, labelpad=+4)
fig.text(0.5, -0.00, x_label, ha='center', fontsize=13)



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
    fig.patch.set_alpha(alpha)
    fig.savefig(folder_final+'lag_plots.png', format='png',
                bbox_inches='tight', pad_inches=0, dpi = dpi)
    fig.patch.set_alpha(1.00)
    print('{:-^100}'.format(' Graph Saved ')+'\n')
# plt.show()
print('{:#^100}'.format(' Program Complete '))
