#%% imports
import numpy as np
import pandas as pd

# plotting using matplotlib (using plot_bolt_pattern function)
#from bolt_pattern_plots import plot_bolt_pattern

# plotting using bokeh (using plotboltpoints function)
from bolt_pattern_plots_bokeh import plotboltpoints


#%%
def bolt_centroid(points, A=1, return_all_data = False, udf_pivot = False):

    if (type(A) == float) or (type(A) == int):
        A = A * np.ones(len(points[0]))

    if (type(A) == list) or (type(A) == tuple):
        A = np.array(A)
    
    # Coordinates of centroid
    x = points[0]
    y = points[1]
    
    if udf_pivot == False:
        xc = (x*A).sum()/A.sum()
        yc = (y*A).sum()/A.sum()
    else:
        xc, yc = udf_pivot[0], udf_pivot[1]
    
    
    # Distance of the bolt from the pattern centroid
    rcx = x - xc
    rcy = y - yc

    # Centroidal moment of inertia
    Icx = (rcy**2 * A).sum()
    Icy = (rcx**2 * A).sum()
    Icp = Icx + Icy

    # Shortest distance between bolt and centroid
    rcxy = np.sqrt(rcx**2 + rcy**2)

    if return_all_data == False:
        return xc, yc
    elif return_all_data == True:
        return xc, yc, rcx, rcy, Icx, Icy, Icp, rcxy
    else:
        print('error: return_all_data not correctly specified')
        return

#%%
def points(*args, plot = True, A = 1, udf_pivot = False):
    points = np.array(args)
    if points.ndim != 2:
        print('error: (x,y) coordinates not entered correctly')
        return
    points = points[:,0], points[:,1]
    if plot:
        centroid = bolt_centroid(points, A, False, udf_pivot)
        #plot_bolt_pattern(points, centroid, A)
        plotboltpoints(points, centroid)

    
    return points

def circle(r, N, theta_start_deg = 0, plot = True, A = 1, udf_pivot = False):
    alpha = np.deg2rad(theta_start_deg)
    theta = np.linspace(np.pi/2, -3*np.pi/2 + 2*np.pi/N, N)
    points = r*np.cos(-alpha + theta), r*np.sin(-alpha + theta)
    if plot:
        centroid = bolt_centroid(points, A, False, udf_pivot)
        #plot_bolt_pattern(points, centroid, A)
        plotboltpoints(points, centroid)

    return points

def square(x_dist, Nx, Ny, plot = True, A = 1, udf_pivot = False):
 
    return rectangle(x_dist, x_dist, Nx, Ny, plot, A, udf_pivot)

def rectangle(x_dist, y_dist, Nx, Ny, plot = True, A = 1, udf_pivot = False):

    x = np.linspace(start=-x_dist/2, stop=x_dist/2, num=Nx)
    y = np.linspace(start=y_dist/2, stop=-y_dist/2, num=Ny)
       
    y_outer = np.r_[y[0], y[-1]]
    
    x_out = np.r_[x[0].repeat(Ny), x[1:-1].repeat(2), x[-1].repeat(Ny)] 
    y_out = np.r_[y, np.tile(y_outer, Nx-2), y]
    points = x_out, y_out

    
    if plot:
        centroid = bolt_centroid(points, A, False, udf_pivot)
        #plot_bolt_pattern(points, centroid, A)
        plotboltpoints(points, centroid)

    
    return points






#%% Testing

# # points
# p1 = points((1,2), (3, 4), (5, 6))
# p2 = points((1,2), (3,4), (5,6), udf_pivot=(0,0))

# # circle
# p3 = circle(100, 8)
# p4 = circle(100, 6, theta_start_deg=0, udf_pivot=(25, 40))

# # square
# p5 = square(150, 3, 4)
# p6 = square(150, 3, 4, udf_pivot=(-25, -50))

# # rectangle
# p7 = rectangle(150, 300, 3, 5)
# p8 = rectangle(150, 300, 3, 5, udf_pivot = (-50, 50))
# p9 = rectangle(300, 100, 6, 3)

# %%
