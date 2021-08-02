from numpy.lib.function_base import _parse_input_dimensions
import scipy as sp
from scipy import optimize as opt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import random
import functools



def takeTime (func) :
    """
    Decorator for checking the runtime of single functions.
    Necessary arguments: A function to
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
def mapCreation(offs, N = 1000, intv=(-10,10)):
    """
    Auxiliary tool for generating a csv file with "hilly" landscape in order 
    to test the elastic band with simple data.
    necessary arguments:
    - offs  Offset, where the minimum should be centered around

    optional arguments: 
    - N     Number of grid points in one direction
    - d     interval of the data given as tuple
    - 
    """
    
    x   = np.linspace(intv,N)
    X,Y = np.meshgrid(x,x)
    Z = -1*np.exp(-(X-offs)**2)-1*np.exp(-(Y-offs)**2)
    Z = np.where(Z<-1,-1,Z)

    plt.contourf(X,Y,Z)
    plt.savefig("map_raw.png")
    Z = pd.DataFrame(Z)
    Z.to_csv("map_data.csv")
    return Z

def Energy(band,k=1):
    """
    These are both energies: the elastic band part, giving an energy contribution via Hooke's law and the potential energy/height.
    Necessary arguments:
    - band     1D array of tuples
    
    Optional arguments:
    - k     the spring constant, by default set to 1
    """
    #band = np.array(band)
    #print(len(band))
    X = band[::2]
    Y = band[1::2]
    #X = [band[i][0] for i in range(len(band))]
    #Y = [band[i][1] for i in range(len(band))]
    results = []
    for idpoint in range(len(band)//2):
        if idpoint == 0 or idpoint == len(band)//2-1:
            results.append(0)
        else:
            results.append(k * ((X[idpoint-1]-X[idpoint])**2+(X[idpoint+1]-X[idpoint])**2 + \
                        (Y[idpoint-1]-Y[idpoint])**2 + (Y[idpoint+1]-Y[idpoint-1])**2))
    return np.sum(results)
    




offs = -3*10/4
#giving the length of the band N and the initial/final endpoint coordinates p
N_band  = 5
p_init  = (10,offs)
p_final = (offs,10)
#Creating a linear interpolation between the two points as a first guess
band = np.zeros([N_band,2])
band[:,0]   = np.linspace(p_init[0],p_final[0],N_band)
band[:,1]   = np.linspace(p_init[1],p_final[1],N_band)
band_list = [band[i,:] for i in range(np.shape(band)[0])]
#print(band)
data = pd.read_csv("map_data.csv")


res = opt.minimize(Energy,band_list)
#%%
new_x = np.array(res.x[::2])
new_y = np.array(res.x[1::2])
new_band = np.stack((new_x,new_y))
plt.contourf(data)
plt.scatter(new_band[0],new_band[1])
print(new_band)