# PCA with NIPALS

import numpy as np

def PCA(X, nbPC):
    s0, s1 = X.shape
    T = np.zeros((s0, nbPC))
    P = np.zeros((s1, nbPC))
    SSX = np.zeros((nbPC, 1))
    X0 = X # Save a copy
    
    for i in range(0,nbPC):
        error = 1
        t_temp = np.ones((s0, 1))
        t = np.ones((s0, 1))
            
        while error > 1E-10:
            p = (X.T@t)/(t.T@t)
            p = p/np.linalg.norm(p,2)
            # np.linalg.norm(p,2) = np.max(np.sqrt(p.T @ p))
            t = (X@p)/(p.T@p)
            # Check t convergence --------------------
            error = sum(np.power((t-t_temp),2),0) # Squared error
            t_temp = t
            # ----------------------------------------     
        P[:,i] = np.squeeze(p)
        T[:,i] = np.squeeze(t)
        X = X - t@p.T
        
        # Sum of squares -----------
        Xhat = t@p.T
        ssX0 = np.sum(np.sum(X0 * X0)) # Each element squared
        ssX = np.sum(np.sum(Xhat * Xhat))
        ssX = ssX / ssX0
        SSX[i] = ssX
        # --------------------------
        
    return T, P, SSX
