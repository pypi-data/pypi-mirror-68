#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:55:56 2020

@author: ryangosselin
"""

import numpy as np


def emsc(spectra, remove_mean=False):
    """ Performs (basic) extended multiplicative scatter correction to the mean.
    Args:
        spectra <numpy.ndarray>: NIRS data matrix.
    Returns:
        spectra <numpy.ndarray>: Scatter corrected NIR spectra.
    """

    

    spectra = spectra.T
    
    if remove_mean:
        spectra = spectra - np.mean(spectra,axis=0)
        

    wave = np.arange(0,spectra.shape[0],1)    
    p1 = .5 * (wave[0] + wave[-1])
    p2 = 2 / (wave[0] - wave[-1])

    # Compute model terms
    model = np.ones((wave.size, 4))
    model[:, 1] = p2 * (wave[0] - wave) - 1
    model[:, 2] = (p2 ** 2) * ((wave - p1) ** 2)
    model[:, 3] = np.mean(spectra, axis=1)

    # Solve correction parameters
    params = np.linalg.lstsq(model, spectra,rcond=None)[0].T

    # Apply correction
    spectra = spectra - np.dot(params[:, :-1], model[:, :-1].T).T
    spectra = np.multiply(spectra, 1 / np.repeat(params[:, -1].reshape(1, -1), spectra.shape[0], axis=0))

    spectra = spectra.T
    return spectra