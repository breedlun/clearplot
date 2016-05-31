# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:33:52 2016

@author: Ben
"""

import clearplot.figure as cpfig
import numpy as np

#Verification that auto selected limits allow data to exceed limits by a 
#small amount
fig = cpfig.Figure()
ax = fig.add_axes()
ax.x_tick = 5
ax.y_tick = 0.5
ex = ax.exceed_lim * 0.99 * ax.x_tick
ey = ax.exceed_lim * 0.99 * ax.y_tick
x3a = np.arange(-10 - ex, 10 + ex, 0.01)
y3a = (1.0 + ey) * np.sin(x3a)
ax.plot([x3a], [y3a])
fig.auto_adjust_layout()
fig.save('slightly_exceed_limits')