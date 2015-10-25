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

[fig, ax] = pf.plot('', [xa, xb], [ya, yb], \
    ['\overline{\omega}_{x}'], ['\overline{\Omega}'])
ax.label_curves(['\overline{\Omega}_1', '\overline{\Omega}_2'], \
    ndx = [500, 530], angles = [120, -60])
fig.save('two_curves-labels-no_units.png')