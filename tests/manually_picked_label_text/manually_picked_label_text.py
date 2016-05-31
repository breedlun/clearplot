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
[fig, ax] = pf.plot('', [xa, xb], [ya, yb])
ax.label_curves(['\Omega_1', '\Omega_2'], pick = 'text')
fig.save('manually_picked_label_text')