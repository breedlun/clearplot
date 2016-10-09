# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:57:26 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np
import matplotlib.mlab as mlab

#Generate the data
delta = 0.025
x = np.arange(-1.5, 1.5 + delta/100, delta)
y = np.arange(-1.5, 1.5 + delta/100, delta)
xa, ya = np.meshgrid(x, y)
r = (xa + 1.5)**2.0 + (ya + 1.5)**2.0
z1 = mlab.bivariate_normal(xa, ya, 1.0, 1.0, 0.0, 0.0)
z2 = mlab.bivariate_normal(xa, ya, 1.5, 0.5, 1, 1)
za = 10.0 ** (5*(z2 - z1))
za = za - np.min(za) + 0.01
#Plot the matrix as an image
pf.plot_matrix('matrix_plot-log_scale.png', xa, ya, za, \
    x_label = ['\tau_1', 'kg'], y_label = ['\tau_2', 'kg'], \
    x_lim = [-1.5, 1.5], y_lim = [-1.5, 1.5], \
    c_label = ['E', 'kJ'], c_scale = 'log')