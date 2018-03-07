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



### Figure & Axis Attributes ###
print('{:-^100}'.format(' Setup Figures and Axes ')+'\n')
figsize = (7,12) #Inches
x_lim = (0.0, 1.43)
y_lim = (14, 27.0)
y_lim_res = (-20,25)
x_lim_occ = (0,60)
dpi = 1000
bin_width = 1.0
x_label = r'Redshift, $z$'
y_label = r'Effective Magnitude, $m_{eff}$'
y_label_res = r'Norm. Residual'
x_label_occ = r'Occurrence'
alpha = 0.0
ls = {'-':(0, ()), '..':(0, (1, 5)), ':':(0, (1, 1)), '--':(0, (5, 5)),
      '-.':(0, (3, 5, 1, 5)), '-..':(0, (3, 4, 1, 4, 1, 4))}
markers = ['o', '^', '1', 'p', 's', '*', '+', 'x', 'd', r'$\ast $']



### Calculations ###
print('{:-^100}'.format(' Perform Required calculations ')+'\n')

## Top Plot ##
num_models = 6
model_z = np.linspace(x_lim[0]+0.001, x_lim[1]-0.001, 400)
label_ΩΛ = (r'$\Omega_{D.E.}$: %.2f  ;  $\omega_{D.E.}$: %.2f'
            % (ΩΛ,-1.00))
model_ΩΛ = omega2mag(ΩΛ, model_z, Lp, w = -1, R = R_0, om_M0 = 'flat')
label_Ω_DE0 = (r'$\Omega_{D.E.}$: %.2f  ;  $\omega_{D.E.}$: %.2f'
               % (Ω_DE0['Ω_DE'],Ω_DE0['ω_DE']))
model_Ω_DE0 = omega2mag(Ω_DE0['Ω_DE'], model_z, Lp, w = Ω_DE0['ω_DE'])
label_Ω_DE1 = (r'$\Omega_{D.E.}$: %.2f  ;  $\omega_{D.E.}$: %.2f'
               % (Ω_DE1['Ω_DE'],Ω_DE1['ω_DE']))
model_Ω_DE1 = omega2mag(Ω_DE1['Ω_DE'], model_z, Lp, w = Ω_DE1['ω_DE'])
label_ωΩ = (r'$\Omega_{D.E.}$: %.2f  ;  $\omega_{D.E.}$: %.2f'
            % (ωΩ[1],ωΩ[0]))
model_ωΩ = omega2mag(ωΩ[1], model_z, Lp, w = ωΩ[0])
label_allΛ = (r'$\Omega_{D.E.}$: %.2f  ;  $\omega_{D.E.}$: %.2f'
             % (1.00,-1.00))
model_allΛ = omega2mag(1.00, model_z, Lp, w = -1.00)
label_noΛ = (r'$\Omega_{D.E.}$: %.2f  ;  $\omega_{D.E.}$: %.2f'
             % (0.00,-1.00))
model_noΛ = omega2mag(0.00, model_z, Lp, w = -1.00)


## Middle Plot ##
def model_err(model_bf, Ω, Ω_err, Lp, Lp_err, ω, ω_err):
    model_Ωerr = omega2mag(Ω + Ω_err, model_z, Lp, w = ω) - model_bf
    model_Lperr = omega2mag(Ω, model_z, Lp + Lp_err, w = ω) - model_bf
    model_ωerr = omega2mag(Ω, model_z, Lp, w = ω + ω_err) - model_bf
    return (model_Ωerr**2 + model_Lperr**2 + model_ωerr**2)**0.5
model_allω = omega2mag(1.00, model_z, Lp, w = ωΩ[0])
model_noω = omega2mag(0.00, model_z, Lp, w = ωΩ[0])
model_ωΩ_err = model_err(model_ωΩ, ωΩ[1], ωΩ_err[1], Lp, Lp_err, ωΩ[0], ωΩ_err[0])
model_ub = model_ωΩ + model_ωΩ_err
model_lb = model_ωΩ - model_ωΩ_err
no_outliers = set(all_data['dataset'])
no_outliers.remove('Outlier')
datasets = sorted(no_outliers, key=len)
outliers_arr = all_data[np.where(all_data['dataset'] == 'Outlier')]


## Residual Plot ##
datasets_norm_res, all_norm_res = {}, []
for dataset in datasets:
    dataset_arr = all_data[np.where(all_data['dataset'] == dataset)]
    dataset_residual = dataset_arr['mag'] - omega2mag(ωΩ[1], dataset_arr['z'],
                                                      Lp, w = ωΩ[0])
    datasets_norm_res[dataset] = dataset_residual / dataset_arr['m_err']
    all_norm_res = np.concatenate((all_norm_res, datasets_norm_res[dataset]))
outliers_norm_res = outliers_arr['mag'] - omega2mag(ωΩ[1], outliers_arr['z'],
                                                    Lp, w = ωΩ[0])
outliers_norm_res = outliers_norm_res / outliers_arr['m_err']

# Occurence Plot #
diff = lambda a, b: b-a
occ_bins = np.linspace(*y_lim_res, 1+float(diff(*y_lim_res))/float(bin_width))
bin_values = np.empty(len(occ_bins[:-1]))
widths = np.empty(len(occ_bins[:-1]))
for n, n_bin in enumerate(occ_bins[:-1]):
    low, upp = n_bin, occ_bins[n+1]
    widths[n] = upp - low
    bin_values[n] = all_norm_res[(low<all_norm_res)*(all_norm_res<upp)].size
norm_y = np.linspace(*y_lim_res, 500)
norm_x = norm.pdf(norm_y, all_norm_res.mean(), all_norm_res.std())
norm_scale = all_norm_res.size*bin_width



### Plot Graph ###
fig = plt.figure(figsize=figsize)
ax1 = fig.add_axes([0.05,0.59,0.69,0.36])  # Add axes on top half of the vertical.
ax2 = fig.add_axes([0.05,0.23,0.69,0.36], sharex = ax1, sharey = ax1)
ax3 = fig.add_axes([0.05,0.05,0.69,0.18], sharex = ax1)
ax4 = fig.add_axes([0.75,0.05,0.21,0.18], sharey = ax3)
fig.text(0.075,0.9275,'(a)',fontsize=15)
fig.text(0.075,0.57,'(b)',fontsize=15)
fig.text(0.057,0.21,'(c)',fontsize=15)
fig.text(0.760,0.21,'(d)',fontsize=15)


## Top Plot ##
print('{:-^100}'.format(' Setup Top Plot ')+'\n')
ax1.xaxis.tick_top()
ax1.tick_params(axis = 'both',  # Set tick marks inside and outside of x-axis.
                top = True, bottom = True, left = True, right = True,
                direction = 'in', length = 3)
ax1.set_xlabel(x_label, labelpad=+4, fontsize=13)
ax1.xaxis.set_label_position('top')
ax1.set_ylabel(y_label, labelpad=+6, fontsize=13)

colours = iter(cm.prism(np.linspace(0, 1, num_models)))
ax1.errorbar(all_data['z'], all_data['mag'], yerr=all_data['m_err'],
             ls='', marker='+', capsize=1.25, c='black', zorder=0)
ax1.plot(model_z, model_noΛ, c=next(colours),
         label = label_noΛ, zorder=1, ls=ls[':'])
ax1.plot(model_z, model_ωΩ, c=next(colours),
         label = label_ωΩ, zorder=1, ls=ls['-'])
ax1.plot(model_z, model_ΩΛ, c=next(colours),
         label = label_ΩΛ, zorder=1, ls=ls['-..'])
ax1.plot(model_z, model_Ω_DE0, c=next(colours),
         label = label_Ω_DE0, zorder=1, ls=ls['-.'])
ax1.plot(model_z, model_Ω_DE1, c=next(colours),
         label = label_Ω_DE1, zorder=1, ls=ls['--'])
ax1.plot(model_z, model_allΛ, c=next(colours),
         label = label_allΛ, zorder=1, ls=ls[':'])
ax1.legend(loc='upper right',
           bbox_to_anchor=(0.999, 0.999),
           frameon=False, fontsize=12)


## Middle Plot ##
print('{:-^100}'.format(' Setup Middle Plot ')+'\n')
ax2.tick_params(axis = 'both',  # Set tick marks inside and outside of
                top = True,  bottom = True, left = True, right = True,
                direction = 'in', length = 3)
plt.setp(ax2.get_xticklabels(), visible=False)
ax2.set_ylabel(y_label, labelpad=+6, fontsize=13)


ax2.plot(model_z, model_ωΩ, ls=ls['-'], c='black', zorder=3)
ax2.plot(model_z, model_ub, ls=ls['--'], c='grey', zorder=2)
ax2.plot(model_z, model_lb, ls=ls['--'], c='grey', zorder=2)
ax2.plot(model_z, model_allω, ls=ls[':'], c='grey', zorder=2)
ax2.plot(model_z, model_noω, ls=ls[':'], c='grey', zorder=2)
ax2.fill_between(model_z, model_lb, model_ub, zorder=0,
                 color=(0.82,0.82,0.82,1))

colours = iter(cm.rainbow(np.linspace(0, 1, len(datasets))))
dataset_markers = iter(markers)
for dataset in datasets:
    dataset_arr = all_data[np.where(all_data['dataset'] == dataset)]
    colour, marker = next(colours), next(dataset_markers)
    ax2.errorbar(dataset_arr['z'], dataset_arr['mag'],
                 yerr=dataset_arr['m_err'], ls='', marker=marker,
                 c=colour, zorder=1, capsize=1.5, label=dataset)
ax2.errorbar(outliers_arr['z'], outliers_arr['mag'], yerr=outliers_arr['m_err'],
             ls='', c='black', marker='s', zorder=1, capsize=1.5,
             label='Outlier', markeredgewidth=1, markeredgecolor='black',
             markerfacecolor='None')

ax2.legend(loc='upper right', bbox_to_anchor=(0.999, 0.999), frameon=False,
           ncol=2, fontsize=12)


## Residual Plot ##
print('{:-^100}'.format(' Setup Residual Plot ')+'\n')
ax3.tick_params(axis = 'both',  # Set tick marks inside and outside of
                top = True,  bottom = True, left = True, right = True,
                direction = 'in', length = 3)
ax3.set_xlabel(x_label, labelpad=+2, fontsize=13)
ax3.set_ylabel(y_label_res, labelpad=-2, fontsize=13)

ax3.axhline(y=0, c='black', ls=ls['-'], zorder=3)
ax3.plot(model_z, np.ones(model_z.shape), ls=ls['--'], c='grey', zorder=2)
ax3.plot(model_z, -np.ones(model_z.shape), ls=ls['--'], c='grey', zorder=2)
ax3.fill_between(model_z, np.ones(model_z.shape), -np.ones(model_z.shape),
                 zorder=1, color=(0.82,0.82,0.82,1), alpha=0.4)

colours = iter(cm.rainbow(np.linspace(0, 1, len(datasets))))
dataset_markers = iter(markers)
for dataset in datasets:
    dataset_arr = all_data[np.where(all_data['dataset'] == dataset)]
    colour, marker = next(colours), next(dataset_markers)
    ax3.scatter(dataset_arr['z'], datasets_norm_res[dataset],
                c=colour, marker=marker, zorder=0)

# Occurence Plot #
ax4.yaxis.tick_right()
ax4.tick_params(axis = 'both',  # Set tick marks inside and outside of x-axis.
                top = True, bottom = True, left = True, right = True,
                direction = 'in', length = 3)
ax4.xaxis.set_label_position('bottom')
ax4.set_xlabel(x_label_occ, labelpad=+2, fontsize=13)
plt.setp(ax4.get_yticklabels(), visible=False)

ax4.axhline(y=0, c='black', ls=ls['-'], zorder=3)
ax4.plot(x_lim_occ, np.ones(len(x_lim_occ)), ls=ls['--'], c='grey', zorder=2)
ax4.plot(x_lim_occ, -np.ones(len(x_lim_occ)), ls=ls['--'], c='grey', zorder=2)
ax4.fill_between(x_lim_occ, np.ones(len(x_lim_occ)), -np.ones(len(x_lim_occ)),
                 zorder=1, color=(0.82,0.82,0.82,1), alpha=0.4)
color = cm.rainbow(np.linspace(0, 1, len(datasets)))[7]
ax4.barh(occ_bins[:-1], bin_values, widths, align='edge', facecolor=color,
         edgecolor='black', zorder=0)
ax4.plot(norm_scale*norm_x, norm_y, ls=ls['--'], c='red', zorder=3)


## Set Axes Limits and Title ##
ax1.set_xlim(x_lim)
ax1.set_ylim(y_lim)
ax1.invert_yaxis()
ax3.set_ylim(y_lim_res)
ax3.yaxis.set_ticks([-20, -10, 0.0, 10, 20])
ax3.invert_yaxis()
ax4.set_xlim(x_lim_occ)
labels = [' 0', '20', '40', '60']
ax4.set_xticklabels(labels)
fig.patch.set_alpha(alpha)


## Save/Show Figure ##
save = 'y'
while save.upper() not in ['Y', 'N']:
    save = input('Would you like to save this graph? (y/n): ')
if save.upper() == 'Y':
    fig.savefig(folder_final+'mag_vs_redshift.png', format='png',
                bbox_inches='tight', pad_inches=0, dpi = dpi)
    print('{:-^100}'.format(' Graph Saved ')+'\n')
# plt.show()
print('{:#^100}'.format(' Program Complete '))
