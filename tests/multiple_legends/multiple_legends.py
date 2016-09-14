# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:39:01 2016

@author: Ben
"""

import clearplot.plot_functions as pf

#Verfication that multiple legends can be added to a plot
[fig, ax, curves] = pf.plot('', [0,1], [0,1], 'x', 'y', labels = ['P'], \
    legend = True, legend_loc = 'upper left')
markers = ax.plot_markers([0.25, 0.75], [0.25, 0.75], labels = ['A'], \
    shapes = '+', sizes = 10, edge_widths = 2)
ax.add_legend(curves, loc = 'upper left')
ax.add_legend(markers, loc = 'lower right')
fig.save('multiple_legends')