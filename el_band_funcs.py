from scipy.optimize import minimize
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
        
        if func.__name__ == 'run' and args[0].func == 'mortars':
            print("\
            =============================================\n\
                        THIS IS A WARZONE!!! \n\
                YOU ARE ADVANCING ON ENEMY LINES AND \n\
                        LEFT THE TRENCH!             \n\
                WATCH OUT FOR IMPACT OF ENEMY FIRE!!!\n\
                        GOOD LUCK OUT THERE! \n\
            =============================================\n\
            ")
        tic = time.perf_counter()
        result = func(*args, **kwargs)
        toc = time.perf_counter()
        print(f"Time elapsed for {func.__name__}: {(toc - tic):8.3f} s")
        return result
    return wrapper


#Functions to create different potential maps
def trench(X,Y):
    offs=-3*10/4
    Z   =   -1*np.exp(-(X-offs)**2)-1*np.exp(-(Y-offs)**2)
    Z   =   np.where(Z<-1,-1,Z)
    return Z

def mortars(X,Y):
    offs=-3*10/4
    Z   =   +3*np.exp(-0.1*((Y-8)**2+(X)**2))+3*np.exp(-0.1*((X-4)**2+(Y+7)**2))
    return Z


@takeTime
def mapCreation(func,offs=-3*10/4, N = 1000, intv=(-10,10)):
    """
    Auxiliary tool for generating a csv file with "hilly" landscape in order 
    to test the elastic band with simple data.  

    optional arguments: 
    - offs  Offset, where the minimum should be centered around
    - N     Number of grid points in one direction
    - intv  interval of the data given as tuple
    """
    
    x   = np.linspace(*intv,N)
    X,Y = np.meshgrid(x,x)
    
    #Gaussian to make a "energy trench" or several other landscapes
    funcs   =   {'mortars': mortars,'trench':trench}
    Z       =   funcs[func](X,Y)

    #Save the map to "map_data.csv"
    data = pd.DataFrame(Z,index=x,columns=x)
    data.to_csv("map_data.csv")
    
    return


def Energy(band,init,final,x_ext,y_ext,Z,N=1000,k=1):
    """
    These are both energies: the elastic band part, giving an energy contribution via Hooke's law and the potential energy/height.
    Necessary arguments:
    - band      list: tuples as band x,y-coordinates
    - init      tuple: initial band point's coordinates
    - final     tuple: final band point's coordinates
    - x_ext     1D-array: x-coordinates of potential-map
    - y_ext     1D-array: y-coordinates of potential-map
    - Z         2D-array: potential values
    
    Optional arguments:
    - N         resolution of potential map, by default set to 1000
    - k         the spring constant, by default set to 1
    
    Returns:
    - float     total energy of the band configuration
    """
    
    #Assemble the X and Y arrays from the new minimize-data and the fixed end points
    X = list(band[::2])
    X.insert(0,init[0])
    X.append(final[0])
    Y = list(band[1::2])
    Y.insert(0,init[1])
    Y.append(final[1])
    
    #Creating indices for coordinates in potential energy map
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
    
    #Calculate energy contribution of potential background
    energy_pot = 0
    for i in range(np.size(idx_x)):
        energy_pot += Z[idx_y[i],idx_x[i]]

    #Calculate energy contribution of springs between points
    energy_spring = []
    for idpoint in range(len(X)):
        #Contribution of fixed end points
        if idpoint == 0:
            energy_spring.append(k*((X[0]-X[1])**2+(Y[0]-Y[1])**2))
        elif idpoint == len(X)-1:
            energy_spring.append(k*((X[-1]-X[-2])**2+(Y[-1]-Y[-2])**2))
        #Contribution of springs to the points before and after
        else:
            energy_spring.append(k * ((X[idpoint-1]-X[idpoint])**2+(X[idpoint+1]-X[idpoint])**2 + \
                        (Y[idpoint-1]-Y[idpoint])**2 + (Y[idpoint+1]-Y[idpoint])**2))
                
    #Return the total energy
    return energy_pot + np.sum(energy_spring)


@takeTime
def run(params):
    """
    This function is the heart of the whole program.
    It initializes the map (depending on csv_existing by mapCreation or from an external csv).

    It uses parameters from the params class 
    """
    
    #Create map if necessary
    if params.csv_existing == False:
        mapCreation(params.func,N = params.N)
    #Load map
    data = pd.read_csv("map_data.csv",index_col=0)
    x = np.array(data.index,dtype=float)
    y = np.array(data.columns,dtype=float)
    Z = data.values

    #Creating a linear interpolation between the end points as a first guess
    band = np.zeros([params.N_band,2])
    band[:,0]   = np.linspace(params.p_init[0],params.p_final[0],params.N_band)
    band[:,1]   = np.linspace(params.p_init[1],params.p_final[1],params.N_band)
    band_list = [band[i,:] for i in range(np.shape(band)[0])]

    #Specify the value spacing of the map and the bounds
    spacing = (max(x)-min(x))/np.size(x)
    bound = [(min(x)+spacing,max(x)-spacing) for _ in range((params.N_band-2)*2)]
    
    #Arguments for the Energy function: inital, final, x, y, Z, map-resolution, spring-constant
    args = (band_list[0],band_list[-1],x,y,Z,params.N,params.k)
    
    #The scipy.optimize.minimize evaluates the total energy of all band points and minimizes it.
    #The initial and final points need to be given seperatly, so that they don't get minimized.
    #The 'eps'-option sets the absolute step size the algorithm makes.
    #It has to be slightly larger than the map spacing so that new values get evaluated.
    print("Starting minimizer.")
    res = minimize(Energy,band_list[1:-1],args=args,bounds=bound,options={'disp':False,'eps':spacing*1.05})
    print("Minimizer finished.")
    #Extract the minimized coordinates from the flattened result and append the end points
    new_x = list(res.x[::2])
    new_x.append(band_list[-1][0])
    new_x.insert(0,band_list[0][0])
    new_y = list(res.x[1::2])
    new_y.append(band_list[-1][1])
    new_y.insert(0,band_list[0][1])

    #Prepare the plot
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlabel('x coordinate of the map')
    ax.set_ylabel('y coordinate of the map')
    ax.set_title(f'Test of the band with k={params.k} for {params.func}')

    #Plot the potential map
    X,Y = np.meshgrid(x,y)
    cont = ax.contourf(X,Y,Z,levels=25,cmap='gist_heat')
    fig.colorbar(cont)
    
    #Plot the initial band
    ax.scatter(band[:,0],band[:,1],c='red',s=3,label='initial band')
    
    #Plot the minimized band
    ax.scatter(new_x,new_y,c='blue',s=10,label='relaxed band')
    
    #Save the plot
    ax.legend()
    fig.savefig(f'./images/el_band_k={params.k}_map_{params.func}.png')
    
    return