# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:37:32 2016

@author: Ben
"""

import clearplot.plot_functions as pf

#Verification that multiple x axes and linked y axes work properly
[fig, ax1, curves] = pf.plot('', [0,1], [0,1], x_label = 'x1', y_label = 'y')
ax2 = fig.add_axes(share_y_ax = ax1)
ax2.x_tick = 0.1
ax2.x_label = ['x2']
ax2.plot([0,0.3], [0,2])
ax1.x_lim = [0.0, 0.4]
ax3 = fig.add_axes(link_y_ax = ax1)
ax3.x_label = ['x3']
ax3.plot([0, 0.2], [0, 0.6])
ax3.x_tick = 0.1
ax3.y_lim = [0, 1.5]
fig.auto_adjust_layout()
fig.save('multiple_x_axes-linked_y_axes')