import dill as pickle, numpy as np, matplotlib.pyplot as plt, matplotlib.cm as cm
from textwrap import wrap

RQ_starts = (6.55, 6.35)
Qmin_start = 4.4
RM_cross = (5.1, 2.1)
QM_cross = (6.2, 1.3)
Q_droptime = 0.09
Q_initrng = (RQ_starts[0], 4.2)
Q_enddrop = 0.05

padwidth = 0.25
x_range = (0, 7.5)
y_range = (0, 7)
x_ticks=[[      1,       2,      3,        4,      5,        6,       7    ],
         [r'10$^{30}$', '', r'10$^{20}$', '', r'10$^{10}$', '', r'10$^{0}$']]
y_ticks=[[      1,       2,      3,        4,      5,        6,       7    ],
         [r'10$^{0}$', '', r'10$^{40}$', '', r'10$^{80}$', '', r'10$^{120}$']]



######## Code ########
def label_line(line, ax, label, x, y, color='black', size=12):
    xdata, ydata = line.get_data()
    x1 = xdata[0]
    x2 = xdata[-1]
    y1 = ydata[0]
    y2 = ydata[-1]

    #ax = line.get_axes()
    text = ax.annotate(label, xy=(x, y), xytext=(-10, 0),
                       textcoords='offset points',
                       size=size, color=color,
                       horizontalalignment='center',
                       verticalalignment='center')

    sp1 = ax.transData.transform_point((x1, y1))
    sp2 = ax.transData.transform_point((x2, y2))

    rise = (sp2[1] - sp1[1])
    run = (sp2[0] - sp1[0])

    slope_degrees = np.degrees(np.arctan2(rise, run))
    text.set_rotation(slope_degrees+180)
    return text

grad = lambda y2,y1,x2,x1: (y2-y1)/(x2-x1)
model = lambda x,y2,y1,x2,x1: (x-x1)*grad(y2,y1,x2,x1) + y1
pad = padwidth/(2**0.5)
centre = lambda y2,y1,x2,x1: (x1+(x2-x1)/2 + pad, y1+(y2-y1)/2 + pad)
angle = lambda y2,y1,x2,x1: np.rad2deg(np.arctan(grad(y2,y1,x2,x1)**-1))

R_model = lambda x: model(x, RM_cross[1],RQ_starts[0],RM_cross[0],0.0)
M_model = lambda x: model(x, QM_cross[1],RM_cross[1],QM_cross[0],RM_cross[0])
Q_pmodel = lambda x: x*grad(RM_cross[1],RQ_starts[0],RM_cross[0],0.0) + RQ_starts[1]
Q_attrxcrd = (Q_initrng[1] - RQ_starts[1])/grad(RM_cross[1],RQ_starts[0],RM_cross[0],0.0)

x = np.linspace(x_range[0], x_range[1], 10)
R, M = R_model(x), M_model(x)
Q_xs = [x_range[0], RM_cross[0], RM_cross[0]+Q_droptime, x_range[1]]
Q_ys = [Q_pmodel(x_range[0]), Q_pmodel(RM_cross[0]), QM_cross[1], QM_cross[1]-Q_enddrop]

R_arrw = [RM_cross[1] + pad, RQ_starts[0], RM_cross[0], x_range[0] + pad] # [y2, y1, x2, x1].
M_arrw = [QM_cross[1] + pad, RM_cross[1] + pad, QM_cross[0], RM_cross[0]] # [y2, y1, x2, x1].
Q_arrw = [Q_ys[-1] + pad + Q_enddrop, QM_cross[1] + pad, x_range[1], QM_cross[0]]

R_centre, R_angle = centre(*R_arrw), angle(*R_arrw)
M_centre, M_angle = centre(*M_arrw), angle(*M_arrw)
Q_centre, Q_angle = centre(*Q_arrw), angle(*Q_arrw)



fig = plt.figure(figsize=(9,6.5))
ax1 = fig.add_subplot(111)  # Add axes on top half of the vertical.

ax1.plot(x, M, ls='-.', zorder=1, c='green', label=r'Matter, $M$')
ax1.plot(x, R, ls='--', zorder=1, c='orange', label=r'Radiation, $\gamma$')
ax1.plot(Q_xs, Q_ys, ls='-', zorder=2, c='blue', label=r'k-essence, $Q$')
ax1.fill_between([x_range[0], Q_attrxcrd],
                 Q_initrng, [Q_initrng[1], Q_initrng[1]],
                 zorder=0, color='lightblue')
ax1.legend(loc='upper right', bbox_to_anchor=(0.99, 0.99), frameon=False,
           prop={'size': 13})

bbox = {'fc': '0.8', 'pad': 0}
props = {'ha': 'center', 'va': 'center'}#, 'bbox': bbox}
ax1.annotate('', xytext=(R_arrw[3], R_arrw[1]), xy=(R_arrw[2], R_arrw[0]),
             xycoords='data', textcoords='data',
             arrowprops={'arrowstyle': '<->', 'color':'orange'})
Im_line, = ax1.plot(R_arrw[2:], R_arrw[:2], alpha=0)
label_line(Im_line, ax1, 'Radiation Dominant', *R_centre, color='orange', size=12)

ax1.annotate('', xytext=(M_arrw[3], M_arrw[1]), xy=(M_arrw[2], M_arrw[0]),
             xycoords='data', textcoords='data',
             arrowprops={'arrowstyle': '<->', 'color':'green'})
Im_line, = ax1.plot(M_arrw[2:], M_arrw[:2], alpha=0)
label_line(Im_line, ax1, 'M Dominant', *M_centre, color='green', size=12)

ax1.annotate('', xytext=(Q_arrw[3], Q_arrw[1]), xy=(Q_arrw[2], Q_arrw[0]),
             xycoords='data', textcoords='data',
             arrowprops={'arrowstyle': '<->', 'color':'blue'})
Im_line, = ax1.plot(Q_arrw[2:], Q_arrw[:2], alpha=0)
label_line(Im_line, ax1, 'Q Dominant', *Q_centre, color='blue', size=12)

ax1.set_xlim(x_range)
ax1.set_xticks(x_ticks[0])
ax1.set_xticklabels(x_ticks[1])
ax1.set_ylim(y_range)
ax1.set_yticks(y_ticks[0])
ax1.set_yticklabels(y_ticks[1])

ax1.set_xlabel(r'Redshift, $z + 1$')#, labelpad=-0.6)
ax1.set_ylabel(r'Energy Density, $\rho$ (eV$\cdot$mm$^{-3}$)')#, labelpad=-0.5)
label = r'$Q$ Inital Conditions'
ax1.text(0.05, 4.25, label, fontsize=11, color='blue')

fig.patch.set_alpha(0.0)
fig.savefig('poster_k-essence_graph.png', format='png', bbox_inches='tight',
            pad_inches=0, dpi = 750)
plt.show()
