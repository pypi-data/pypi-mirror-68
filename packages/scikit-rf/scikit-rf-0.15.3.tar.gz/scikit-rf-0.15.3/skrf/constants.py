

'''

.. currentmodule:: skrf.constants
========================================
constants (:mod:`skrf.constants`)
========================================

This module contains constants, numerical approximations, and unit conversions


'''

from scipy.constants import c, micron, mil, inch, centi, milli, nano, micro,pi



# used as substitutes to handle mathematical singularities.
INF = 1e99
ONE = 1.0 + 1/1e14
ZERO = 1e-6

K_BOLTZMANN = 1.38064852e-23
T0 = 290.

# S-parameter definition labels and default definition
S_DEFINITIONS = ['power', 'pseudo', 'traveling']
S_DEF_DEFAULT = 'power'

global distance_dict
distance_dict = {'m':1.,
                 'cm':1e-2,
                 'mm':1e-3,
                 'um':1e-6,
                 'in':inch,
                 'mil': mil,
                 's':c,
                 'us':1e-6*c,
                 'ns':1e-9*c,
                 'ps':1e-12*c,
                 }

def to_meters( d, unit='m',v_g=c):
    '''
    Translate various  units of distance into meters

    

    Parameters
    ------------
    d : number or array-like
        the value
    unit : str
        the unit to that x is in:
        ['m','cm','um','in','mil','s','us','ns','ps']
    v_g : 

    '''
    
    distance_dict = {'m':1.,
                 'cm':1e-2,
                 'mm':1e-3,
                 'um':1e-6,
                 'in':inch,
                 'mil': mil,
                 's':v_g,
                 'us':1e-6*v_g,
                 'ns':1e-9*v_g,
                 'ps':1e-12*v_g,
                 }
                 
                 
    unit = unit.lower()
    try:
        return distance_dict[unit]*d
    except(KeyError):
        raise(ValueError('Incorrect unit'))

