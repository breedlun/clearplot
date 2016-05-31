# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:35:35 2016

@author: Ben
"""
import clearplot.plot_functions as pf

#Verification that multiple y axes and linked x axes work properly
[fig, ax1] = pf.plot('', [0,1], [0,1], 'x', 'y1')
ax2 = fig.add_axes(share_x_ax = ax1)
ax2.y_tick = 0.1
ax2.y_label = ['y2']
ax2.plot([0,2], [0,0.3])
ax1.y_lim = [0.0, 0.4]
ax3 = fig.add_axes(link_x_ax = ax1)
ax3.y_label = ['y3']
ax3.plot([0, 0.6], [0, 0.2])
ax3.y_tick = 0.1
ax3.x_lim = [0, 1.5]
fig.auto_adjust_layout()
fig.save('multiple_y_axes-linked_x_axes')