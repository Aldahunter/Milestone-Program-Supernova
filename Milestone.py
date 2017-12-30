"""Supernova Milestone Program for Physics Problem Solving."""
import numpy as np
import matplotlib.pyplot as pyplot
import scipy, tkinter
from Milestone_imports import *

### Clalc flux and L_peak for low redshifts ###
flux_low_z = mag_to_flux(low_z['eff_m'])
Lpeak_low_z = flux_to_Lpeak(flux_low_z, low_z['z'], 0.0, low_z = True)
test_arr = create_test_array(low_z, flux_low_z, Lpeak_low_z)

### Calc a range of L_peaks over the low redshifts ###
Lpeak_limits = (test_arr['L_peak'].min(),test_arr['L_peak'].max())
Lpeak_low_Z_arr = np.linspace(Lpeak_limits[0], Lpeak_limits[1], 100)
#print(Lpeak_low_Z_arr)

### Plot Graphs for Visuals.
kwargs = {'x_label':r'Redshift, ($z$)', 'y_label':r'Effective Magnitude, ($m_{eff}$)',
          'marker':'x', 'line':False}
Graph1 = (211, test_arr['Rshf'], test_arr['Eff_M'], kwargs)

kwargs = {'x_label':r'Redshift, ($z$)', 'y_label':r'Peak Luminosity, ($L_{peak}$)',
          'marker':'x', 'line':False}
Graph2 = (212, test_arr['Rshf'], test_arr['L_peak'], kwargs)
show_graphs(Graph1, Graph2, main_title = r'Low Redshift SNIa Data')
