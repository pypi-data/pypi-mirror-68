# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 09:25:27 2020

@author: yoelr
"""
from numba import njit
import sys

__all__ = ('njitable', 'speed_up')

#: All njitable functions
njitables = []

def njitable(f=None, **options):
    """
    Decorate function as 'njitable'. All 'njitable' functions must be able to 
    be compiled by Numba's njit decorator.
    """
    if not f: return lambda f: njitable(f, **options)
    njitables.append((f, options))
    return f

def speed_up():
    """
    Speed up simulations by jit compiling all functions registered as 'njitable'.
    
    See also
    --------
    njitable
    
    Notes
    -----
    Several computation-heavy functions in Thermosteam and BioSTEAM are already marked as 'njitable'.
    This function serves to cut down the time required to perform Monte Carlo analysis.
    
    When running a simulation for the first time, the simulation will take much longer.
    However, every simulation after the first will be about 35% faster.
    
    """
    for f, options in njitables:
        module = sys.modules[f.__module__]
        setattr(module, f.__name__, njit(f, **options))
    njitables.clear()