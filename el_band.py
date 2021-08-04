from numpy.lib.function_base import _parse_input_dimensions
import scipy as sp
from scipy import optimize as opt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import random
import functools

import el_band_funcs.py

N=5000
offs = -3*10/4
#giving the length of the band N and the initial/final endpoint coordinates p
N_band  = 50
p_init  = (7.5,-10)
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
mapCreation(offs, N = N)
data = pd.read_csv("map_data.csv",index_col=0)
X = np.array(data.index,dtype=float)
Y = np.array(data.columns,dtype=float)
Z = data.values

spacing = (max(x)-min(x))/N
bound = [(-10+spacing,10-spacing) for _ in range((N_band-2)*2)]

res = opt.minimize(Energy,band_list[1:-1],args=(band_list[0],band_list[-1],x,y,Z,N,k),bounds=bound,options={'disp':True,'eps':spacing*1.05})

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
fig.savefig(f'El_band_k_{k}_mid_trench_new_endpoints2_numerical.png')
fig.show()
