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
    
    x   = np.linspace(*intv,N)
    X,Y = np.meshgrid(x,x)
    Z = -1*np.exp(-(X-offs)**2)-1*np.exp(-(Y-offs)**2)
    Z = np.where(Z<-1,-1,Z)

    plt.contourf(X,Y,Z)
    plt.savefig("map_raw.png")
    #data = pd.DataFrame(X,Y,Z)
    #data.to_csv("map_data.csv")
    np.save("data_raw",X,Y,Z)
    return x,x,Z

def Energy(band,init,final,x_ext,y_ext,Z_ext,k=1):
    """
    These are both energies: the elastic band part, giving an energy contribution via Hooke's law and the potential energy/height.
    Necessary arguments:
    - band     1D array of tuples
    
    Optional arguments:
    - k     the spring constant, by default set to 1
    """
    #print(init,final)
    #band = np.array(band)
    #print(len(band))
    X = list(band[::2])
    X.insert(0,init[0])
    X.append(final[0])
    Y = list(band[1::2])
    Y.insert(0,init[1])
    Y.append(final[1])
    
    #print(f'X={X}')
    #print(f'Y={Y}')
    
    X = [x_ext[int(np.round(x))] for x in X]
    Y = [y_ext[int(np.round(y))] for y in Y]

    
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
    return np.sum(results)
    



N=1000
offs = -3*10/4
#giving the length of the band N and the initial/final endpoint coordinates p as INDICES
N_band  = 10
p_init  = (999,125)
p_final = (125,999)

x,y,Z = mapCreation(offs,N=N)

print(p_init[0],p_final[0])
#Creating a linear interpolation between the two points as a first guess
band = np.zeros([N_band,2])
band[:,0]   = np.linspace(p_init[0],p_final[0],N_band)
band[:,1]   = np.linspace(p_init[1],p_final[1],N_band)
#band[3,0]   = 600
band_list = [band[i,:] for i in range(np.shape(band)[0])]
#print(band)
#data = pd.read_csv("map_data.csv")


res = opt.minimize(Energy,band_list[1:-1],args=(band_list[0],band_list[-1],x,y,Z),method = 'BFGS',options={'maxiter' : 20, 'eps' : 2.0})

#%%
new_x = np.array(res.x[::2])
new_y = np.array(res.x[1::2])
new_band = np.stack((new_x,new_y))
print(new_band)
plt.contourf(x,y,Z)
x_init = [x[int(round(i))] for i in band[:,0]]
y_init = [y[int(round(i))] for i in band[:,1]]
plt.scatter(x_init,y_init)
#print(x[int(round(new_band[2,0]))])
x_final = [x[int(round(i))] for i in new_band[0,:]]
y_final = [y[int(round(i))] for i in new_band[1,:]]
#print(x_final,y_final,np.shape(x_final))
plt.scatter(x_final,y_final,c='red',s=1)
plt.show()

