import dill as pickle, numpy as np, matplotlib.pyplot as plt, matplotlib.cm as cm
from textwrap import wrap
from Milestone_imports import flux2mag, Lp2flux, z2eta

all_graphing_data = pickle.load(open("graphing_data.p", "rb"))  # Load in data for graphing.
for varaible, var_data in all_graphing_data.items():  # Turn each part of dictionary into an actual varaible with same name as the key.
    exec(varaible + ' = var_data')

all_arr['m_err'] = all_arr['m_err']*1.2

Lp = 3.25e39
Om_cc, Om_cc_err = 0.71, 0.15
x_lim = [0.0, 1.45]
y_lim = [14.0, 27.0]
model_z = np.linspace(x_lim[0]+0.01, x_lim[1], 300)


fig = plt.figure(figsize=(9,6))
ax1 = fig.add_axes([0.05,0.59,0.9,0.36])  # Add axes on top half of the vertical.
ax2 = fig.add_axes([0.05,0.23,0.9,0.36], sharex = ax1, sharey = ax1)
ax3 = fig.add_axes([0.05,0.05,0.9,0.18], sharex = ax1)

##### Top Plot #####
ax1.xaxis.tick_top()
ax1.tick_params(axis = 'both',  # Set tick marks inside and outside of x-axis.
                top = True, bottom = True, left = True, right = True,
                direction = 'in', length = 3)

Om_cc_values = sorted([0.0, 0.5, 1.0, Om_cc])
colours = iter(cm.rainbow(np.linspace(0, 1, len(Om_cc_values))))
for n, iOm_cc in enumerate(Om_cc_values):
    ieff_m = Om_cc2mag(iOm_cc, model_z, Lp)
    label = r'$\Omega_{{\Lambda}}$ = {:.2f}'.format(iOm_cc)
    ax1.plot(model_z, ieff_m, c=next(colours), label = label, zorder=1)
ax1.errorbar(all_arr['z'], all_arr['eff_m'], yerr=all_arr['m_err'], ls='',
             marker='+', capsize=1.5, c='black', zorder=0)

ax1.legend(loc='lower right', bbox_to_anchor=(0.999, 0.001), frameon=False)
#ax1.set_xlabel(r'ax1 $x$-axis')
ax1.xaxis.set_label_position('top')
ax1.set_ylabel(r'ax1 $y$-axis')


##### Bottom Plot #####
ax2.tick_params(axis = 'both',  # Set tick marks inside and outside of
                top = True,  bottom = True, left = True, right = True,
                direction = 'in', length = 3)

model_bf = Om_cc2mag(Om_cc, model_z, Lp)
label = r'$\Omega_{{\Lambda}}$ = {:.2f}'.format(Om_cc)
fig.text(0.774,0.305,label,fontsize=11) #######################EDIT POSITION
ax2.plot(model_z, model_bf, ls='-', c='black', zorder=2)
model_lb = Om_cc2mag(Om_cc-Om_cc_err, model_z, Lp)
ax2.plot(model_z, model_lb, ls='--', c='grey', zorder=1)
model_ub = Om_cc2mag(Om_cc+Om_cc_err, model_z, Lp)
ax2.plot(model_z, model_ub, ls='--', c='grey', zorder=1)
datasets = sorted(set(all_arr['dataset']), key=len)
colours = iter(cm.rainbow(np.linspace(0, 1, len(datasets))))
dataset_markers = iter(['o', '^', '1', 'p', 's', '*', '+', 'x', 'd', r'$\ast $'])
for dataset in datasets:
    dataset_arr = all_arr[np.where(all_arr['dataset'] == dataset)]
    ax2.errorbar(dataset_arr['z'], dataset_arr['eff_m'],
                 yerr=dataset_arr['m_err'], ls='', marker=next(dataset_markers),
                 c=next(colours), zorder=0, label=dataset)
ax2.legend(loc='lower right', bbox_to_anchor=(0.999, 0.001), frameon=False,
           ncol=2)


ax2.set_ylabel(r'ax2 $y$-axis')


##### Residue Plot #####




ax1.set_xlim(x_lim)
ax1.set_ylim(y_lim)
plt.suptitle("\n".join(wrap(r'Main Title (with text wrapping)', 50)),
             fontsize=18, y=1.0001) #######################EDIT Y_VALUE

plt.show()
