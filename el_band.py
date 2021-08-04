from el_band_funcs import *
from params import *

"""
The elastic band or path-over-hills method is used to find the minimal energy configuration of a path between two points.

By giving the necessary parameters in the params class of the params.py file (Size of the system, end points of the band, given landscape,...),
one prepares the program.
These informations are passed to the run() function in el_band_funcs, which starts by calling the mapCreator() with a specified function 
for the landscape or importing an external csv.
After that the band is created and as first step linearly interpolated between the end points.
By the scipy algorithm scipy.optimize.minimize, one obtains the global energy minimum and the corresponding local band points, which are afterwards 
plotted above the landscape as heatmap and exported in a png file.

Have fun :)

"""

run(params)