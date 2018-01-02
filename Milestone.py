"""Supernova Milestone Program for Physics Problem Solving."""
import numpy as np
import matplotlib.pyplot as pyplot
import scipy, tkinter
from Milestone_imports import *


### Clalc flux and L_peak for low redshifts ###
#main_arr = strarray_rem_column(data_lz, 'err') #Create main array to hold important data.
main_arr = strarray_add_column(data_lz,  mag2flux(data_lz['eff_m']), 'flux',
                               np.float64) #Calculate and append flux to main array.
main_arr = strarray_add_column(main_arr,  flux2Lp(main_arr['flux'], main_arr['z'],
                                                  0.0, low_z = True),
                               'Lp', np.float64, print_array = True) #Calculate and append L_peak to main array.


## Find best guess for Luminosity Peak ###
Lp_range = np.linspace(main_arr['Lp'].min(), main_arr['Lp'].max(), 10) #Create a range of Lpeak values between bounds.


### Find minimised Chi Squared from range of Luminosity Peaks ###
Lp_guesses = np.empty((10,2), dtype=np.float64)
for n, Lp in enumerate(Lp_range): #Cycle through each peak Luminosity.
    exp_eff_m = flux2mag(Lp2flux(Lp, main_arr['z'], 0.0, low_z = True)) #Calculate the expected effective magnitude for the given Luminsity Peak.
    chisq = calc_chisq(exp_eff_m, main_arr['eff_m'], main_arr['m_err']) #Calculate Chi Squared for given peak Luminosity.
    Lp_guesses[n] = Lp, chisq
Lp_guesses = Lp_guesses[Lp_guesses[:,1].argsort()] #Sort Luminosity Peak guesses by Chi Squared


### Calculate minimised Chi Squared and best value and uncertainty for Luminosity Peak ###
Lp2mag = lambda Lp, z, eta, low_z: flux2mag(Lp2flux(Lp, z, eta, low_z))
Lp2mag_args = (main_arr['z'], 0.0, True)

Lp_chisq_stats = calc_min_chisq(Lp2mag, Lp_guesses[0,0], Lp2mag_args, #Calculate minimised Chi Squared, and Bestfit, error and percentage error for Luminosity Peak.
                                main_arr['eff_m'], main_arr['m_err'],
                                return_stats = True)
chisq_min, Lp, Lp_err, Lp_perr = Lp_chisq_stats #Assign variables to returned values.
print('L_peak = %0.5f +/- %0.5f (%0.2g%%) with Chi_sq: %0.2f' %(Lp, Lp_err, Lp_perr, chisq_min))



################################################################################
### Plot Graphs for Visuals ###
model_z = np.linspace(main_arr['z'].min(), main_arr['z'].max(), 50) #Range of redshift values for line of bestfit.
f = lambda Lp, err, args: (Lp2mag(Lp, *args), Lp2mag(Lp + err, *args), Lp2mag(Lp - err, *args))
bf_eff_m, ub_eff_m, lb_eff_m = f(Lp, Lp_err, (model_z, 0.0, True)) #Y-axis values for line of bestfit and upper and lower uncertainties for line of best fit.
model = [(model_z,bf_eff_m), (model_z,ub_eff_m), (model_z,lb_eff_m)] #Lines of best fit to plot.

kwargs = {'err':main_arr['m_err'], 'x_label':r'Redshift, ($z$)',
          'y_label':r'Effective Magnitude, ($m_{eff}$)', 'marker':'x',
          'line':False, 'trend_line':model}
Graph1 = (111, main_arr['z'], main_arr['eff_m'], kwargs)
show_graphs(Graph1,  main_title = r'Low Redshift SNIa Data')
