#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 08:10:15 2017

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np

x = np.array([0.0, 1.0, 2.0, 3.0])
y = np.array([0.0, 2.0, 1.0, 3.0])

[fig, ax, curves] = pf.plot('', x, y)

ax.add_v_line(1.0, line_style = '--')
ax.add_h_line(1.0, color = [0,0,1])
ax.add_v_rect(np.array([1.5, 2.5]), edge_width = 1)
ax.add_h_rect(np.array([1.5, 2.5]), color = [0,0.6,0])

fig.save('line_and_rect_that_span_axes.png')