# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:21:16 2015

@author: Ben
"""
import clearplot.plot_functions as pf
import numpy as np

xa = np.arange(0, 1.001, 0.001)
ya = np.sqrt(0.0625 - ((xa-0.5)/2.0)**2.0) * 8.0
xa = np.append(xa, np.flipud(xa))
ya = np.append(ya, -np.flipud(ya))
xb = xa * 2.35
yb = ya * 1.5

[fig, ax] = pf.plot('', [xa, xb], [ya, yb], \
    ['\lambda_{zz}'], ['\rho_{r\theta}', 'Btu']);
ax.x_tick_labels = ['0', '\pi/2', '\pi', '3\pi/2', '2\pi', '5\pi/4']
ax.y_tick_labels = ['\alpha', '', '0', '', '\beta']
ax.add_arrowheads_to_curves(ndx = [[800, 1300], [800, 1300]])
fig.save('arrows-custom_tick_labels.png')