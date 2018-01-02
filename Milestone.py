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


## Calc a range of L_peaks ###
Lp_range = np.linspace(main_arr['Lp'].min(), main_arr['Lp'].max(), 100) #Create a range of Lpeak values between bounds.


### Find minimised Chi Squared from range of Luminosity Peaks ###
chisq_min = 1e10
for Lp in Lp_range: #Cycle through each peak Luminosity.
    exp_eff_m = flux2mag(Lp2flux(Lp, main_arr['z'], 0.0, low_z = True)) #Calculate the expected effective magnitude for the given Luminsity Peak.
    chisq = calc_chisq(exp_eff_m, main_arr['eff_m'], main_arr['m_err']) #Calculate Chi Squared for given peak Luminosity.

    if chisq < chisq_min: #Find smallest Chi Squared.
        chisq_min, Lp_best = chisq, Lp
print('\nBest Lpeak is:', Lp_best, '\t|\t Minimised chi_sq is:', chisq_min)



### Plot Graphs for Visuals.
model_z = np.linspace(main_arr['z'].min(), main_arr['z'].max(), 50)
model_eff_m = exp_eff_m = flux2mag(Lp2flux(Lp_best, model_z, 0.0, low_z = True))
kwargs = {'err':main_arr['m_err'], 'x_label':r'Redshift, ($z$)',
          'y_label':r'Effective Magnitude, ($m_{eff}$)', 'marker':'x',
          'line':False, 'trend_line':(model_z, model_eff_m)}
Graph1 = (111, main_arr['z'], main_arr['eff_m'], kwargs)
show_graphs(Graph1,  main_title = r'Low Redshift SNIa Data')
