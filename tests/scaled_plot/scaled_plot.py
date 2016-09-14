# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:40:08 2016

@author: Ben
"""

import clearplot.plot_functions as pf

#Verification that scaling the plot works cprrectly
pf.plot('scaled_plot', [0,1,2], [0,0.1,0.15], \
    x_label = ['x', 'mm'], y_label = ['y', 'mm'], \
    scale_plot = 1.5, font_size = 24)