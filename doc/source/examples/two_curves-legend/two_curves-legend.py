# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:08:47 2015

@author: Ben
"""
import clearplot.plot_functions as pf
import numpy as np

xa = np.arange(0,10,0.01)
ya = np.sqrt(xa)
xb = xa
yb = 3.0 * (xb/10)**3 - 2.0 * (xb/10)**2

[fig, ax, curves] = pf.plot('two_curves-legend.png', [xa, xb], [ya, yb], \
    labels = ['\kappa_y', '\kappa_z'], \
    x_label = ['\zeta_{yz}', 'in'], y_label = ['\kappa_j', 'lbf'])