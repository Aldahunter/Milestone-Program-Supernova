"""Supernova Milestone Program for Physics Problem Solving."""
import numpy as np
import matplotlib.pyplot as pyplot
import scipy, tkinter
from textwrap import wrap

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
high_z, low_z = data[:42], data[42:] #Split Data into low and high redshift.
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
    """Return peak Luminosity (L_peak).

    Parameters: - flux,
                - redshift (z),
                - comoving coord (eta).

    Note: If low_x = True the returned value is independent of eta.
    """
    return 4 * np.pi * (R_0*S_eta(eta, low_z, z))**2 * (1+z)**2 * flux


def Lpeak_to_distLum(Lpeak, flux):
    """Return distance luminosity (d_L) from peak Luminosity (L_peak) and flux."""
    return (Lpeak / (4*np.pi*flux))**0.5

def redshift_to_distLum(z):
    """Return distance luminosity (d_L) for a given redshift (z)."""
    return (c / H_0) * z * (1.0 + z)


def strarray_add_column(strarray, column_data, column_header, column_dtype, print_array = False):
    """Retun inputted structured array with new column appended to end.

    Parameters: - strarray - structured array, the original array to which new
                             column will be appended;
                - column_data - list (or array) of values for appended column,
                                column_data must be same length as height of
                                strarray;
                - column_header - string for the header to the new column;
                - column_dtype - np.dtype, data type for value in column:
                        + For valid dtypes see np.sctypeDict and np.sctypes;
                - print_array - Boolean (Default: False), outputs to terminal
                                the new column headers and new array.
    """
    if strarray.dtype.fields is None: #Check main_array is a structured array.
        raise ValueError("'strarray' must be a structured numpy array")

    descr = [(column_header, column_dtype)] #Create dtype description for new column.
    rtn_array = np.empty(strarray.shape, dtype=strarray.dtype.descr + descr) #Create empty return array with correct shape and dtype description.

    for column in strarray.dtype.names: #Cycle through each column of input array.
        rtn_array[column] = strarray[column][:] #Copy column values from input array to empty return array.
    rtn_array[column_header] = column_data[:] #Copy values for new column into return array.

    if print_array == True: #Output new array with column headers.
        print(rtn_array.dtype.names, '\n')
        print(rtn_array, '\n')
    return rtn_array #Return the array with added column.


def strarray_rem_column(strarray, column_header, print_array = False):
    """Retun inputted structured array with specified column removed.

    Parameters: - strarray - structured array, the original array to which the
                             column will be removed;
                - column_header - string, the header of the column to be
                                  removed;
                - print_array - Boolean (Default: False), outputs to terminal
                                the new column headers and new array.
    """
    if strarray.dtype.fields is None: #Check main_array is a structured array.
        raise ValueError("'strarray' must be a structured numpy array")

    rtn_descr = [] #Create empty dtype description for returned array.
    for column in strarray.dtype.descr: #Cycle through columns of input array.
        if column_header != column[0]: #Check column header is not the same as the header of the column to be removed.
            rtn_descr.append(column) #Add column's dtype description to returned array's dtype description.

    rtn_array = np.empty(strarray.shape, dtype=rtn_descr) #Create empty return array with correct shape and dtype description.

    for column in rtn_array.dtype.names: #Cycle through each column of input array.
        rtn_array[column] = strarray[column][:] #Copy column values from input array to empty return array.

    if print_array == True: #Output new array with column headers.
        print(rtn_array.dtype.names, '\n')
        print(rtn_array, '\n')
    return rtn_array #Return the array with added column.


def plot_graph(x_axis, y_axis, **kwargs):
    """Plot the Data to follow what is going on.

    Parameters: - x_axis, list (or array) to plot on horizontal axis,
                - y_axis, list (or array) to plot on vertical axis,

                - kwargs:
                         + x_label, string to title horizontal axis,
                         + y_label, string to title vertical axis,
                         + title_lable, string to title the plot,
                         + line, Booleen (Default 'False') to add line to plot,
                         + marker, string to add markers to plot:
                                      # 'o', circle (Default),
                                      # '^', triagnle up,
                                      # 's', square,
                                      # '*', star,
                                      # '+', cross,
                                      # 'x', x,
                                      # 'None', no markers.

                         + trend_line, tuple (x_axis, y_axis) to overlay black
                           line on plot:
                                      # x_axis list (or array) to plot on
                                        horizontal axis,
                                      # y_axis, list (or array) to plot on
                                        vertical axis.
    """
    if 'x_label' in kwargs: pyplot.xlabel(kwargs['x_label']) #Add x_axis if specified.
    if 'y_label' in kwargs: pyplot.ylabel(kwargs['y_label']) #Add y_axis if specified.
    if 'title_label' in kwargs: pyplot.title(kwargs['title_label']) #Add title if specified.

    if 'marker' not in kwargs: kwargs['marker'] = 'o' #Set to default marker if not specified.
    pyplot.scatter(x_axis, y_axis, marker=kwargs['marker']) #Plot scatter with markers.
    if 'line' in kwargs: #Check if 'line' is specified as parameter.
        if kwargs['line'] == True: pyplot.plot(x_axis, y_axis) #If 'line' is true plot lines between markers.print('Line Plotted')

    if 'trend_line' in kwargs:
        pyplot.plot(*kwargs['trend_line'])


def show_graphs(Graph1, *graphs, **kwargs):
    """Plot (multiple) graphs to follow what is going on.

    Parameters: - Graph1 - (subplot, x_axis, y_axis, gr_kwargs):
                         + subplot - 3-digit integer to position subplot,
                         + x_axis - list (or array) to plot on horizontal axis,
                         + y_axis - list (or array) to plot on vertical axis,

                         + gr_kwargs - dictionary of kwargs for plot:
                                # 'x_label' - string to title horizontal axis,
                                # 'y_label' - string to title vertical axis,
                                # 'title_lable' - string to title the plot,
                                # 'line' - Booleen (Default 'False') to add line
                                         to plot,
                                # 'marker' - string to add markers to plot:
                                      * 'o' - circle (Default),
                                      * '^' - triagnle up,
                                      * 's' - square,
                                      * '*' - star,
                                      * '+' - cross,
                                      * 'x' - x,
                                      * 'None' - no markers.

                                # 'trend_line' - tuple (x_axis, y_axis) to overlay
                                               black line on plot:
                                      * x_axis - list (or array) to plot on
                                                 horizontal axis,
                                      * y_axis - list (or array) to plot on
                                                 vertical axis.

                - *graphs - Graph2, ..., GraphN. Arbitary number of graphs to
                            plot as subplots, must be formated as tuple like
                            the first graph (Graph1):
                        + Graph2 - (subplot, x_axis, y_axis, gr_kwargs):
                          .    # Parameters follow same conditions as Graph1.
                          .
                          .
                        + GraphN - (subplot, x_axis, y_axis, gr_kwargs):
                               # Parameters follow same conditions as Graph1.

                - **kwargs:
                                # main_title - string to use for the main
                                               window title.
    """
    pyplot.figure() #Create window to hold graphs.

    subplot, x_axis, y_axis, gr_kwargs = Graph1 #Unpack first graph parameters.
    pyplot.subplot(subplot) #Create subplot for first graph.
    plot_graph(x_axis, y_axis, **gr_kwargs) #Plot first graph.

    for graph in graphs: #Cycle through other graphs.
        if len(graph) < 3: #Raise error if not enough parameters given.
            raise ValueError("Each graph must containt at least (subplot, x_axis, y_axis)")
        elif len(graph) == 3: #Assign parameters for given graph of 3 params.
            subplot, x_axis, y_axis = graph
            gr_kwargs = {} #If no kwargs given for graph make blank.
        else: #Assign parameters for given graph.
            subplot, x_axis, y_axis, gr_kwargs = graph

        pyplot.subplot(subplot) #Create subplot for graph.
        plot_graph(x_axis, y_axis, **gr_kwargs) #Plot graph.

    if 'main_title' in kwargs: #If 'main_title' given add to window.
        pyplot.suptitle("\n".join(wrap(kwargs['main_title'], 50)), fontsize=18)

    pyplot.show() #Show graph(s).
