# -*- coding: utf-8 -*-
"""
Created on Mon May 30 21:20:05 2016

@author: Ben
"""

import clearplot.figure as cpfig
import numpy as np

#Verification of natural log y-axis
x = np.linspace(0, 2, 50)
y = np.exp(3*x)
fig = cpfig.Figure()
ax = fig.add_axes()
ax.plot(x, y)
ax.y_scale = 'log'
ax.y_scale_log_base = np.e
fig.auto_adjust_layout()
fig.save('natural_log_y_axis')