"""Stupid script to find cartesian coordinates for equally spaced fieldline starting points.
Takes the number of fieldlines desired and radius of circle considered and spits out coordinates"""

import numpy as np

r=15 #radius of circle in vis5d grid #
c=41 #center point of grid (find from vis5d starting point)

#define center of your circle
x0=c
y0=c
z0=c

N=20.0 #number of lines you want

th=2*np.pi/N
fill = 0
set = 1 #set number (jet=0, disk=1, corona=2, plunge=3)

for i in range(0,int(N)):
    x, y, z = x0 + r*np.cos(th*i), y0, z0+r*np.sin(th*i)
    print x,y,z, fill, set
