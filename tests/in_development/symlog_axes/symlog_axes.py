# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:19:31 2015

@author: Ben
"""
import clearplot.figure as cp_fig
import numpy as np

x = np.hstack([-np.flipud(np.logspace(-3,2,20)), np.logspace(-3,2,20)])
y = 10 * x

fig = cp_fig.Figure()
ax = fig.add_axes()
ax.x_scale = 'symlog'
ax.y_scale = 'symlog'
ax.x_tick_mm = 20.0
ax.x_lin_half_width = 1e-2
ax.y_lin_half_width = 1e-2
ax.x_lim = [-1e1, 1e2]
ax.x_label = ['h\,/\,h_o']
ax.y_label = ['e']
ax.plot(x, y, marker_shapes = 'o', marker_edge_widths = 0)
fig.auto_adjust_layout()
fig.save('symlog_axes.pdf')