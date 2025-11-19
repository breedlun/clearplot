# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:47:40 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np

#Verification that manually picking the root of the label works properly
xa = np.arange(0,10,0.01)
ya = np.sqrt(xa)
xb = xa
yb = np.log(xa + 1.0)
[fig, ax, curves] = pf.plot('', [xa, xb], [ya, yb], \
	labels = [r'\Omega_1', r'\Omega_2'], legend = False)
ax.label_curves(pick = 'root', angles = [120, -60]);
fig.save('manually_picked_label_root')