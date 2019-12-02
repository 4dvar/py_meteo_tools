#!/urs/bin/env python
#! coding:utf8

import sys
import math
import numpy as np
import pylab as pl

# most of the code adapted from pywrfplot
# http://code.google.com/p/pywrfplot/

# PURPOSE: plot raw data of Temperature and Dewpoint in skewT-log(p)-diagram


# define constants

skewness = 37.5
# Defines the ranges of the plot, do not confuse with P_bot and P_top
P_b = 105000.
P_t = 10000. 
dp = 100.
plevs = np.arange(P_b,P_t-1,-dp)

T_zero = 273.15

P_top = 10**4
P_bot = 10**5


L = 2.501e6 # latent heat of vaporization
R = 287.04  # gas constant air
Rv = 461.5  # gas constant vapor
eps = R/Rv

cp = 1005.
cv = 718.
kappa = (cp-cv)/cp
g = 9.81


# constants used to calculate moist adiabatic lapse rate
# See formula 3.16 in Rogers&Yau
a = 2./7.
b = eps*L*L/(R*cp)
c = a*L/R





def SkewTPlot(filename_soundingdata):
    
    pl.figure()
    _isotherms()
    _isobars()
    _dry_adiabats()
    _moist_adiabats()
    _mixing_ratio()
       
    _plot_data(filename_soundingdata)
    
    
    pl.axis([-40,50,P_b,P_t])
    pl.xlabel(r'Temperature ($^{\circ}\! C$)')
    xticks = np.arange(-40,51,5)
    pl.xticks(xticks,['' if tick%10!=0 else str(tick) for tick in xticks])
    pl.ylabel('Pressure (hPa)')
    yticks = np.arange(P_bot,P_t-1,-10**4)
    pl.yticks(yticks,yticks/100)
    
    pl.show()
    pl.close()
    pl.clf()



def _skewnessTerm(P):
    return skewness * np.log(P_bot/P)


def _isotherms():
    for temp in np.arange(-100,50,10):
        pl.semilogy(temp + _skewnessTerm(plevs), plevs,  basey=math.e, \
                     color = ('blue'), \
                     linestyle=('solid' if temp == 0 else 'dashed'), linewidth = .5)
    return


def _isobars():
    for n in np.arange(P_bot,P_t-1,-10**4):
        pl.plot([-40,50], [n,n], color = 'black', linewidth = .5)
    return


def _dry_adiabats():
    for tk in T_zero+np.arange(-30,210,10):
        dry_adiabat = tk * (plevs/P_bot)**kappa - T_zero + _skewnessTerm(plevs)
        pl.semilogy(dry_adiabat, plevs, basey=math.e, color = 'brown', \
                     linestyle='dashed', linewidth = .5)
    return


def es(T):
    """
    PURPOSE:
        Returns saturation vapor pressure (Pascal) at temperature T (Celsius)
        Formula 2.17 in Rogers&Yau
    """
    return 611.2*np.exp(17.67*T/(T+243.5))


def gamma_s(T,p):
    """
    PURPOSE:
        Calculates moist adiabatic lapse rate for T (Celsius) and p (Pa)
        Note: We calculate dT/dp, not dT/dz
        See formula 3.16 in Rogers&Yau for dT/dz, but this must be combined with the dry adiabatic lapse rate (gamma = g/cp) and the 
        inverse of the hydrostatic equation (dz/dp = -RT/pg)
    """
    esat = es(T)
    wsat = eps*esat/(p-esat) # Rogers&Yau 2.18
    numer = a*(T+T_zero) + c*wsat
    denom = p * (1 + b*wsat/((T+T_zero)**2)) 
    return numer/denom # Rogers&Yau 3.16



def _moist_adiabats():
    ps = [p for p in plevs if p<=P_bot]
    for temp in np.concatenate((np.arange(-40.,10.1,5.),np.arange(12.5,45.1,2.5))):
        moist_adiabat = []
        for p in ps:
            temp -= dp*gamma_s(temp,p)
            moist_adiabat.append(temp + _skewnessTerm(p))
        pl.semilogy(moist_adiabat, ps, basey=math.e, color = 'green', \
                     linestyle = 'dashed', linewidth = .5)

    return


def _mixing_ratio():
    
    w = np.array([0.1, 0.4, 1, 2, 4, 7, 10, 16, 24, 32])
    w=w*10**(-3)
    
    for wi in w:
        mr=[]
        for pt in plevs:
            e = pt * wi / (eps + wi)
            T = 243.5/(17.67/np.log(e/611.2) - 1)
            mr.append(T + _skewnessTerm(pt))
            if pt==100000.0: mr_ticks = T + _skewnessTerm(pt)
        pl.semilogy(mr, plevs, basey=math.e, color = 'red', \
                     linestyle = 'dashed', linewidth = 1.0)
        pl.annotate(str(wi*10**3), xy=(mr_ticks, 100000), xytext=(-15.0,5.0), xycoords='data', textcoords='offset points', color='red')

    return


def _windbarbs(speed,theta,p): # in kt
    x = np.cos(np.radians(270-theta)) # direction only
    y = np.sin(np.radians(270-theta)) # direction only
    u = x*speed
    v = y*speed
    
    for item in zip(p,theta,speed,x,y,u,v): 
        print(item)
    
    i=0
    for pi in p*100:
        pl.barbs(45,pi,u[i],v[i])
        i=i+1

    return




def _plot_data(filename_soundingdata):

    p,h,T,Td,rh,m,theta,speed = np.loadtxt(filename_soundingdata,usecols=range(0,8),unpack=True)
    
    pl.semilogy(T+ _skewnessTerm(p*100),p*100,basey=math.e, color=('black'),linestyle=('solid'),linewidth= 1.5)
    
    pl.semilogy(Td+ _skewnessTerm(p*100),p*100,basey=math.e, color=('black'),linestyle=('solid'),linewidth= 1.5)
    
    _windbarbs(speed,theta,p)
    
    return



if __name__ == '__main__':

    # sounding data can be downloaded e.g. from http://weather.uwyo.edu/upperair/sounding.html
    # make sure to only use only the actual sounding data without header/footer

    filename_soundingdata = sys.argv[1]

    SkewTPlot(filename_soundingdata)

    # USAGE: python skewt_logp.py input_data.txt
