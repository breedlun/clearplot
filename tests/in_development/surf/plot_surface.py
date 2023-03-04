# -*- coding: utf-8 -*-
"""
Created on Mon May 30 21:25:49 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np

#3D Surface Plot
x_list = np.linspace(-1.0,1.0,100)
y_list = np.linspace(-1.5,1.5,100)
[x, y] = np.meshgrid(x_list, y_list)
z = -(x*3.0)**2.0 + (y*1.5)**2.0 + 5
pf.plot_surface('surf', x, y, z, x_tick = 1, y_tick = 1, z_tick = 5, \
    z_lim = [-10.0, 10.0], x_lim = [-2.0, 2.0], y_lim = [-2.0, 2.0], \
    light_alt_angle = 90.0, light_azm_angle = 0.0);