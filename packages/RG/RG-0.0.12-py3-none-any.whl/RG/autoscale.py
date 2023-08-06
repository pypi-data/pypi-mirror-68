#%% Center and scale to unit variance

import numpy as np

def autoscale(X):
    '''
    Autoscale for spectroscopic
    
    INPUT: 
    Spectral matrix: X(m,n) 
    m observations x n variables
    
    OUTPUT:
    Spectral matrix: X
    Vertical mean of X
    Vertical std of X 
    '''
    
    m,n = X.shape
    mx = np.nanmean(X, axis=0)
    stdx = np.nanstd(X, axis=0)
    ax = (X - mx)/stdx
    
    # Remove NaN values occuring when std = 0
    for i in range(1,m):
        for j in range(1,n):
            if np.isnan(ax[i,j]) == 1:
                ax[i,j] = 0
    
    return ax, mx, stdx