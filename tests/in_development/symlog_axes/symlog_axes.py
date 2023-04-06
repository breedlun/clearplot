# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:19:31 2015

@author: Ben
"""
import clearplot.figure as cp_fig
import numpy as np

x = -np.flipud(np.logspace(1,5,5))
y = -4.0 * np.abs(x)**0.5 

fig = cp_fig.Figure()
ax = fig.add_axes()
ax.x_scale = 'symlog'
ax.y_scale = 'symlog'
ax.x_label = ['h\,/\,h_o']
ax.y_label = ['e']
ax.plot(x, y, marker_shapes = 'o', marker_edge_widths = 0)
fig.auto_adjust_layout()
fig.save('symlog_axes.pdf')