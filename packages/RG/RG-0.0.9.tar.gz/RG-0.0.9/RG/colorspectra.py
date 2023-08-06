# Plot X spectra with colorcode according to y

import numpy as np
import matplotlib.pyplot as plt

def colorspectra(X,y):
    # Plot - color by lines
    [s0,s1]=X.shape
    # Add column listing the original order of y
    order = np.arange(0,s0,1)
    order = (order[np.newaxis]).T
    color = plt.cm.inferno(np.linspace(0,0.9,s0))
    ycolor = np.concatenate((order,y),axis=1)
    # Sort "y" by increasing value
    ycolor=ycolor[np.argsort(ycolor[:,1])]
    # Add colormap
    ycolor = np.concatenate((ycolor,color),axis=1)
    # Sort "order" by increasing value to return to original order
    ycolor=ycolor[np.argsort(ycolor[:,0])]
    # Now the colormap is sorter according to y
    
    # Using contourf to provide my colorbar info, then clearing the figure
    plt.figure()
    mymap = plt.cm.inferno
    Z = [[0,0],[0,0]]
    ymin, ymax = (np.floor(np.min(y)), np.ceil(np.max(y)))
    ymin = int(ymin)
    ymax = int(ymax) 
    levels = np.arange(ymin,ymax,(ymax-ymin)/100)
    CS3 = plt.contourf(Z, levels,cmap=mymap)
    plt.close()
        
    fig = plt.figure()
    for i in range(s0):
        x = X[i,:]
        plt.plot(x.T, color=color[i])
    plt.colorbar(CS3)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('wavelength',fontsize=16)
    plt.ylabel('intensity',fontsize=16)
    plt.show()
    count = int(np.round(1000*np.random.rand(1),0))
    plt.tight_layout()
    #name = 'plot colors'+str(count)+'.png'
    #name = str(name)
    #print(name)
    #fig.savefig('plot colors'+str(count)+'.png',dpi=200)