# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:39:01 2016

@author: Ben
"""

import clearplot.plot_functions as pf

#Verfication that multiple legends can be added to a plot
[fig, ax] = pf.plot('', [0,1], [0,1], 'x', 'y', legend = ['P'], \
    legend_loc = 'upper left')
ax.plot_markers([0.25, 0.75], [0.25, 0.75], shapes = '+', sizes = 10, \
    edge_widths = 2)
ax.add_marker_legend(['A'], loc = 'lower right')
fig.save('multiple_legends')