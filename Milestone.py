"""Supernova Milestone Program for Physics Problem Solving."""
import numpy as np
import matplotlib.pyplot as pyplot
import scipy, tkinter
from Milestone_imports import *


### Clalc flux and L_peak for low redshifts ###
main_arr = strarray_rem_column(low_z, 'err') #Create main array to hold important data.

flux_low_z = mag_to_flux(main_arr['eff_m']) #Calculate flux for low z.
main_arr = strarray_add_column(main_arr, flux_low_z, 'flux', flux_low_z.dtype,
                               print_array = True) #Append flux to main array.

## Calc a range of L_peaks over the low redshifts ###
Lpeak_low_z = flux_to_Lpeak(flux_low_z, main_arr['z'], 0.0, low_z = True) #Calculate Lpeak for low z.
Lpeak_range = np.linspace(Lpeak_low_z.min(), Lpeak_low_z.max(), 10) #Create a range of Lpeak values between bounds.

### Calc Distance Luminosity Model from Redshift ###
z_model = np.linspace(main_arr['z'].min(), main_arr['z'].max(), 100) #Create a range of z values between given data.
d_L_model = redshift_to_distLum(z_model) #Calculate Distance Luminosity (d_L) from redshift.
model = (z_model, d_L_model) #Put in tuple to plot on graphs.

### Calc Luminsoity distance for each Luminosity Peak ###
for Lpeak in Lpeak_range: #Cycle through each peak Luminosity.
    d_L = Lpeak_to_distLum(Lpeak, main_arr['flux']) #Calculate Distance Luminosity (d_L) Lpeak and flux.

    kwargs = {'x_label':r'Redshift, ($z$)', 'y_label':r'Distance Luminosity, ($d_{L}$)',
              'marker':'x', 'line':False, 'trend_line':model}
    Graph1 = (111, main_arr['z'], d_L, kwargs)
    show_graphs(Graph1,  main_title = r'Low Redshift SNIa Data')

quit()

### Plot Graphs for Visuals.

kwargs = {'x_label':r'Redshift, ($z$)', 'y_label':r'Effective Magnitude, ($m_{eff}$)',
          'marker':'x', 'line':False, 'trend_line':model}
Graph1 = (111, main_arr['z'], main_arr['eff_m'], kwargs)
# kwargs = {'x_label':r'Redshift, ($z$)', 'y_label':r'Peak Luminosity, ($L_{peak}$)',
#           'marker':'x', 'line':False}
# Graph2 = (212, main_arr['z'], main_arr['L_peak'], kwargs)

show_graphs(Graph1,  main_title = r'Low Redshift SNIa Data')
