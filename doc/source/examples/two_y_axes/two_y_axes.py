# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:12:21 2015

@author: Ben
"""
import clearplot.figure as figure
import numpy as np

xa = np.arange(0,10,0.01)
ya = np.sqrt(xa)
xb = xa
yb = 3.0 * (xb/10)**3 - 2.0 * (xb/10)**2
xc = xa
yc = 1.0/2.0 * xc**2.0

fig = figure.Figure()
ax1 = fig.add_axes()
ax1.plot([xa, xb], [ya, yb])
ax1.x_label = ['A', 'mm^2']
ax1.y_label = ['\alpha,\,\beta', 'kJ']
ax1.y_lim = [-1,'auto']
ax1.add_legend(['\alpha', '\beta'], 'upper left')

ax2 = fig.add_axes(share_x_ax = ax1)
ax2.plot([xc], [yc], line_colors = [0,0,1])
ax2.add_legend(['\gamma'], 'upper right')
ax2.y_lim = [-20, 80]
ax2.y_label = ['\gamma','\mu m']

fig.auto_adjust_layout()
fig.save('two_y_axes.png')