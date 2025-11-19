# -*- coding: utf-8 -*-
"""
Created on Mon May 30 21:11:27 2016

@author: Ben
"""

import clearplot.plot_functions as pf

#Verification that duplicate legend labels are automatically removed
xa = [0,1]
xb = [0,1]
xc = [0,1]
xd = [0,1]
xe = [0,1]
xf = [0,1]
ya = [0,0.1]
yb = [0,0.2]
yc = [0,0.3]
yd = [0,0.4]
ye = [0,0.5]
yf = [0,0.6]
pf.plot('duplicate_legend_labels', \
    [xa, xb, xc, xd, xe, xf], \
    [ya, yb, yc, yd, ye, yf], \
    curve_colors = [[1,0,0], [0,1,0], [0,1,0], [0,0,1], [0,0,1], [0,0,1]],\
    curve_widths = [1,2,2,3,3,3], \
    curve_styles = ['-', '--', '--', ':', ':', ':'],\
    labels = [r'\Omega_1', r'\Omega_2', r'\Omega_2', \
    r'\Omega_3', r'\Omega_3', r'\Omega_3'], legend = True)