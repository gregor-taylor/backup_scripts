# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 11:10:07 2018
Messing around with gdspy
@author: 0901754T
"""

import numpy as np
import gdspy

print('Using gdspy version ' + gdspy.__version__)
#define cell for polygons
poly_cell = gdspy.Cell('POLYGONS')
#some points for polgon corners
points = [(0,0), (2,2), (2,6), (-6,6), (-6,-6), (-4,-4), (-4,4), (0,4)]
#create the polygon
poly1= gdspy.Polygon(points, 1)
#add it to the cell
poly_cell.add(poly1)
#add another one as before but rotate it
poly2=gdspy.Polygon(points, 1).rotate(np.pi)
poly_cell.add(poly2)
#add a rectangle and a circle
poly_cell.add(gdspy.Rectangle((18,1), (22,2), 2))
poly_cell.add(gdspy.Round((27,2),2, layer=2))
#add a big half doughnut shape
poly_cell.add(
        gdspy.Round(
                (23.5, 7),
                15,
                inner_radius=14,
                initial_angle=2.0 * np.pi / 3.0,
                final_angle=-np.pi / 3.0,
                layer=2))

#PATHS
#add a cell for paths
path_cell = gdspy.Cell('PATHS')
#add a path
path1 = gdspy.Path(1, (0,0))
#create a dict for standard parameters fot the path
spec = {'layer':1, 'datatype':1}
#add a segment og the path
path1.segment(3, '+x', **spec)
#and an arc
path1.arc(2, -np.pi/2.0, np.pi/6.0, **spec)
#and another straight segment
path1.segment(4, **spec)
#and a turn
path1.turn(2, -2.0*np.pi/3.0, **spec)
#and a final segment, taper it out at end
path1.segment(3, final_width=0.5, **spec)
#once finished, add the path to the cell
path_cell.add(path1)

#Add another 2 paths starting where path1 ended
path2=gdspy.Path(0.5, (path1.x, path1.y), number_of_paths=2, distance=1)
#change the spec dict to layer 2 amd add a segment to the 2 paths
spec['layer']=2
path2.segment(3, path1.direction, final_distance=1.5, **spec)
#add a turn, another segment and another turn - then add the path to the cell
path2.turn(2, -2.0 * np.pi /3.0, **spec).segment(4, final_distance=1, **spec)
path2.turn(4,np.pi/6.0, **spec)
path_cell.add(path2)
#add a 3rd path where the last one ended in the -y direction
path3=gdspy.Path(0.5, (path2.x, path2.y))
path3.segment(1, '-y', layer=3)

def spiral(t):
    r = 4-3*t
    theta=5*t*np.pi
    x=4-r*np.cos(theta)
    y=-r*np.sin(theta)
    return(x,y)
def dspiral(t):
    theta = 5*t*np.pi
    dx_dt=np.sin(theta)
    dy_dt=-np.cos(theta)
    return (dx_dt, dy_dt)

path3.parametric(
        spiral, 
        dspiral,
        final_width=lambda t: 0.1 + abs(0.4*(1-2*t)**3),
        number_of_evaluations=600,
        layer=3)
path_cell.add(path3)


gdspy.LayoutViewer()