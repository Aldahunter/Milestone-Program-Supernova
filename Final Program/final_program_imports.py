import numpy as np, matplotlib.pyplot as pyplot, scipy, tkinter, warnings
from textwrap import wrap
from scipy import optimize, integrate
from copy import deepcopy

### Define Constants ###
K = 0 # Curvature of Universe can be: 1(closed), 0(flat), -1(open).
m_0 = -20.45 # Gives flux in units: erg·cm⁻²·s⁻¹·Å⁻¹.
H_0 = 74.8 / 3.086e19 # Current Hubble Flow in units: s⁻¹ (or recent data from 74.8 ± 3.1 km s−1 Mpc−1, Riess et al. 2011: https://arxiv.org/pdf/1103.2976.pdf)
R_0 = 4.4e26 # Current raidus of observable universe in units: m.
c = 2.99792458e8 # Speed of light in units: m*s⁻¹

### Load Data ###
folder = "/media/alex/Shared/University/Physics/Year 3/Physics Problem Solving\
/Computing Project/Programming/Milestone-Program-Supernova/"
dtype = np.dtype([('name', np.str_, 16), ('z', np.float64, 1),
                  ('mag', np.float64, 1), ('m_err', np.float64, 1),
                  ('dataset', np.str_, 16)])
all_data = np.loadtxt(folder+"Union 2.1 SNIa Data/All SNe Union2.1.txt",
                      dtype=dtype, delimiter=' , ')
all_data = all_data[np.argsort(all_data['z'])]


### Physics Functions ###
def S_eta(eta, low_z = False, z = 0.0):
    """Return the comoving coordinate (η, dimensionless), depending on the \
    curvature of space."""
    if low_z == True:
        if K == 0: return (c*z)/(H_0*R_0)
    else:
        if K == 0: return eta
        elif K == 1: return np.sin(eta)
        elif K == -1: return np.sinh(eta)
        else: raise ValueError("K must be one of: 1, 0, -1")

def mag2Lp(mag, z, eta, low_z = False):
    """Return peak Luminosity (erg·s⁻¹·Å⁻¹) for a given effective magnitude \
    (dimensionless) and redshift (dimensionless)."""
    flux = 10**((m_0 - mag)/2.5)
    return 4 * np.pi * (R_0*S_eta(eta, low_z, z))**2 * (1+z)**2 * flux * 1e4

def Lp2mag(Lp, z, eta, low_z = False):
    """Return the effective magnitude (dimensionless) for a given peak \
    Luminosity (erg·s⁻¹·Å⁻¹) and redshift (dimensionless)."""
    flux = Lp / (4 * np.pi * (R_0*S_eta(eta, low_z, z))**2 * (1+z)**2) * 1e-4
    return m_0 - 2.5*np.log10(flux)

def z2H(z, omega, w = -1, R = R_0, om_M0 = 'flat'):
    """Return the Hubble Parameter (H, s⁻¹) for a given redshift (z, \
    dimensionless) and Ω_D.E. (omega, dimensionless)."""
    a = 1 / (1 + z)
    if om_M0 == 'flat': om_M0 = 1.0 - omega
    return H_0 * (om_M0/a**3 + omega/a**(3*(1+w)) - (K*c**2)/R**2)**0.5

def z2eta(z, omega, w = -1, R = R_0, om_M0 = 'flat'):
    """Return the comoving coordinate (dimensionless) for a given redshift \
    (z, dimensionless) and Ω_D.E. (omega, dimensionless)."""
    z = np.array(z)
    etas = np.empty(z.shape)
    int_fn = lambda z, omega, w, R, om_M0: 1.0 / z2H(z, omega, w, R, om_M0)
    int_fn_params = (omega, w, R, om_M0) # Parameters for function to integrate.
    with warnings.catch_warnings(): # Catch 'IntegrationWarning'.
        warnings.simplefilter('ignore')
        for n, n_z in enumerate(z):
            etas[n] = (c/R_0) * integrate.quad(int_fn, # int_{0}^{z} 1/H(z') dz'
                                               0.0, n_z, args=int_fn_params)[0]
    return etas

def omega2mag(omega, z, Lp, w = -1, R = R_0, om_M0 = 'flat'):
    """Return the effective magnitude (dimensionless) for a given Ω_D.E. \
    (omega, dimensionless), redshift (z, dimensionless) and D.E. parameter \
    (w = -1, dimesionless)."""
    mags = Lp2mag(Lp, z, z2eta(z, omega, w, R , om_M0), low_z = False)
    return mags

def decelerate_param(omega, z, w = -1, om_M0 = 'flat'):
    """Return the deceleration parameter (q, dimensionless) for a given \
    Ω_D.E. (omega, dimensionless), redshift (z, dimensionless) and D.E. \
    parameter (w = -1, dimesionless). Note: In a flat universe if q < 0, then \
    it is accelerating"""
    DE_parm = omega*(1 + z)**(3+3*w)
    if om_M0 == 'flat': om_M0 = 1.0 - omega
    M_param = om_M0*(1 + z)**3
    return ((3.0/2.0) * (DE_parm*(1 + w) + M_param)/(DE_parm + M_param)) - 1.0

def universe_age(omega, w = -1.0, R = R_0, om_M0 = 'flat'):
    """Returns the age of the universe (years) for a given Ω_D.E. \
    (omega, dimensionless) and D.E. parameter (w = -1, dimesionless)."""
    int_fn = lambda z, omega, w, R, om_M0: (z2H(z,omega,w,R,om_M0) * (1+z))**-1
    int_fn_params = (omega, w, R, om_M0) # Parameters for function to integrate.
    with warnings.catch_warnings(): # Catch 'IntegrationWarning'.
        warnings.simplefilter('ignore')
        age = integrate.quad(int_fn, 0.0, np.inf, args=int_fn_params)[0]
    return age * 3.168895541e-8 #Convert from seconds to years.



### Stats Functions ###
def calc_chi(exp_data, obs_data, err_data):
    """Calculate the χ² (dimensionless) between the observed (collected) data \
    and the expected (model) data."""
    return np.sum((obs_data - exp_data)**2 / err_data**2)

def minimise_fn(dyn_param, model_fn, model_params, obs_data, err_data):
    """Arbitary function used to calculate minimised chi squared, where \
    'model_fn' is the function to obtain the expected values."""
    model_values = model_fn(dyn_param, *model_params)
    return calc_chi(model_values, obs_data, err_data)

def minimise_chi_1D(model_fn, dyn_param, model_params, obs_data, err_data):
    """Returns the reduced minimised chi squared, and its respective dyn_param \
    and error in this parameter."""
    args = (model_fn, model_params, obs_data, err_data)
    with warnings.catch_warnings(): # Catch 'IntegrationWarning' warnings.
        warnings.simplefilter('ignore') # Surpress warnings from printing.
        bestfit_param = optimize.minimize(minimise_fn, dyn_param, args,
                                          method='Nelder-Mead').x[0]
        chisq_min = minimise_fn(bestfit_param, *args)
        # Find error in parameter.
        func = lambda var : np.abs(minimise_fn(var, *args) - (chisq_min + 1.0))
        param_bound = optimize.minimize(func, bestfit_param,
                                        method='Nelder-Mead').x[0]
        err_param = np.abs(param_bound - bestfit_param)
    return chisq_min/float(obs_data.size), bestfit_param, err_param

def minimise_chi_2D(model_fn, dyn_params, model_params, obs_data, err_data,
                    err_sensitivity = 0.015, err_stats = True):
    """Returns the reduced minimised chi squared, and the two respective \
    dyn_params and error in this parameter."""
    args = (model_fn, model_params, obs_data, err_data)
    with warnings.catch_warnings(): # Catch 'IntegrationWarning' warnings.
        warnings.simplefilter('ignore') # Surpress warnings from printing.
        bestfit_params = optimize.minimize(minimise_fn, dyn_params, args,
                                          method='Nelder-Mead').x
        chisq_min = minimise_fn(bestfit_params, *args)
        chi_red = chisq_min/float(obs_data.size)

        # Find error in parameters #
        if err_stats == True:
            # Parameter 0
            fn_0a = lambda p1, p2 : np.abs(minimise_fn([p1, p2], *args) - (chisq_min + 1.0))
            fn_0b = lambda p2, p1 : minimise_fn([p1, p2], *args)
            param0_bound = deepcopy(bestfit_params)
            param0_bound[0] = optimize.minimize(fn_0a, param0_bound[0],
                                             args=(param0_bound[1]),
                                             method='Nelder-Mead').x[0]
            param0_frdif = 1.0 # Setup the fractional differences.
            while param0_frdif > err_sensitivity:
                old_param0 = param0_bound[0]
                param0_bound[1] = optimize.minimize(fn_0b, param0_bound[1],
                                                    args=(param0_bound[0]),
                                                    method='Nelder-Mead').x[0]
                param0_bound[0] = optimize.minimize(fn_0a, param0_bound[0],
                                                    args=(param0_bound[1]),
                                                    method='Nelder-Mead').x[0]
                param0_frdif = np.abs((old_param0-param0_bound[0])/param0_bound[0])
            err_param0 = np.abs(param0_bound[0] - bestfit_params[0])
            # Parameter 1
            fn_1a = lambda p2, p1 : np.abs(minimise_fn([p1, p2], *args) - (chisq_min + 1.0))
            fn_1b = lambda p1, p2 : minimise_fn([p1, p2], *args)
            param1_bound = deepcopy(bestfit_params)
            param1_bound[1] = optimize.minimize(fn_1a, param1_bound[1],
                                             args=(param1_bound[0]),
                                             method='Nelder-Mead').x[0]
            param1_frdif = 1.0 # Setup the fractional differences.
            while param1_frdif > err_sensitivity:
                old_param1 = param1_bound[1]
                param1_bound[0] = optimize.minimize(fn_1b, param1_bound[0],
                                                    args=(param1_bound[1]),
                                                    method='Nelder-Mead').x[0]
                param1_bound[1] = optimize.minimize(fn_1a, param1_bound[1],
                                                    args=(param1_bound[0]),
                                                    method='Nelder-Mead').x[0]
                param1_frdif = np.abs((old_param1-param1_bound[1])/param1_bound[1])
            err_param1 = np.abs(param1_bound[1] - bestfit_params[1])
    if err_stats == True:
        return chi_red, bestfit_params, np.array([err_param0, err_param1])
    else:
        return chi_red, bestfit_params



### Plotting Functions ###
def map2D(fn_2D, X, Y, fn_args=(), fn_kwargs={}, perc_step = 0.25, thread=None):
    "Returns the z values for the function ('fn_2D') over the x and y \
    values ('X' & 'Y') in the form: z = Z[x,y]."

    if thread != None: # 0 <= n_thread < threads
        n_thread, threads = thread[0], thread[1]
    else: n_thread, threads = 0, 1

    Z = np.zeros((X[n_thread::threads].size, Y.size))
    counter = 0
    perc = 0
    ticker = 0
    for ix, x in enumerate(X[n_thread::threads]):
        for iy, y in enumerate(Y):
            z = fn_2D(x, y, *fn_args, **fn_kwargs)
            Z[ix, iy] = z

            counter += 1.0
            perc = (counter / Z.size) * 100
            if perc > ticker * perc_step:
                ticker += 1
                print("Calculted: {: 6.2f}".format(perc))
    return Z
