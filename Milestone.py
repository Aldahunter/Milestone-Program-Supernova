"""Supernova Milestone Program for Physics Problem Solving."""
import numpy as np
import matplotlib.pyplot as pyplot
import scipy, tkinter

### Define Constants ###
K = 0 #Curvature of Universe can be 1(closed), 0(flat), -1(open).
m_0 = -20.45 #Gives flux in units: erg*cm-2*s-1*A-1.
H_0 = 75 #Current Hubble Flow in units: km*s-1*Mpc-1.
R_0 = 4.4e26 #Current raidus of observable universe in units: m.
c = 2.99792458e8 #Speed of light in units: m*s-1.

### Load Data ###
dtype = np.dtype([('name', np.str_, 16), ('z', np.float64, 1),
                  ('eff_m', np.float64, 1), ('err', np.float64, 1)])
data = np.loadtxt("SuperNova Data.txt", dtype=dtype)
low_z, high_z = data[:42], data[42:] #Split Data into low and high redshift.
name, z, eff_m, err = 'name', 'z', 'eff_m', 'err' #Reserve variables to easily call data from array.


### Define Functions ###
def mag_to_flux(eff_mag):
    """Return the flux (erg/cm^2/s/A) for a given effective magnitude."""
    return 10**((m_0 - eff_mag)/2.5)

def S_eta(eta, low_z = False, z = 0.0):
    """Return the comoving coordinate depending on the curvature of space."""
    if low_z == True:
        if K == 0: return (c*z)/(H_0*R_0)
    else:
        if K == 0: return eta
        elif K == 1: return np.sin(eta)
        elif K == -1: return np.sinh(eta)
        else: raise ValueError("K must be one of: 1, 0, -1")

def flux_to_Lpeak(flux, z, eta, low_z = False):
    """Return peak Luminosity (L_peak) for a given: flux, redshift (z) & comoving coord (eta).
          Note: If low_x = True the returned value is independent of eta."""
    return 4 * np.pi * (R_0*S_eta(eta, low_z, z))**2 * (1+z)**2 * flux

def create_test_array(low_z, flux_low_z, Lpeak_low_z):
    '''Create 'sudo' test array to hold all data with column names.'''
    test_arr = np.array([low_z['eff_m'], flux_low_z[:], low_z['z'],
                        Lpeak_low_z[:]])
    test_dtype = np.dtype([('Eff_M', np.float64), ('Flux', np.float64),
                           ('Rshf', np.float64), ('L_peak', np.float64)])
    test_arr = np.array(list(zip(test_arr[0], test_arr[1], test_arr[2],
                                 test_arr[3])), dtype = test_dtype)
    test_names = str(test_arr.dtype.names)
    test_names = test_names[:9] + ' '*5 + test_names[9:18] + ' '*5 + test_names[18:25] + ' '*2 + test_names[25:34] + ' ' + test_names[34:35]
    print(test_names)
    print(test_arr)
    return test_arr

def show_graphs():
    """Plot the Data to follow what is going on."""
    #complex_map = argand_map(Bounds, Map_Points)

    pyplot.figure()
    pyplot.subplot(211) #Plot enumerated root convergence of the complex plane.
    #img_1 = pyplot.imshow(complex_map[:,:,0], extent = (Bounds)) #Create a greyscale colour map of function.
    pyplot.xlabel('Effective Magnitude')
    pyplot.ylabel('Redshift, z')
    pyplot.title('Figure 1')
    pyplot.scatter(test_arr['Eff_M'], test_arr['Rshf'])

    #pyplot.subplot(122) #Plot convergence time of the complex plane.
    #img_2 = pyplot.imshow(complex_map[:,:,1], extent = (Bounds), norm = matplotlib.colors.PowerNorm(0.65)) #Create a greyscale colour map of function.
    #pyplot.xlabel('Real Component')
    #pyplot.title('Convergence Time')

    #pyplot.suptitle("\n".join(wrap(r"Argand Diagrams of Root Convergence and Convergence Time of the Function $z^{4} - 1$",50)), fontsize=18)
    pyplot.show()



if __name__ == '__main__':
    flux_low_z = mag_to_flux(low_z['eff_m'])
    Lpeak_low_z = flux_to_Lpeak(flux_low_z, low_z['z'], 0.0, low_z = True)
    test_arr = create_test_array(low_z, flux_low_z, Lpeak_low_z)

    Lpeak_limits = (test_arr['L_peak'].min(),test_arr['L_peak'].max())
    print('Min:', Lpeak_limits[0], '\tMax:', Lpeak_limits[1])

    print(np.linspace(Lpeak_limits[0], Lpeak_limits[1], 100))

    show_graphs()
