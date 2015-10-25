# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 17:36:03 2015

@author: Ben
"""
import clearplot.plot_functions as pf
import numpy as np
import matplotlib.mlab as mlab

delta = 0.025
x1d = np.arange(-1.5, 1.5 + delta/100, delta)
y1d = np.arange(-1.5, 1.5 + delta/100, delta)
x, y = np.meshgrid(x1d, y1d)
z1 = mlab.bivariate_normal(x, y, 1.0, 1.0, 0.0, 0.0)
z2 = mlab.bivariate_normal(x, y, 1.5, 0.5, 1, 1)
z = 10.0 * (z2 - z1)

pf.plot_contours('filled_contours.png', x, y, z, ['\tau_1', 'kg'], \
    ['\tau_2', 'kg'], x_tick = 0.5, y_tick = 0.5, c_label = ['E', 'kJ']);