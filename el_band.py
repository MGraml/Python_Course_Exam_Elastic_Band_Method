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
    Z = +3*np.exp(-0.1*((X-4)**2+(Y+7)**2))+3*np.exp(-0.1*((X)**2+(Y-8)**2))
    #-1*np.exp(-1*(X)**2)-1*np.exp(-1*(Y-offs)**2) #3*np.exp(-0.1*((X-4)**2+(Y)**2))#-1*np.exp(-(X-offs)**2)-1*np.exp(-(Y-offs)**2)#+np.exp(-1/3*(X+offs)**2)+3*np.exp(-0.01*(Y)**2) #+3*np.exp(-0.1*((X)**2+(Y+7)**2))+3*np.exp(-0.1*((X)**2+(Y-8)**2))#+3*np.exp(-0.01*((Y-offs)**2+(X-10)**2))+3*np.exp(-0.01*((X-offs)**2+(Y-10)**2))
    #-1*np.exp(-(X-offs)**2)-1*np.exp(-(Y-offs)**2)+np.exp(-1/3*(X+offs)**2)+3*np.exp(-0.01*(Y)**2)
    
    plt.contourf(X,Y,Z)
    plt.savefig("map_raw.png")
    #data = pd.DataFrame((X,Y,Z))
    #data.to_csv("map_data.csv")
    #np.save("data_raw",X,Y,Z)
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
    #print(np.shape(band),band)
    X = list(band[::2])
    #print(X)
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
        #print(comp_x)
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
    #poten = 0
    #for i in range(np.size(idx_x)):
        #poten += Z[idx_x[i],idx_y[i]]
    #    poten += -1*np.exp(-0.01*(X)**2)-1*np.exp(-0.01*(Y-offs)**2)

    #X = [band[i][0] for i in range(len(band))]
    #Y = [band[i][1] for i in range(len(band))]
    results = []
    poten   = []
    for idpoint in range(len(X)):
        poten.append(height(X[idpoint],Y[idpoint]))
        if idpoint == 0:
            results.append(k*((X[0]-X[1])**2+(Y[0]-Y[1])**2))
        elif idpoint == len(X)-1:
            results.append(k*((X[-1]-X[-2])**2+(Y[-1]-Y[-2])**2))
        else:
            results.append(k * ((X[idpoint-1]-X[idpoint])**2+(X[idpoint+1]-X[idpoint])**2 + \
                        (Y[idpoint-1]-Y[idpoint])**2 + (Y[idpoint+1]-Y[idpoint])**2))
    #print(np.sum(results),poten)
    return np.sum(poten) + np.sum(results)
    
def height(X,Y):
    return +3*np.exp(-0.1*((X-4)**2+(Y+7)**2))+3*np.exp(-0.1*((X)**2+(Y-8)**2))


N=5000
offs = -3*10/4
#giving the length of the band N and the initial/final endpoint coordinates p
N_band  = 50
p_init  = (10,offs)
p_final = (offs,10)
k=1e-1
#Creating a linear interpolation between the two points as a first guess
band = np.zeros([N_band,2])
band[:,0]   = np.linspace(p_init[0],p_final[0],N_band)
band[:,1]   = np.linspace(p_init[1],p_final[1],N_band)
#band[4,0]   = +offs+0.5
band_list = [band[i,:] for i in range(np.shape(band)[0])]
print(np.shape(band_list),band_list)
print(np.array(band_list).flatten())

#print(band)
#data = pd.read_csv("map_data.csv")
x,y,Z = mapCreation(offs,N=N)

spacing = (max(x)-min(x))/N
bound = [(-10+spacing,10-spacing) for _ in range((N_band-2)*2)]

res = opt.minimize(Energy,band_list[1:-1],args=(band_list[0],band_list[-1],x,y,Z,N,k),bounds=bound,options={'disp':True})

#%%
new_x = np.array(res.x[::2])
new_y = np.array(res.x[1::2])
new_band = np.stack((new_x,new_y))
#print(new_band)
X,Y = np.meshgrid(x,y)
fig = plt.figure()
ax = fig.add_subplot()
cont = ax.contourf(X,Y,Z,levels=25,cmap='gist_heat')
fig.colorbar(cont)
ax.scatter(new_band[0],new_band[1],c='blue',s=10,label='relaxed band')
ax.scatter(band[:,0],band[:,1],c='red',s=1,label='initial band')
ax.set_xlabel('x coordinate of the map')
ax.set_ylabel('y coordinate of the map')
ax.legend()
ax.set_title(f'Test of the band with k={k} for the middle trench')
fig.savefig(f'El_band_k_{k}_mid_trench_new_endpoints2.png')
fig.show()
