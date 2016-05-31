# -*- coding: utf-8 -*-
"""
Created on Mon May 30 21:15:34 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np

#Verification that the cropping algorithm works properly with log data
#(Select x values that are nearly the same as the limits on a linear scale, 
#but significantly different on a log scale.  Select y values that are totally 
#within the y limits, so that the data exceeds the x limits and not the y 
#limits.)
xa = np.linspace(5.0e-13, 5.0e-6, 20)
ya = np.linspace(1.0e8, 1.0e11, 20)
#(Select x values that are totally within the x limits, so that the data 
#exceeds the y limits and not the x limits.  Select y values that are 
#significantly  bigger/smaller than limits on a linear scale, but are nearly 
#the same on a log scale.)
xb = np.linspace(1.0e-11, 1.0e-8, 20)
yb = np.linspace(1.0e7 - 0.4e6, 1.0e12 + 0.04e12, 20)
pf.plot('curve_cropping-log_axes', \
    [xa, xb], [ya, yb], \
    x_scale = 'log', y_scale = 'log', \
    x_lim = [1.0e-12, 1.0e-7], y_lim = [1.0e7, 1.0e12])