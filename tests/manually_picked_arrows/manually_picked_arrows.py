# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:41:30 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np

#Verification that manually picked arrows work properly
xa = np.arange(0, 1.001, 0.001)
ya = np.sqrt(0.0625 - ((xa-0.5)/2.0)**2.0) * 12.0
xa = np.append(xa, np.flipud(xa))
ya = np.append(ya, -np.flipud(ya))
xb = xa * 2.35
yb = ya * 1.45
[fig, ax, curves] = pf.plot('', \
    [xa, xb], [ya, yb])
ax.add_arrowheads_to_curves(pick = 'middle')
fig.save('manually_picked_arrows')