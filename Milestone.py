"""Supernova Milestone Program for Physics Problem Solving."""
import numpy as np
import matplotlib.pyplot as pyplot
import scipy, tkinter
from Milestone_imports import *


### Clalc flux and L_peak for low redshifts ###
main_arr = strarray_rem_column(low_z, 'err') #Create main array to hold important data.

flux_low_z = mag_to_flux(main_arr['eff_m']) #Calculate flux for low z.
main_arr = strarray_add_column(main_arr, flux_low_z, 'flux', flux_low_z.dtype) #Append flux to main array.

Lpeak_low_z = flux_to_Lpeak(flux_low_z, main_arr['z'], 0.0, low_z = True) #Calculate Lpeak for low z.
main_arr = strarray_add_column(main_arr, Lpeak_low_z,
                               'L_peak', Lpeak_low_z.dtype, print_array = True)  #Append Lpeak to main array.


### Calc a range of L_peaks over the low redshifts ###
Lpeak_bounds = (main_arr['L_peak'].min(), main_arr['L_peak'].max()) #Get bounds for Lpeak of low z.
Lpeak_range = np.linspace(Lpeak_bounds[0], Lpeak_bounds[1], 100) #Create a range of Lpeak values between bounds.
print(Lpeak_range)


### Plot Graphs for Visuals.
kwargs = {'x_label':r'Redshift, ($z$)', 'y_label':r'Effective Magnitude, ($m_{eff}$)',
          'marker':'x', 'line':False}
Graph1 = (211, main_arr['z'], main_arr['eff_m'], kwargs)
kwargs = {'x_label':r'Redshift, ($z$)', 'y_label':r'Peak Luminosity, ($L_{peak}$)',
          'marker':'x', 'line':False}
Graph2 = (212, main_arr['z'], main_arr['L_peak'], kwargs)

show_graphs(Graph1, Graph2, main_title = r'Low Redshift SNIa Data')
