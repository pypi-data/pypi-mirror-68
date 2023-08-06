#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:53:06 2020

@author: ryangosselin
"""

import scipy

def detrend(spectra, bp=0):
    """ Perform spectral detrending to remove linear trend from data.
    Args:
        spectra <numpy.ndarray>: NIRS data matrix.
        bp <list>: A sequence of break points. If given, an individual linear fit is performed for each part of data
        between two break points. Break points are specified as indices into data.
    Returns:
        spectra <numpy.ndarray>: Detrended NIR spectra
    """
    return scipy.signal.detrend(spectra, bp=bp)