import numpy as np
class params:
    """
    In this file all user input is gathered.
    Parameter:
        Systemsizes
        - N             -   Size of one axis of the by the mapCreation()-func created map
        - N_band        -   Number of points in the elastic band

        - p_init        -   Custom initial point for start of the band interpolation
        - p_final       -   Custom final point for start of the band interpolation

        - k             -   Strength of the elastic band - has to chosen carefully and dependent on the system (in most cases around 0.1 - 10)

        - csv_existing  -   Boolean for enabling own csv data - set to True if you provide a .csv (be careful about the format!) with own parameters in X,Y and Z.
        - func          -   Function, which is, used IF csv_existing == False, for the creation of the map. Given as string, currently available are 'mortars' and 'trench'

    """
    N                   =       1000            
    N_band              =       50

    
    p_init              =       (7.5,-10)
    p_final             =       (-7.5,10)

    k                   =       0.1    

    csv_existing        =       False 
    func                =       "mortars"