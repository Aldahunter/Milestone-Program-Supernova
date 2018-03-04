import dill as pickle, numpy as np, matplotlib.pyplot as plt, matplotlib.cm as cm
from textwrap import wrap
from final_program_imports import *
data = all_data[np.where(all_data['dataset'] != 'Outlier')]

# Import Calculated Data #
print('{:#^100}'.format(' Import Calculated Data ')+'\n')
calculated_data = pickle.load(open(folder+"final_data.p", "rb"))
for variable, var_data in calculated_data.items():
    exec(variable + ' = var_data')
print('Imported Variables are:\n  · ', end='')
print(' ; '.join(sorted([i for i in calculated_data]))+'\n')

### Figure & Axis Attributes ###
load_map = True
figsize = (7,14) #Inches
x_lim = (0.40, 0.5, 500) # Omega_DE.
y_lim = (-2.18, -1.92, 500) # w_DE.
dpi = 100

def ωΩ2chi(ω, Ω, z, Lp, obs_data, err_data):
    ωΩ2mag = lambda ωΩ, z, Lp: omega2mag(ωΩ[1], z, Lp, ωΩ[0])
    ωΩ_params, ωΩ2mag_params = (ω, Ω), (z, Lp)
    return minimise_fn(ωΩ_params, ωΩ2mag, ωΩ2mag_params, obs_data, err_data)


omegas = np.linspace(*x_lim) # omega's
ws = np.linspace(*y_lim) # w's
if load_map == True:
    chis = np.loadtxt("w_omega_contour_data(old_hd).txt")
else:
    chis = np.zeros((omegas.size, ws.size))
    perc, perc_step = 0.0, 0.25
    counter, counter_step = 0, chis.size*perc_step/100
    for ix, x in enumerate(omegas):
        for iy, y in enumerate(ws):
            chi_sq = ωΩ2chi(y, x, data['z'], 3.23e+32/1e-7, data['mag'], data['m_err'])
            chis[ix, iy] = chi_sq
            counter += 1
            if counter == counter_step:
                counter, perc = 0, perc + perc_step
                print(perc, '%')
    np.savetxt("w_omega_contour_data.txt", chis)
    quit()


min_chi = np.nanmin(chis)
print(ωΩ2chi(-2.11538, 0.480754, data['z'], Lp, data['mag'], data['m_err']))
chi = 670.554159004
plt.figure()

im = plt.imshow(chis, cmap=cm.gray, extent=(*x_lim[:-1][::-1], *y_lim[:-1]), aspect='auto')
CS = plt.contour(omegas[::-1], ws[::-1], chis, levels=[min_chi+1, min_chi+2.3, min_chi+4.61])
plt.scatter(ωΩ[1],ωΩ[0], color='r')
plt.clabel(CS, inline=1, fontsize=10)
plt.gca().invert_xaxis()
plt.show()

#
# omega_rng = np.arange(0.0, 1.0, 0.02)
# w_rng = np.arange(-0.5,-1.5,-0.02)
#
# print(omega_rng, w_rng)
# Omega, W = np.meshgrid(omega_rng, w_rng)
# Chi = w_omega2chi(W, Omega, data['z'], 3.23e+32/1e-7, data['mag'], data['m_err'])
# print(Chi)

### PLot Graph ###
fig = plt.figure(figsize=figsize)
ax1 = fig.add_axes([0.06,0.59,0.9,0.36])  # Add axes on top half of the vertical.
ax2 = fig.add_axes([0.06,0.23,0.9,0.36], sharex = ax1, sharey = ax1)
ax3 = fig.add_axes([0.06,0.05,0.9,0.18], sharex = ax1)
