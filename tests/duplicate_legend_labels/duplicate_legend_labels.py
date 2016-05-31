# -*- coding: utf-8 -*-
"""
Created on Mon May 30 21:11:27 2016

@author: Ben
"""

import clearplot.plot_functions as pf

#Verification that duplicate legend labels are automatically removed
x19a = [0,1]
x19b = [0,1]
x19c = [0,1]
x19d = [0,1]
x19e = [0,1]
x19f = [0,1]
y19a = [0,0.1]
y19b = [0,0.2]
y19c = [0,0.3]
y19d = [0,0.4]
y19e = [0,0.5]
y19f = [0,0.6]
[fig, ax] = pf.plot('', [x19a, x19b, x19c, x19d, x19e, x19f], \
    [y19a, y19b, y19c, y19d, y19e, y19f], \
    curve_colors = [[1,0,0], [0,1,0], [0,1,0], [0,0,1], [0,0,1], [0,0,1]],\
    curve_widths = [1,2,2,3,3,3], curve_styles = ['-', '--', '--', ':', ':', ':'])
ax.add_legend(['\Omega_1', '\Omega_2', '\Omega_2', '\Omega_3', '\Omega_3', '\Omega_3']);
fig.save('duplicate_legend_labels')