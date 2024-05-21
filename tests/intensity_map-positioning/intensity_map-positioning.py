# -*- coding: utf-8 -*-
"""
Created on Mon May 30 21:02:31 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import clearplot.figure as cpfig
import clearplot as cp
import numpy as np

#Verification that the image position is consistent with the contour lines.  
#(This is best seen with a very coarse image.)  Also verify that multiple 
#contour plots can be placed in a figure window
#Generate a coarse data set so that individual image pixels are easily visible.
x = np.array([[0,1,2,3], [0,1,2,3], [0,1,2,3], [0,1,2,3]])
y = np.array([[0,0,0,0], [1,1,1,1], [2,2,2,2], [3,3,3,3]])
z = np.array([[0.25, 0.75, 1.0, 0.75], [0.1, 0.65, 0.5, 0.4], [0.6, 0.3, 0.0, 0.2], [0.7, 0.9, 0.4, 0.6]])
#Create figure window
fig = cpfig.Figure()
#Create axes
ax = fig.add_axes()
ax.x_tick = 1
ax.y_tick = 1
ax.x_lim = [0,3]
ax.y_lim = [0,3]
#Plot intensity map
im_obj = ax.plot_intensity_map(x, y, z)
fig.add_color_bar(im_obj, label = ['z', 'mm'])
fig.auto_adjust_layout()
#Save result
fig.save('intensity_map-positioning')