#!/usr/bin/env python

import matplotlib.pyplot as pl
import numpy as np

 

def planck(lam, T):
    """
    PURPOSE:
        calc planck function
    """

    c = 2.99792458e8 # speed of light
    k = 1.380662e-23 # Boltzmann constant
    h = 6.626180e-34 # Planck constant
 
    return 2*np.pi*h*c*c/(lam**5 * (np.exp(h*c/(lam*k*T))-1.))



def plot_planck_function_for_wavelength_range(lam):
    """
    PURPOSE:
        plot the planck function for a given wavelength range
    INPUT:
        lam: wavelength range
    """

    #constants
    d = 1.49e11      # distance between sun and earth
    r = 1.3914e9/2.  # radius of sun


    pl.figure(1, figsize=(8,5))
    pl.loglog(lam*1e6, planck(lam, 6000)*1e-6, label='6000 K')
    pl.loglog(lam*1e6, planck(lam, 6000)*(r/d)**2*1e-6, ':' )
    pl.loglog(lam*1e6, planck(lam, 300)*1e-6, label='300 K')
    pl.ylim(1e-1,1e9)
    pl.legend()
    pl.xlabel(r'wavelength [$\mu$m]')
    pl.ylabel(r'irradiance [W/(m$^2$ $\mu$m]')
     
    pl.show()
    
    # if you want to save the created figure
    #pl.savefig('planck_functions.png')

    return


if __name__ == '__main__':

    lam=np.arange(0.05, 100, 0.01)*1e-6 # wavelength range

    plot_planck_function_for_wavelength_range(lam)

