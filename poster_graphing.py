import dill as pickle, numpy as np, matplotlib.pyplot as plt, matplotlib.cm as cm
from textwrap import wrap
from Milestone_imports import flux2mag, Lp2flux, z2eta

all_graphing_data = pickle.load(open("graphing_data.p", "rb"))  # Load in data for graphing.
for varaible, var_data in all_graphing_data.items():  # Turn each part of dictionary into an actual varaible with same name as the key.
    exec(varaible + ' = var_data')

# Lp, Lp_err = 3.25e39, 3.25e39*0.04
# Om_cc, Om_cc_err = 0.71, 0.15
x_lim = [0.0, 1.45]
y_lim = [14.0, 27.0]
model_z = np.linspace(x_lim[0]+0.01, x_lim[1], 300)


fig = plt.figure(figsize=(9,6))
ax1 = fig.add_axes([0.06,0.59,0.9,0.36])  # Add axes on top half of the vertical.
ax2 = fig.add_axes([0.06,0.23,0.9,0.36], sharex = ax1, sharey = ax1)
ax3 = fig.add_axes([0.06,0.05,0.9,0.18], sharex = ax1)

##### Top Plot #####
ax1.xaxis.tick_top()
ax1.tick_params(axis = 'both',  # Set tick marks inside and outside of x-axis.
                top = True, bottom = True, left = True, right = True,
                direction = 'in', length = 3)
ax1.set_xlabel(r'Redshift, $z$', labelpad=-0.5)
ax1.xaxis.set_label_position('top')
ax1.set_ylabel(r'Effective Magnitude, $m_{eff}$', labelpad=+7)

Om_cc_values = sorted([0.0, 0.5, 1.0, Om_cc])
colours = iter(cm.rainbow(np.linspace(0, 1, len(Om_cc_values))))
for n, iOm_cc in enumerate(Om_cc_values):
    ieff_m = Om_cc2mag(iOm_cc, model_z, Lp)
    label = r'$\Omega_{{\Lambda}}$ = {:.2f}'.format(iOm_cc)
    ax1.plot(model_z, ieff_m, c=next(colours), label = label, zorder=1)
ax1.errorbar(all_arr['z'], all_arr['eff_m'], yerr=all_arr['m_err'], ls='',
             marker='+', capsize=1.5, c='black', zorder=0)
ax1.legend(loc='upper right', bbox_to_anchor=(0.999, 0.999), frameon=False)



##### Bottom Plot #####
ax2.tick_params(axis = 'both',  # Set tick marks inside and outside of
                top = True,  bottom = True, left = True, right = True,
                direction = 'in', length = 3)
plt.setp(ax2.get_xticklabels(), visible=False)
ax2.set_ylabel(r'Effective Magnitude, $m_{eff}$', labelpad=+7)


model_bf = Om_cc2mag(Om_cc, model_z, Lp)
label = r'$\Omega_{{\Lambda}}$ = {:.2f} $\pm$ {:.2f}'.format(Om_cc, Om_cc_err)
fig.text(0.774,0.305,label,fontsize=11)                                      #######################EDIT POSITION
ax2.plot(model_z, model_bf, ls='-', c='black', zorder=3)
model_lb = Om_cc2mag(Om_cc-Om_cc_err, model_z, Lp+Lp_err)
model_lb_err = ((Om_cc2mag(Om_cc-Om_cc_err, model_z, Lp)-model_lb)**2 + (Om_cc2mag(Om_cc, model_z, Lp+Lp_err)-model_lb)**2)**0.5
ax2.plot(model_z, model_lb, ls='--', c='grey', zorder=2)
model_ub = Om_cc2mag(Om_cc+Om_cc_err, model_z, Lp-Lp_err)
model_ub_err = ((Om_cc2mag(Om_cc+Om_cc_err, model_z, Lp)-model_ub)**2 + (Om_cc2mag(Om_cc, model_z, Lp-Lp_err)-model_ub)**2)**0.5
ax2.plot(model_z, model_ub, ls='--', c='grey', zorder=2)
ax2.fill_between(model_z, model_lb, model_ub, zorder=0,
                 color=(0.82,0.82,0.82,1))

datasets = sorted(set(all_arr['dataset']), key=len)
colours = iter(cm.rainbow(np.linspace(0, 1, len(datasets))))
dataset_markers = iter(['o', '^', '1', 'p', 's', '*', '+', 'x', 'd', r'$\ast $'])
for dataset in datasets:
    dataset_arr = all_arr[np.where(all_arr['dataset'] == dataset)]
    marker, color = next(dataset_markers), next(colours)
    ax2.errorbar(dataset_arr['z'], dataset_arr['eff_m'],
                 yerr=dataset_arr['m_err'], ls='', marker=marker,
                 c=color, zorder=1, capsize=1.5, label=dataset)
    dataset_residual = dataset_arr['eff_m']-Om_cc2mag(Om_cc,dataset_arr['z'],Lp)
    ax3.scatter(dataset_arr['z'], dataset_residual/dataset_arr['m_err'],
                marker=marker, c=color, zorder=1)
ax2.legend(loc='upper right', bbox_to_anchor=(0.999, 0.999), frameon=False,
           ncol=2)


##### Residue Plot #####
ax3.tick_params(axis = 'both',  # Set tick marks inside and outside of
                top = True,  bottom = True, left = True, right = True,
                direction = 'in', length = 3)
ax3.set_xlabel(r'Redshift, $z$', labelpad=-0.6)
ax3.set_ylabel(r'Norm. Residual', labelpad=-0.5)

ax3.axhline(y=0, c='black', ls='-', zorder=3)
norm_residual_lb = (model_lb-model_bf)/model_lb_err
norm_residual_ub = (model_ub-model_bf)/model_ub_err
ax3.plot(model_z, norm_residual_lb, c='grey', ls='--', zorder=2)
ax3.plot(model_z, norm_residual_ub, c='grey', ls='--', zorder=2)
ax3.fill_between(model_z, norm_residual_lb, norm_residual_ub, zorder=0,
                 color=(0.82,0.82,0.82,1))


##### Set axes limits #####
ax1.set_xlim(x_lim)
ax1.set_ylim(y_lim)
ax1.invert_yaxis()
ax3.set_ylim([-13,13])
ax3.invert_yaxis()
# plt.suptitle("\n".join(wrap(r'Main Title (with text wrapping)', 50)),
#              fontsize=18, y=1.0001)

plt.show()
