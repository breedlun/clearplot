# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:25:41 2015

@author: Ben
"""
import clearplot.plot_functions as pf
import numpy as np

xa = np.array([1, 2.5, 4, 6])
ya = np.arange(4,8,1)
ya_err = ya / 10.0
xb = np.array([1, 3, 5.5, 7])
yb = np.array([2, 4, 3, 5.5])
yb_err = np.array([yb / 20.0, yb / 10.0])

[fig, ax] = pf.plot_bars('', [xa, xb], [ya, yb], ['N'], ['d-D'], \
    legend = ['\alpha', '\beta'], widths = 0.75)
ax.plot_error_bars([xa, xb], [ya, yb], y_err = [ya_err, yb_err])
fig.save('bar_plot.png')