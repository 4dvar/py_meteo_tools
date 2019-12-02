#!/usr/bin/env python
#! coding:utf8

import sys
import numpy as np

# approximation valid for
# 0 degrees Celsius < T < 60 degrees Celcius
# 1% < RH < 100%
# 0 degrees Celcius < Td < 50 degrees Celcius 

# constants
a = 17.271
b = 237.7 # in units of degrees Celcius


def dewpoint_approximation(T,RH):
    """
    PURPOSE:
        approximate the dewpoint given temperature and relative humidty
    INPUT:
        T: temperature
        RH: relative humidity
    """

    Td = (b * gamma(T,RH)) / (a - gamma(T,RH))
    
    return Td



def gamma(T,RH):
    """
    PURPOSE:
        helper function used to calc. dewpoint
    INPUT:
        T: temperature
        RH: relative humidity
    """
    
    g = (a * T / (b + T)) + np.log(RH/100.0)
    
    return g



if __name__ == '__main__':
    
    # sys.argv[0] is program name
    T=float(sys.argv[1])
    RH=float(sys.argv[2])

    Td = dewpoint_approximation(T,RH)
    print('T, RH: '+str(T)+u'°C, '+str(RH)+'%')
    print('Td: '+str(Td))


    # USAGE: python dewpoint.py T RH
    # e.g. python dewpoint.py 10 98