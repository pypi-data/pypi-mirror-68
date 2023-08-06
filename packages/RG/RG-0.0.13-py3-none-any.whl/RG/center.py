#%% Center 

import numpy as np

def center(X):
    '''
    Center spectroscopic data
    
    INPUT: 
    Spectral matrix: X(m,n) 
    m observations x n variables
    
    OUTPUT:
    Spectral matrix: X
    Vertical mean of X
    '''
    
    m,n = X.shape
    mx = np.nanmean(X, axis=0)
    ax = (X - mx)
    
    return ax, mx