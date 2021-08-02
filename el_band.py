import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import random



def takeTime (func) :
    def wrapper (*args, **kwargs) :
        tic = time.perf_counter()
        result = func(*args, **kwargs)
        toc = time.perf_counter()
        print(f"Time elapsed: {(toc - tic) * 1000:8.3f} ms")
        return result
    return wrapper

def mapCreation():
    N = 1000
    d = 10
    offs = -3*d/4
    x   = np.linspace(-d,d,N)
    X,Y = np.meshgrid(x,x)
    Z = -1*np.exp(-(X-offs)**2)-1*np.exp(-(Y-offs)**2)
    Z = np.where(Z<-1,-1,Z)

    plt.contourf(X,Y,Z)
    plt.savefig("map_raw.png")
    Z = pd.DataFrame(Z)
    Z.to_csv("map_data.csv")
    return Z

data = pd.read_csv("./map_data.csv")