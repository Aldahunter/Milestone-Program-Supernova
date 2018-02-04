"""Supernova Milestone Program for Physics Problem Solving."""
import numpy as np
import matplotlib.pyplot as pyplot
import matplotlib.cm as cm
import scipy, tkinter
from Milestone_imports_alldata import * #Use Milestone_imports for small sample data, use Milestone_imports_alldata for all Union2.1 data.

################################## Find L_peak #################################
print('\n'+'-'*39+' Find Peak Luminosity '+'-'*39+'\n')
### Clalc flux and L_peak for low redshifts ###
lz_arr = strarray_add_column(data_lz,  mag2flux(data_lz['eff_m']), 'flux',
                               np.float64) #Calculate and append flux (erg·cm⁻²·s⁻¹·Å⁻¹) to main array.

lz_arr = strarray_add_column(lz_arr,  flux2Lp(lz_arr['flux'], lz_arr['z'],
                                                  0.0, low_z = True),
                               'Lp', np.float64, print_array = True) #Calculate and append L_peak (erg·s⁻¹·Å⁻¹) to main array.

### Find best guess for Peak Luminosity ###
Lp_range = np.linspace(lz_arr['Lp'].min(), lz_arr['Lp'].max(), 10) #Create a range of L_peak (erg·s⁻¹·Å⁻¹) values between bounds.
Lp_guesses = np.empty((10,2), dtype=np.float64)
for n, Lp in enumerate(Lp_range): #Cycle through each L_peak (erg·s⁻¹·Å⁻¹).
    exp_eff_m = flux2mag(Lp2flux(Lp, lz_arr['z'], 0.0, low_z = True)) #Calculate the expected effective magnitude (dimensionless) for the given L_peak.
    chisq = calc_chisq(exp_eff_m, lz_arr['eff_m'], lz_arr['m_err']) #Calculate χ² (dimensionless) for given L_peak.
    Lp_guesses[n] = Lp, chisq
Lp_guesses = Lp_guesses[Lp_guesses[:,1].argsort()] #Sort L_peak guesses by χ².

### Calculate minimised χ² and best value and uncertainty for Peak Luminosity ###
Lp2mag = lambda Lp, z, eta, low_z: flux2mag(Lp2flux(Lp, z, eta, low_z))
Lp2mag_args = (lz_arr['z'], 0.0, True)
Lp_chisq_stats = calc_min_chisq(Lp2mag, Lp_guesses[0,0], Lp2mag_args, #Calculate minimised χ² (dimensionless), and Bestfit, error and percentage error for L_peak (erg·s⁻¹·Å⁻¹).
                                lz_arr['eff_m'], lz_arr['m_err'],
                                return_stats = True)
chisq_min, Lp, Lp_err, Lp_perr = Lp_chisq_stats #Assign variables to returned values (Dimensionless, erg·s⁻¹·Å⁻¹, erg·s⁻¹·Å⁻¹, Dimesionless).

adopted_units = (Lp*1e-7, Lp_err*1e-7, Lp_perr, chisq_min) #Convert from (Dimensionless, J·s⁻¹·Å⁻¹, J·s⁻¹·Å⁻¹, Dimesionless).
string = 'L_peak = %0.2e ' + pm + ' %0.1e (%0.2g%%) J·s' + Sm1 + '·Å' + Sm1 #Add unicode superscript to string.
string += ' | Reduced ' + chiSq + ': %0.2f'
print(string % adopted_units) #Format and print string.


####################### Find Omega_CosmologicalConstant ########################
print('\n'+'-'*42+' Find Omega_cc '+'-'*42+'\n')
hz_arr = data_hz[:]
show_strarray(hz_arr) #Print array to be seen.

### Find best guess for Ω_cc ###
Om_cc_Range = np.linspace(-0.5, 1.5, 21) #Test range of Ω_cc guesses to minimize χ².
Om_cc_guesses = np.empty((len(Om_cc_Range),2), dtype=np.float64) #Create array to hold guesses and χ².

for i, iOm_cc in enumerate(Om_cc_Range): #Cycle through each Ω_cc guess.
    ieta = z2eta(hz_arr['z'], iOm_cc) #Calc comoving coord (η) for each Ω_cc guess.
    ieff_m = flux2mag( Lp2flux(Lp, hz_arr['z'], ieta))
    ichisq = calc_chisq(ieff_m, hz_arr['eff_m'], hz_arr['m_err']) #Calc χ² for each Ω_cc guess.
    Om_cc_guesses[i] = iOm_cc, ichisq
Om_cc_guesses = Om_cc_guesses[Om_cc_guesses[:,1].argsort()] #Sort Ω_cc guesses by χ².


### Calculate minimised χ² and best value and uncertainty for Ω_cc ###
#Om_cc2mag = lambda Om_cc, z, Lp: flux2mag(Lp2flux(Lp, z, z2eta(z, Om_cc)))
def Om_cc2mag(Om_cc, z, Lp):
    return flux2mag(Lp2flux(Lp, z, z2eta(z, Om_cc)))
Om_cc2mag_args = (hz_arr['z'], Lp)

Om_cc_chisq_stats = calc_min_chisq(Om_cc2mag, Om_cc_guesses[0,0],  #Calculate minimised χ², and Bestfit, error and percentage error for L_peak.
                                   Om_cc2mag_args, hz_arr['eff_m'],
                                   hz_arr['m_err'], return_stats = True)
chisq_min, Om_cc, Om_cc_err, Om_cc_perr = Om_cc_chisq_stats #Assign variables to returned values.

string = Omega + '_cc = %0.2f ' + pm + ' %0.2f (%0.2g%%) | Reduced ' + chiSq + ': %0.2f'
print(string % (Om_cc, Om_cc_err, Om_cc_perr, chisq_min))



################################## Plot Graphs #################################
### Plots for L_peak ###
model_z = np.linspace(lz_arr['z'].min(), lz_arr['z'].max(), 50) #Range of redshift values for line of bestfit.

f = lambda Lp, err, args: (Lp2mag(Lp, *args), Lp2mag(Lp + err, *args),
                           Lp2mag(Lp - err, *args))
bf_eff_m, ub_eff_m, lb_eff_m = f(Lp, Lp_err, (model_z, 0.0, True)) #Y-axis values for line of bestfit and upper and lower uncertainties for line of best fit.
model = [(model_z,bf_eff_m,{'ls':'-','c':'0','zorder':0}),
         (model_z,ub_eff_m,{'ls':'--','c':'0','zorder':0}),
         (model_z,lb_eff_m,{'ls':'--','c':'0','zorder':0})] #Lines of best fit to plot.
kwargs = {'y_err':lz_arr['m_err'], 'x_label':r'Redshift, ($z$)',
          'y_label':r'Effective Magnitude, ($m_{eff}$)', 'marker':'+',
          'plot_line':model, 'err_kwargs':{'zorder':10}, 'zorder':10}
Graph1 = (212, lz_arr['z'], lz_arr['eff_m'], kwargs)

model = []
colours = iter(cm.rainbow(np.linspace(0, 1, len(Lp_guesses))))
for iLp, ichi in Lp_guesses:
    ieff_m = Lp2mag(iLp, model_z, 0.0, True)
    idict = {'ls':'-','c':next(colours),'zorder':0}
    model.append((model_z, ieff_m, idict))
kwargs = {'y_err':lz_arr['m_err'], 'x_label':r'Redshift, ($z$)',
          'y_label':r'Effective Magnitude, ($m_{eff}$)', 'marker':'+',
          'plot_line':model, 'err_kwargs':{'zorder':10}, 'zorder':10}
Graph2 = (211, lz_arr['z'], lz_arr['eff_m'], kwargs)

#show_graphs(Graph1, Graph2,  main_title = r'Low Redshift SNIa Data')

### Plots for Om_cc ###  #####For just high redshifts change 'data' to 'hz_arr' for everything below here!!!!!!!!!!!!!!!!!!!!!!!!!!
model_z = np.linspace(data['z'].min(), data['z'].max(), 50) #Range of redshift values for line of bestfit.

f = lambda Lp, err, args: (Om_cc2mag(Om_cc, *args),
                           Om_cc2mag(Om_cc + err, *args),
                           Om_cc2mag(Om_cc - err, *args))
bf_eff_m, ub_eff_m, lb_eff_m = f(Om_cc, Om_cc_err, (model_z, Lp)) #Y-axis values for line of bestfit and upper and lower uncertainties for line of best fit.
model = [(model_z,bf_eff_m,{'ls':'-','c':'0','zorder':0}),
         (model_z,ub_eff_m,{'ls':'--','c':'0','zorder':0}),
         (model_z,lb_eff_m,{'ls':'--','c':'0','zorder':0})] #Lines of best fit to plot.
kwargs = {'y_err':data['m_err'], 'x_label':r'Redshift, ($z$)',
          'y_label':r'Effective Magnitude, ($m_{eff}$)', 'marker':'+',
          'plot_line':model, 'err_kwargs':{'zorder':10}, 'zorder':10}
Graph1 = (212, data['z'], data['eff_m'], kwargs)

model = []
colours = iter(cm.rainbow(np.linspace(0, 1, len(Om_cc_guesses))))
for iOm_cc, ichi in Om_cc_guesses:
    ieff_m = Om_cc2mag(iOm_cc, model_z, Lp)
    idict = {'ls':'-','c':next(colours),'zorder':0}
    model.append((model_z, ieff_m, idict))
kwargs = {'y_err':data['m_err'], 'x_label':r'Redshift, ($z$)',
          'y_label':r'Effective Magnitude, ($m_{eff}$)', 'marker':'+',
          'plot_line':model, 'err_kwargs':{'zorder':10}, 'zorder':10}
Graph2 = ({'pos':211, 'sharex':1, 'sharey':1}, data['z'], data['eff_m'], kwargs)

#show_graphs(Graph1, Graph2,  main_title = r'High Redshift SNIa Data')

import dill as pickle
all_graphing_data = {'lz_arr' : lz_arr, 'hz_arr' : hz_arr, 'all_arr' : data,
                     'model_z' : model_z, 'Om_cc2mag' : Om_cc2mag} #Om_cc2mag(Om_cc {float}, z {array/float}, Lp {float})

pickle.dump(all_graphing_data, open("graphing_data.p", "wb" ))
print('Graphing Data Saved')
