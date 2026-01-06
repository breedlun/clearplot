# -*- coding: utf-8 -*-
"""
Created on Mon May 30 21:18:22 2016

@author: Ben
"""

import clearplot.figure as cpfig
import numpy as np
    
#Verification that a linear scaled y-axis can share a x-axis with a log scaled
#y-axis.
xa = np.linspace(0, 5, 10)
ya = np.linspace(0, 5, 10)
xb = np.linspace(1, 4, 10)
yb = 10.0**xb
fig = cpfig.Figure()
ax1 = fig.add_axes()
ax1.x_label = ['x']
ax1.y_label = ['y_1']
ax1.plot(xa, ya)
ax2 = fig.add_axes(share_x_ax = ax1)
ax2.y_scale = 'log'
ax2.y_label = ['y_2']
ax2.plot(xb, yb)
fig.auto_adjust_layout()
fig.save('shared_x_axes_with_linear_and_log_y_axes')