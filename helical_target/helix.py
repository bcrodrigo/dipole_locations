import numpy as np
from numpy import pi
import matplotlib.pyplot as plt

def conical_spiral(halfangle,hand,turns,pitch,Rmin,r_minor,jmolout = False, ddaout = False, doplot = True):
    '''
    Function that generates points forming a helical particle in a square 
    computational grid, specifically in the positive octant. 
    The particle can be a cylindrical helix (similar to a spring) or a conical-shaped helix. In the latter case, the 
    vertex is at the origin and the helix opens towards the positive z direction.
    
    Parameters
    ----------
    halfangle : floating point positive number (>=0)
        Value in degrees of the half angle cone with respect to the z-axis. It can be zero to generate a cylindrical helical trajectory.
    
    hand : integer (+/- 1)
        Handedness of the helical particle: +1 for Right-handed and -1 for Left-handed.
    
    turns : floating point positive number (> 0)
        Number of turns of the helix. It can be non-integer (i.e. 2.5).
    
    pitch : floating point positive number (> 0)
        Height of one turn of the helical trajectory.
    
    Rmin : floating point positive number (>=0)
        Minimum radius of the helical trajectory, measured from the z-axis. Rmin = 0 for a trajectory starting on the origin.
    
    r_minor : positive integer (> 0)
        Thickness of the helical particle 'wire'.
    
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
      
    # halfangle = 30
    # hand = 1
    # turns = 2
    # pitch = 20
    # Rmin = 50
    # r_minor = 3
    
    # tuple with all input parameters, this will come handy at the end
    input_params = (halfangle,hand,turns,pitch,Rmin,r_minor)
    
    hand = np.sign(hand)
    hand_original = hand
    
    tan_beta_original = np.tan(halfangle*(pi/180))
    tan_beta = tan_beta_original
    phi = np.linspace(0,2*pi*turns,int(100*turns),endpoint = True)
    Nphi = len(phi)
    
    # Parametric equations for a conical helix
    z0 = (pitch/(2*pi))*phi
    
    xval = (Rmin + tan_beta*z0) * np.cos(phi);
    yval = hand*(Rmin + tan_beta*z0) * np.sin(phi);
    zval = z0
    
    if (tan_beta_original != 0):
        zval = zval + Rmin/tan_beta;
    
    # Generate a sphere of radius r_minor
    points_sphere = sphere(r_minor)
    
    # Shift the points towards the positive octant
    xval = xval - min(xval) + 1
    yval = yval - min(yval) + 1
    zval = zval - min(zval) + 1
    
    Npoints = len(zval)
    print(f'\nNumber of points in helical path {Npoints}')
    
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
        
    Npoints = len(z_new)
    
    print(f'Number of unique points in helical parth {Npoints}')
    
    if doplot:
        
        # Make a scatter plot of helical trajectory
        fig = plt.figure(1)
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(x_new,y_new,z_new,c = z_new,cmap ='Blues')
    
    # --> need to figure out a better way to account for the maximum size of 
    # occupied_points array
    
    occupied_points = np.zeros((xmax + 2*r_minor + 10,
                                ymax + 2*r_minor + 10,
                                zmax + 2*r_minor + 10))
    
    Npoints_sphere = len(points_sphere[0,:])
    
    temp = np.repeat(points_sphere,Npoints)
    temp = np.reshape(temp,(3,Npoints_sphere,Npoints))
    
    # loop over the points in the helical path
    for j in range(0,Npoints):
        
        # temp = np.copy(points_sphere)
        
        x0 = x_new[j]
        y0 = y_new[j]
        z0 = z_new[j]
        
        temp[0,:,j] = temp[0,:,j] + x0
        temp[1,:,j] = temp[1,:,j] + y0
        temp[2,:,j] = temp[2,:,j] + z0
    
    # Make multidimensional arrays 1D
    xtemp = temp[0,:,:].flatten()
    ytemp = temp[1,:,:].flatten()
    ztemp = temp[2,:,:].flatten()
    
    temp = []
        
    # fig = plt.figure(3)
    # ax = fig.add_subplot(111, projection = '3d')
    # ax.scatter(xtemp,ytemp,ztemp)
    
    Npoints_target = len(xtemp)
    
    for k in range(0,Npoints_target):
        occupied_points[xtemp[k],ytemp[k],ztemp[k]] = 1
            
    print(f'Initial number of points {Npoints_target}')
    
    # Retrieve xyz coordinates that are occupied
    x_final, y_final, z_final = np.where(occupied_points == 1)
    
    occupied_points = []
        
    # Make a scatter plot
    if doplot:
        fig = plt.figure(2)
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(x_final,y_final,z_final,c=z_final, cmap ='Blues') 
            
    Npoints_final = len(x_final)
    
    print(f'After bitfielding {Npoints_final}')


    # Write files with locations
    script_name = 'helix.py'
    
    if hand_original > 0:
        handedness = 'R'
    else:
        handedness = 'L'
    
    file_noext = 'helix{}_a{}_t{}_p{}_R{}_r{}'.format(handedness,input_params[0],input_params[2],input_params[3],input_params[4],input_params[5])

    if jmolout:
        
        filename = file_noext + '.xyz'
        f = open(filename,'w')
        f.write(f'{Npoints_final}\n')
        f.write(f'Helix generated with {script_name}\n')
        
        for k in range(0,Npoints_final):
            f.write('Si {} {} {}\n'.format(x_final[k],y_final[k],z_final[k]))
        
        f.close()
        
        print(f'{filename} written')
    
    if ddaout:
               
        filename = file_noext + '.tgt'        
        f = open(filename,'w')
        f.write(f'# Helix generated with {script_name}\n')
        f.write(f'# Number of dipoles {Npoints_final}\n')
        f.write('# Half Angle {}\n'.format(input_params[0]))
        f.write('# Handedness {}\n'.format(handedness))
        f.write('# Turns {}\n'.format(input_params[2]))
        f.write('# Pitch {}\n'.format(input_params[3]))
        f.write('# Rmin {}\n'.format(input_params[4]))
        f.write('# r_minor {}\n'.format(input_params[5]))
    

        for k in range(0,Npoints_final):
            f.write('{},{},{},0,0,0\n'.format(x_final[k],y_final[k],z_final[k]))
        
        f.close()
        
        print(f'{filename} written\n')


def sphere(radius,jmolout = False, ddaout = False, doplot = False):
    '''
    Function that generates points forming a spherical particle in a square 
    computational grid, specifically in the positive octant.
    
    Parameters
    ----------
    radius : integer
        Radius of the sphere in the computational grid. 
        In principle it can accept any positive integer, but values > 5 are preferred
        
    jmolout : Boolean, optional
        To write a .xyz file for jmol. The default is False.
        
    ddaout : Boolean, optional
        To write a .tgt file for OpenDDA. The default is False.
    doplot : Boolean, optional
        To do a plot of the generated value
    
    Returns
    -------
    Array with the xyz coordinates forming the spherical particle.
    Note: the array shape is 3 x Npoints
    
    '''
        
    radius = int(radius)
    input_radius = radius
    Nangles = 1000
    
    theta_original = np.linspace(0, pi, Nangles, endpoint = True)
    phi_original = np.linspace(0, 2*pi, Nangles)
    radius_original = np.linspace(0,input_radius,input_radius + 1, endpoint = True)
    
    [radius,theta,phi] = np.meshgrid(radius_original,theta_original,phi_original)
    
    # Make all arrays one dimensional
    radius = radius.flatten()
    theta = theta.flatten()
    phi = phi.flatten()
    
    # Parametric equations for a sphere
    xval = radius * np.sin(theta) * np.cos(phi)
    yval = radius * np.sin(theta) * np.sin(phi)
    zval = radius * np.cos(theta)
    
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
    
    if doplot == True:
        # Make a scatter plot
        fig = plt.figure(1)
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(x_new,y_new,z_new)
    
    Npoints = len(z_new)
    print(f'Number of unique points {Npoints}')
       
    # Write files with locations
    script_name = 'sphere.py'
    
    file_noext = 'sphere_R{}'.format(input_radius)

    if jmolout:
        
        filename = file_noext + '.xyz'
        f = open(filename,'w')
        f.write(f'{Npoints}\n')
        f.write(f'Sphere generated with {script_name}\n')
        
        for k in range(0,Npoints):
            f.write('Si {} {} {}\n'.format(x_new[k],y_new[k],z_new[k]))
        
        f.close()
        
        print(f'{filename} written')
    
    if ddaout:
        
        filename = file_noext + '.tgt'
        f = open(filename,'w')
        f.write(f'# Sphere generated with {script_name}\n')
        f.write(f'# Radius {input_radius}\n')
        f.write(f'# Number of dipoles {Npoints}\n')
        
        for k in range(0,Npoints):
            f.write('{},{},{},0,0,0\n'.format(x_new[k],y_new[k],z_new[k]))
        
        f.close()
        
        print(f'{filename} written')
    
    return np.vstack((x_new,y_new,z_new))