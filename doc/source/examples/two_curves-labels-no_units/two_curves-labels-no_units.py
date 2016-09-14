# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:10:23 2015

@author: Ben
"""
import clearplot.plot_functions as pf
import numpy as np

xa = np.arange(0,10,0.01)
ya = np.sqrt(xa)
xb = xa
yb = np.log(xb + 1.0)

[fig, ax, curves] = pf.plot('', [xa, xb], [ya, yb], \
    labels = ['\Omega_1', '\Omega_2'], \
    x_label = ['\omega_{x}'], y_label = ['\Omega'])
ax.label_curves(ndx = [500, 530], angles = [120, -60])
fig.save('two_curves-labels-no_units.png')