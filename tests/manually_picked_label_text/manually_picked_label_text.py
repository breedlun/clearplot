# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:44:37 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np

#Verification that manually picking the label text works properly
xa = np.arange(0,10,0.01)
ya = np.sqrt(xa)
xb = xa
yb = np.log(xa + 1.0)
[fig, ax, curves] = pf.plot('', [xa, xb], [ya, yb], \
	labels = ['\Omega_1', '\Omega_2'], legend = False)
ax.label_curves(pick = 'text')
fig.save('manually_picked_label_text')