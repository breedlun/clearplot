# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:59:22 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np
    
#Generate the data
delta = 0.025
x = np.arange(-2.0, 3.0, delta)
y = np.arange(-2.0, 3.0, delta)
X, Y = np.meshgrid(x, y)
Z1 = np.exp(-X**2 - Y**2)
Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
Z = (Z1 - Z2) * 2

#Plot user specified contours
pf.plot_contours('contour_plot-custom_levels', X, Y, Z, \
    x_label = ['\tau_1', 'kg'], y_label = ['\tau_2', 'kg'], \
    x_lim = [-1, 2], x_tick = 0.5, y_lim = [-1, 2], y_tick = 0.5, \
    c_label = ['E', 'kJ'], plot_type = 'lines', \
    cl_levels = np.linspace(-1.0, 1.0, 6), cl_label_fmt = '%.3f')