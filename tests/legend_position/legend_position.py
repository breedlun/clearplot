#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 21:40:28 2023

@author: ben
"""
import numpy as np
import clearplot.figure as cp_fig

x = np.linspace(0, 1, 20)
y = x**2

fig = cp_fig.Figure()
ax = fig.add_axes()
ax.x_label = ['x']
ax.y_label = ['y']
ax.plot(x,y, labels = ['y'])
ax.add_legend(loc = 'best')
ax.add_legend(loc = 'left')
ax.add_legend(loc = 'center')
ax.add_legend(loc = 'right')
ax.add_legend(loc = 'upper')
ax.add_legend(loc = 'lower')
fig.auto_adjust_layout()
fig.save('legend_position_1.pdf')

fig = cp_fig.Figure()
ax = fig.add_axes()
ax.x_label = ['x']
ax.y_label = ['y']
ax.plot(x,y, labels = ['y'])
ax.add_legend(loc = 'upper left')
ax.add_legend(loc = 'upper middle')
ax.add_legend(loc = 'upper right')
ax.add_legend(loc = 'center left')
ax.add_legend(loc = 'center middle')
ax.add_legend(loc = 'center right')
ax.add_legend(loc = 'lower left')
ax.add_legend(loc = 'lower middle')
ax.add_legend(loc = 'lower right')
fig.auto_adjust_layout()
fig.save('legend_position_2.pdf')

fig = cp_fig.Figure()
ax = fig.add_axes()
ax.x_label = ['x']
ax.y_label = ['y']
ax.plot(x,y, labels = ['y'])
ax.add_legend(loc = 'outside upper left')
ax.add_legend(loc = 'outside upper middle')
ax.add_legend(loc = 'outside upper right')
ax.add_legend(loc = 'upper outside right')
ax.add_legend(loc = 'center outside right')
ax.add_legend(loc = 'lower outside right')
fig.auto_adjust_layout()
fig.save('legend_position_3.pdf')
