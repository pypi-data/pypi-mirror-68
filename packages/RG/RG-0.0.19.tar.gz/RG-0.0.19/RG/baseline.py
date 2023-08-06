# Linear baseline removal (remove the mean of each spectrum)
import numpy as np

def baseline(spectra):
    """ Removes baseline (mean) from each spectrum.
    Args:
        spectra <numpy.ndarray>: NIRS data matrix.
    Returns:
        spectra <numpy.ndarray>: Mean-centered NIRS data matrix
    """
    spectra = spectra.T
    spectra = spectra - np.mean(spectra, axis=0)
    spectra = spectra.T
    return spectra