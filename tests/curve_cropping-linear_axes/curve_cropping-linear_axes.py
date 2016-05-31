# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:30:41 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np

#Verification that cropping algorithm is working properly
xa = np.arange(-10, 10, 0.5)
ya = 2.0 * np.sin(xa)
yb = np.arange(-2, 2, 0.1)
xb = 7 * np.sin(yb * 3.0 - 1.8) + 1.0
pf.plot('curve_cropping-linear_axes', [xa, xb], [ya, yb], \
    x_lim = [-4, 6], y_lim = [-1.5, 1.5])