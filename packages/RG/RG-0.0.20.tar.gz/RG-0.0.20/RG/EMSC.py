# EMSC: extended multiplicative scatter correction to the mean

import numpy as np


def EMSC(spectra, remove_mean=False):
    '''
    
    EMSC: extended multiplicative scatter correction to the mean
    [X_emsc] = EMSC(X)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    remove_mean [1 x k] <numpy.ndarray>
        optional input
        remove the mean of the spectra
    
    OUTPUT
    X_emsc [n x k] 
        preprocessed spectra
       
    '''

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