# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:40:08 2016

@author: Ben
"""

import clearplot.plot_functions as pf

#Verification that scaling the plot works correctly
[fig, ax, curves] = pf.plot('', [0,1,2], [0,0.1,0.15], \
    x_label = ['x', 'mm'], y_label = ['y', 'mm'], \
    scale_plot = 1.5, font_size = 24)
ax.add_title(r'\mathsf{Scaled\;Plot}')
fig.auto_adjust_layout()
fig.save('scaled_plot')