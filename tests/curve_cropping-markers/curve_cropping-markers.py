# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 21:31:50 2016

@author: Ben
"""

import clearplot.figure as cpfig
import numpy as np

#Verifies that the curve cropping algorithm works properly with markers
x = np.linspace(0,2,50)
y = x**3.0
fig = cpfig.Figure()
ax = fig.add_axes()
ax.plot_markers(x, y)
ax.x_lim = [0, 1.0]
fig.auto_adjust_layout()
fig.save('curve_cropping-markers')