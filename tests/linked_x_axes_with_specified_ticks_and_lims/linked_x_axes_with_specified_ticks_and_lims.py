# -*- coding: utf-8 -*-
"""
Created on Mon May 30 21:13:08 2016

@author: Ben
"""

import clearplot.figure as cpfig
import numpy as np

#Verification that limits and ticks can be set on the first set of axes
#and do not get reset by the second set of axes.
fig = cpfig.Figure()
ax1 = fig.add_axes()
xa = np.linspace(0,10,10)
ya = np.linspace(0,1,10)
xb = xa
yb = np.linspace(0,20,10)
ax1.x_label = ['x1']
ax1.y_label = ['y1']
ax1.plot(xa, ya)
ax1.x_lim = [0, 5]
ax1.y_tick = 0.25
ax2 = fig.add_axes(link_x_ax = ax1)
ax2.y_label = ['y2']
ax2.y_tick = 5
ax2.plot(xb, yb)
fig.auto_adjust_layout()
fig.save('linked_x_axes_with_specified_ticks_and_lims')