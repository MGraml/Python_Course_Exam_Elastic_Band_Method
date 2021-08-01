import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import random

#data = pd.read_csv("./map_data.csv")

x   = np.linspace(-10,10,1000)
X,Y = np.meshgrid(x,x)
Z   = 4*np.exp(-(X+Y)**2)+2*np.exp(-(X-random.randrange(-10,10))**2)


plt.contourf(X,Y,Z)
plt.savefig("map_raw.png")