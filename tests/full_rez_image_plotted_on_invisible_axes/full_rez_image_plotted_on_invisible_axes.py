# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:54:29 2016

@author: Ben
"""

import clearplot.figure as cpfig
import clearplot as cp
import numpy as np

#Verification that invisible axes work correctly and that we can save an image
#at full resolution as a png
delta = 0.01
x = np.arange(-1.5, 1.5 + delta/100, delta)
y = np.arange(-1.5, 1.5 + delta/100, delta)
xa, ya = np.meshgrid(x, y)
r = (xa + 1.5)**2.0 + (ya + 1.5)**2.0
size = np.array(r.shape) * 1.0 / cp.params.dpmm
fig = cpfig.Figure()
ax = fig.add_invisible_axes(position = [0,0], size = size)
ax.x_lim = [0, r.shape[0]]
ax.y_lim = [0, r.shape[1]]
ax.add_image(r)
fig.auto_adjust_layout()
fig.save('full_rez_image_plotted_on_invisible_axes.png')