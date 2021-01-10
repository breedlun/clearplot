# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 17:36:03 2015

@author: Ben
"""
import clearplot.plot_functions as pf
import numpy as np

delta = 0.025
x = np.arange(-2.0, 3.0, delta)
y = np.arange(-2.0, 3.0, delta)
X, Y = np.meshgrid(x, y)
Z1 = np.exp(-X**2 - Y**2)
Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
Z = (Z1 - Z2) * 2

pf.plot_contours('contour_plot-filled.png', X, Y, Z, ['\tau_1', 'kg'], \
    ['\tau_2', 'kg'], x_tick = 0.5, y_tick = 0.5, c_label = ['E', 'kJ']);