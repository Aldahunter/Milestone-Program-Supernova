"""Supernova Milestone Program for Physics Problem Solving."""
import numpy as np
import matplotlib.pyplot as pyplot
import scipy, tkinter
from Milestone_imports import *

################################## Find L_peak #################################
### Clalc flux and L_peak for low redshifts ###
lz_arr = strarray_add_column(data_lz,  mag2flux(data_lz['eff_m']), 'flux',
                               np.float64) #Calculate and append flux to main array.
lz_arr = strarray_add_column(lz_arr,  flux2Lp(lz_arr['flux'], lz_arr['z'],
                                                  0.0, low_z = True),
                               'Lp', np.float64, print_array = True) #Calculate and append L_peak to main array.


## Find best guess for Luminosity Peak ###
Lp_range = np.linspace(lz_arr['Lp'].min(), lz_arr['Lp'].max(), 10) #Create a range of Lpeak values between bounds.


### Find minimised Chi Squared from range of Luminosity Peaks ###
Lp_guesses = np.empty((10,2), dtype=np.float64)
for n, Lp in enumerate(Lp_range): #Cycle through each peak Luminosity.
    exp_eff_m = flux2mag(Lp2flux(Lp, lz_arr['z'], 0.0, low_z = True)) #Calculate the expected effective magnitude for the given Luminsity Peak.
    chisq = calc_chisq(exp_eff_m, lz_arr['eff_m'], lz_arr['m_err']) #Calculate Chi Squared for given peak Luminosity.
    Lp_guesses[n] = Lp, chisq
Lp_guesses = Lp_guesses[Lp_guesses[:,1].argsort()] #Sort Luminosity Peak guesses by Chi Squared


### Calculate minimised Chi Squared and best value and uncertainty for Luminosity Peak ###
Lp2mag = lambda Lp, z, eta, low_z: flux2mag(Lp2flux(Lp, z, eta, low_z))
Lp2mag_args = (lz_arr['z'], 0.0, True)

Lp_chisq_stats = calc_min_chisq(Lp2mag, Lp_guesses[0,0], Lp2mag_args, #Calculate minimised Chi Squared, and Bestfit, error and percentage error for Luminosity Peak.
                                lz_arr['eff_m'], lz_arr['m_err'],
                                return_stats = True)
chisq_min, Lp, Lp_err, Lp_perr = Lp_chisq_stats #Assign variables to returned values.
print('L_peak = %0.5f +/- %0.5f (%0.2g%%) with Chi_sq: %0.2f' %(Lp, Lp_err, Lp_perr, chisq_min))




print('\n'+'-'*100+'\n')
################################# Find Omega_cc ################################
print(data_hz)
Om_cc_Range = np.linspace(-2.0, 2.0, 41) #Test range of Omega_cc guesses to minimize Chi Squared.
Om_cc_guesses = np.empty((41,2), dtype=np.float64)

for i, iOm_cc in enumerate(Om_cc_Range): #Cycle through each Omega_cc guess.
    ieta = z2eta(data_hz['z'], iOm_cc)
    # print(iOm_cc,'\n', ieta)
    iflux = Lp2flux(Lp, data_hz['z'], ieta)
    # print(iOm_cc,'\n', iflux)
    ieff_m = flux2mag(iflux)
    # print(iOm_cc,'\n', ieff_m)
    ichisq = calc_chisq(ieff_m, data_hz['eff_m'], data_hz['m_err'])
    # print(iOm_cc,'\n', ichisq, '\n')
    Om_cc_guesses[i] = iOm_cc, ichisq
m_cc_guesses = Om_cc_guesses[Om_cc_guesses[:,1].argsort()] #Sort Omega_cc guesses by Chi Squared.
print(Om_cc_guesses)





quit()
################################## Plot Graphs #################################
### Plots for L_peak ###
model_z = np.linspace(lz_arr['z'].min(), lz_arr['z'].max(), 50) #Range of redshift values for line of bestfit.
f = lambda Lp, err, args: (Lp2mag(Lp, *args), Lp2mag(Lp + err, *args), Lp2mag(Lp - err, *args))
bf_eff_m, ub_eff_m, lb_eff_m = f(Lp, Lp_err, (model_z, 0.0, True)) #Y-axis values for line of bestfit and upper and lower uncertainties for line of best fit.
model = [(model_z,bf_eff_m,{'ls':'-','c':'0'}),
         (model_z,ub_eff_m,{'ls':'--','c':'0'}),
         (model_z,lb_eff_m,{'ls':'--','c':'0'})] #Lines of best fit to plot.

kwargs = {'y_err':lz_arr['m_err'], 'x_label':r'Redshift, ($z$)',
          'y_label':r'Effective Magnitude, ($m_{eff}$)', 'marker':'+',
          'plot_line':model}
Graph1 = (111, lz_arr['z'], lz_arr['eff_m'], kwargs)
show_graphs(Graph1,  main_title = r'Low Redshift SNIa Data')
