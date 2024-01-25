import numpy as np
from numpy import pi
import matplotlib.pyplot as plt

def cylinder(radius,height,jmolout = False, ddaout = False, doplot = True):
    '''
    Function that generates points forming a cylindrical particle in a square 
    computational grid, specifically in the positive octant.

    Parameters
    ----------
    radius : positive integer
        Radius of the cylinder in the computational grid. 
        In principle it can accept any positive integer, but values > 5 are preferred
    
    height : positive integer
        Height of the cylinder (z direction) in the computational grid. 
        
    jmolout : Boolean, optional
        To write a .xyz file for jmol. The default is False.
        
    ddaout : Boolean, optional
        To write a .tgt file for OpenDDA. The default is False.
    
    doplot : Boolean, optional
        To do a plot of the generated particle. The default is True.

    Returns
    -------
    None.

    '''
        
    radius = int(radius)
    input_radius = radius
    
    height = int(height)
    input_height = height
    
    Nangles = 2000
    
    theta_original = np.linspace(0, 2*pi, Nangles, endpoint = True)
    radius_original = np.linspace(0,input_radius,input_radius + 1, endpoint = True)
    height_original = np.linspace(0,input_height, input_height + 1, endpoint = True)
    
    [radius,theta,height] = np.meshgrid(radius_original,theta_original,height_original)
    
    # Make all arrays one dimensional
    radius = radius.flatten()
    theta = theta.flatten()
    height = height.flatten()
    
    # Parametric equations for a cylinder
    xval = radius * np.cos(theta)
    yval = radius * np.sin(theta)
    zval = height
    
    # Shift the points towards the positive octant
    xval = xval - min(xval) + 1
    yval = yval - min(yval) + 1
    zval = zval - min(zval) + 1
    
    Npoints = len(zval)
    print(f'Number of points {Npoints}')
    
    # Convert all arrays to integers
    xval = xval.astype(int)
    yval = yval.astype(int)
    zval = zval.astype(int)
    
    xmax = max(xval)
    ymax = max(yval)
    zmax = max(zval)
    
    occupied_points = np.zeros((xmax + 1,ymax + 1,zmax + 1))
    
    for k in range(0,Npoints):
        occupied_points[xval[k],yval[k],zval[k]] = 1
    
    xval = yval = zval = []
    
    # Retrieve xyz coordinates that are occupied
    x_new, y_new, z_new = np.where(occupied_points == 1)
    
    occupied_points = []
    
    if doplot:
        # Make a scatter plot
        fig = plt.figure(1)
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(x_new,y_new,z_new,c=z_new,cmap = 'Blues')

    Npoints = len(z_new)
    print(f'Number of unique points {Npoints}')
       
    # Write files with locations
    script_name = 'cylinder.py'

    file_noext = 'cylinder_R{}_H{}'.format(input_radius,input_height)
    
    if jmolout:
        
        filename = file_noext + '.xyz'
        f = open(filename,'w')
        f.write(f'{Npoints}\n')
        f.write(f'Cylinder generated with {script_name}\n')
        
        for k in range(0,Npoints):
            f.write('Si {} {} {}\n'.format(x_new[k],y_new[k],z_new[k]))
        
        f.close()
        
        print(f'{filename} written')
    
    if ddaout:
        
        filename = file_noext + '.tgt'
        f = open(filename,'w')
        f.write(f'# Cylinder generated with {script_name}\n')
        f.write(f'# Radius {input_radius}\n# Height {input_height}\n')
        f.write(f'# Number of dipoles {Npoints}\n')
        
        for k in range(0,Npoints):
            f.write('{},{},{},0,0,0\n'.format(x_new[k],y_new[k],z_new[k]))
        
        f.close()
        
        print(f'{filename} written')
        