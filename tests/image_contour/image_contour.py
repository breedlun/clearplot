# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:57:26 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np
import matplotlib.mlab as mlab

#Verification that image background contour plot works
delta = 0.025
x = np.arange(-1.5, 1.5 + delta/100, delta)
y = np.arange(-1.5, 1.5 + delta/100, delta)
xa, ya = np.meshgrid(x, y)
r = (xa + 1.5)**2.0 + (ya + 1.5)**2.0
z1 = mlab.bivariate_normal(xa, ya, 1.0, 1.0, 0.0, 0.0)
z2 = mlab.bivariate_normal(xa, ya, 1.5, 0.5, 1, 1)
za = 10.0 * (z2 - z1)
pf.plot_contours('image_contour', xa, ya, za, \
    ['\tau_1', 'kg'], ['\tau_2', 'kg'], \
    x_tick = 0.5, y_tick = 0.5, x_lim = [-1.5, 1.5], y_lim = [-1.5, 1.5], \
    c_label = ['E', 'kJ'], plot_type = 'image', im_interp = 'bilinear')