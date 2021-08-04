from numpy.lib.function_base import _parse_input_dimensions
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import functools

def takeTime (func) :
    """
    Decorator for checking the runtime of single functions.
    Necessary arguments: A function to evaluate
    """
    @functools.wraps(func)
    def wrapper (*args, **kwargs) :
        tic = time.perf_counter()
        result = func(*args, **kwargs)
        toc = time.perf_counter()
        print(f"Time elapsed for {func.__name__}: {(toc - tic) * 1000:8.3f} ms")
        return result
    return wrapper

@takeTime
def mapCreation(offs, N = 10000, intv=(-10,10)):
    """
    Auxiliary tool for generating a csv file with "hilly" landscape in order 
    to test the elastic band with simple data.
    necessary arguments:
    - offs  Offset, where the minimum should be centered around

    optional arguments: 
    - N     Number of grid points in one direction
    - intv  interval of the data given as tuple
    """
    
    x   = np.linspace(*intv,N)
    X,Y = np.meshgrid(x,x)
    
    #Gaussian to make a "energy trench"
    Z = -1*np.exp(-(X-offs)**2)-1*np.exp(-(Y-offs)**2)
    
    #Save the map to "map_data.csv"
    data = pd.DataFrame(Z,index=x,columns=x)
    print(data)
    data.to_csv("map_data.csv")
    
    return


def Energy(band,init,final,x_ext,y_ext,Z,N=1000,k=1):
    """
    These are both energies: the elastic band part, giving an energy contribution via Hooke's law and the potential energy/height.
    Necessary arguments:
    - band     1D array of tuples
    
    Optional arguments:
    - k     the spring constant, by default set to 1
    """
    
    #Assemble the X and Y arrays from the new minimize-data and the fixed end points
    X = list(band[::2])
    X.insert(0,init[0])
    X.append(final[0])
    Y = list(band[1::2])
    Y.insert(0,init[1])
    Y.append(final[1])
    
    #Creating indices for coordinates in potential height
    spacing = (max(x_ext)-min(x_ext))/N
    idx_x = []
    idx_y = []
    
    for x in X:
        comp_x = np.argwhere(np.where(np.abs(x_ext-x)<0.9*spacing,1,0))
        if np.size(comp_x) == 0:
            raise RuntimeError(f"Found no matching indices for x={x}!")
        elif x < 0 :
            idx_x.append(comp_x[0][0])
        else:
            idx_x.append(comp_x[-1][0])
            
    for y in Y:
        comp_y = np.argwhere(np.where(np.abs(y_ext-y)<0.9*spacing,1,0))
        if np.size(comp_y) == 0:
            raise RuntimeError(f"Found no matching indices for y={y}!")
        elif y < 0 :
            idx_y.append(comp_y[0][0])
        else:
            idx_y.append(comp_y[-1][0])
    
    #print(idx_x,idx_y)
    poten = 0
    for i in range(np.size(idx_x)):
        poten += Z[idx_x[i],idx_y[i]]

    #X = [band[i][0] for i in range(len(band))]
    #Y = [band[i][1] for i in range(len(band))]
    results = []
    for idpoint in range(len(X)):
        if idpoint == 0:
            results.append(k*((X[0]-X[1])**2+(Y[0]-Y[1])**2))
        elif idpoint == len(X)-1:
            results.append(k*((X[-1]-X[-2])**2+(Y[-1]-Y[-2])**2))
        else:
            results.append(k * ((X[idpoint-1]-X[idpoint])**2+(X[idpoint+1]-X[idpoint])**2 + \
                        (Y[idpoint-1]-Y[idpoint])**2 + (Y[idpoint+1]-Y[idpoint])**2))
    #print(np.sum(results),poten)
    return poten + np.sum(results)


