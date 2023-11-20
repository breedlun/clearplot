# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 21:31:50 2016

@author: Ben
"""

import clearplot.figure as cpfig
import numpy as np

#Verifies that the curve cropping algorithm works properly with markers
x = np.linspace(0,2,11)
y = np.abs(x - 1)
fig = cpfig.Figure()
ax = fig.add_axes()
ax.plot(x, y)
ax.y_tick = 0.1
ax.y_lim = [0.1, 0.5]

fig.auto_adjust_layout()
fig.save('curve_cropping-one_data_pt_outside_lim')