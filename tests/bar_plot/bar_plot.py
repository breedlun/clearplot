# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:50:04 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np

#Verification that bar plots work propery
xa = np.arange(1,5,1)
ya = np.arange(4,8,1)
ya_err = ya / 10.0
xb = np.arange(1,4,1)
yb = np.array([4, 3, 5.5])
yb_err = np.array([yb / 20.0, yb / 10.0])
[fig, ax] = pf.plot_bars('', [xa, xb], [ya, yb], \
    ['\mathsf{Categories}'], ['d-D'], \
    labels = ['\alpha', '\beta']);
ax.plot_error_bars([xa, xb], [ya, yb], y_err = [ya_err, yb_err])
fig.save('bar_plot')