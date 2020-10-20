#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 08:10:15 2017

@author: Ben
"""

import clearplot.plot_functions as pf
import clearplot as cp
import numpy as np

x = np.array([0.0, 1.0, 2.0, 3.0])
y = np.array([0.0, 2.0, 1.0, 3.0])

[fig, ax, curves] = pf.plot('', x, y)

ax.add_v_line(1.0, style = '--')
ax.add_h_line(1.0, color = [0,0,1])
#Matplotlib version 1.4.2 (and presumably 1.4.3) has a bug where axvspan and axhspan only
#accept linestyle = ['solid' | 'dashed' | 'dashdot' | 'dotted'].  If you use  
#linestyle = ['-' | '--' | '-.' | ':' | 'None' | ' ' | ''] you will get
#ValueError: Unrecognized linestyle: -
#To avoid this problem, we use edge_style = 'solid' here.
ax.add_v_rect(np.array([1.5, 2.5]), edge_width = 1, edge_style = 'solid')
ax.add_h_rect(np.array([1.5, 2.5]), color = [0,0.6,0], edge_style = 'solid')

fig.save('line_and_rect_that_span_axes')