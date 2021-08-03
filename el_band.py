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
def mapCreation(offs, N = 10000, intv=(-10,10)):
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
    Z = Z = -1*np.exp(-(X-offs)**2)-1*np.exp(-(Y-offs)**2)#+np.exp(-1/3*(X+offs)**2)+3*np.exp(-0.01*(Y)**2) #+3*np.exp(-0.1*((X)**2+(Y+7)**2))+3*np.exp(-0.1*((X)**2+(Y-8)**2))#+3*np.exp(-0.01*((Y-offs)**2+(X-10)**2))+3*np.exp(-0.01*((X-offs)**2+(Y-10)**2))
    #-1*np.exp(-(X-offs)**2)-1*np.exp(-(Y-offs)**2)+np.exp(-1/3*(X+offs)**2)+3*np.exp(-0.01*(Y)**2)
    #Z = np.where(Z<-1,-1,Z)

    plt.contourf(X,Y,Z)
    plt.savefig("map_raw.png")
    #data = pd.DataFrame(X,Y,Z)
    #data.to_csv("map_data.csv")
    np.save("data_raw",X,Y,Z)
    return x,x,Z

def Energy(band,init,final,x_ext,y_ext,Z,N=1000,k=1):
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
    idx_x = []
    idx_y = []
    #Creating Indices for Coordinates in Height
    #print(x_ext)
    spacing = (max(x_ext)-min(x_ext))/N

    for x in X:
        comp_x = np.argwhere(np.where(np.abs(x_ext-x)<0.9*spacing,1,0))
        #print(np.size(comp_x))
        if np.size(comp_x) == 0:
            raise RuntimeError(f"Found no matching indices for x={x}!")
        elif x < 0 :
            idx_x.append(comp_x[0][0])
        else:
            idx_x.append(comp_x[-1][0])
    #print(y_ext)
    for y in Y:
        comp_y = np.argwhere(np.where(np.abs(y_ext-y)<0.9*spacing,1,0))
        #print(np.size(comp_y))
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
    



N=5000
offs = -3*10/4
#giving the length of the band N and the initial/final endpoint coordinates p
N_band  = 50
p_init  = (10,offs)
p_final = (offs,10)
k=1.2
#Creating a linear interpolation between the two points as a first guess
band = np.zeros([N_band,2])
band[:,0]   = np.linspace(p_init[0],p_final[0],N_band)
band[:,1]   = np.linspace(p_init[1],p_final[1],N_band)
#band[4,0]   = +offs+0.5
band_list = [band[i,:] for i in range(np.shape(band)[0])]
#print(band)
#data = pd.read_csv("map_data.csv")
x,y,Z = mapCreation(offs,N=N)

spacing = (max(x)-min(x))/N
bound = [(-10+spacing,10-spacing) for _ in range((N_band-2)*2)]

res = opt.minimize(Energy,band_list[1:-1],args=(band_list[0],band_list[-1],x,y,Z,N,k),method='L-BFGS-B',bounds=bound,jac='2-point',options={'maxiter':80,'disp':True,'eps':spacing})

#%%
new_x = np.array(res.x[::2])
new_y = np.array(res.x[1::2])
new_band = np.stack((new_x,new_y))
#print(new_band)
X,Y = np.meshgrid(x,y)
plt.contourf(X,Y,Z,levels=25,cmap='gist_heat')
plt.colorbar()
plt.scatter(new_band[0],new_band[1],c='green')
plt.scatter(band[:,0],band[:,1],c='red',s=1)
plt.show()
