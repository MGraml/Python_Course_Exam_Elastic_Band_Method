from numpy.lib.function_base import _parse_input_dimensions
import scipy as sp
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

def T(band,idx,k=1):
    """
    This is the elastic band part, giving an energy contribution via Hooke's law.
    Necessary arguments:
    - band  the whole band
    - idx   the currently used index
    
    Optional arguments:
    - k     the spring constant, by default set to 1
    """
    results = []
    if idx == 0 or idx == np.size(band,axis=0):
        results.append(0)
    else:
        results.append(k * ((band[idx-1,0]-band[idx,0])**2+(band[idx+1,0]-band[idx,0])**2 + \
                    (band[idx-1,1]-band[idx,1])**2 + (band[idx+1,1]-band[idx,1])**2))
    return results





offs = -3*10/4
#giving the length of the band N and the initial/final endpoint coordinates p
N_band  = 100
p_init  = (10,offs)
p_final = (offs,10)
#Creating a linear interpolation between the two points as a first guess
band = np.zeros([N_band,2])
band[:,0]   = np.linspace(p_init[0],p_final[0],N_band)
band[:,1]   = np.linspace(p_init[1],p_final[1],N_band)
#print(band)
data = pd.read_csv("./map_data.csv")

#By introducing the specific map and the corresponding height/pot. energy, we can combine it with the pot energy of the band
# and obtain the effective U
U = np.empty(np.shape(band))
# Here we have to identify the index of the band with "real" coordinates on the map



for idx in range(N_band):
    U = T(band,idx) + data[]