# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:04:55 2015

@author: Ben
"""
import clearplot.figure as cp_fig
import numpy as np

x = np.arange(0,10,0.01)
y = x**2

fig = cp_fig.Figure()
ax = fig.add_axes()
ax.x_lim = [0, 1]

ax.plot(x, y)
fig.save('auto_ax_limits')