#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 21:34:32 2018

@author: ben
"""
import clearplot.figure as cp_fig
import numpy as np

#Verify that changing distance between tick marks works properly
fig = cp_fig.Figure()
ax = fig.add_axes()
x = np.linspace(0,1,5)
y = np.linspace(0,1,5)
ax.plot(x, y)
ax.x_label = ['x']
ax.y_label = ['y']
ax.x_tick_mm = 10
ax.y_tick_mm = 30
fig.auto_adjust_layout()
fig.save('distance_between_tick_marks')