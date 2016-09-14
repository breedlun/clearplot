# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:59:22 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np
import matplotlib.mlab as mlab

#Verification that a line only contour plot works and specify contour 
#levels
delta = 0.025
x = np.arange(-1.5, 1.5 + delta/100, delta)
y = np.arange(-1.5, 1.5 + delta/100, delta)
xa, ya = np.meshgrid(x, y)
r = (xa + 1.5)**2.0 + (ya + 1.5)**2.0
z1 = mlab.bivariate_normal(xa, ya, 1.0, 1.0, 0.0, 0.0)
z2 = mlab.bivariate_normal(xa, ya, 1.5, 0.5, 1, 1)
za = 10.0 * (z2 - z1)
pf.plot_contours('contour_lines-custom_levels', xa, ya, za, \
    ['\tau_1', 'kg'], ['\tau_2', 'kg'], x_tick = 0.5, y_tick = 0.5, \
    c_label = ['E', 'kJ'], plot_type = 'lines', c_lim = [-1.5, 1.5], c_tick = 0.5, \
    cl_levels = np.linspace(-1.0, 1.0, 10), cl_label_fmt = '%.3f')