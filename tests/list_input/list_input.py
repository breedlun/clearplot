# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:20:23 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np

#Verify that plot function can handle curves input as lists as well as 
#numpy arrays
xa = [1,2,3]
ya = [1,2,3]
xb = xa
yb = np.array([4,5,6])
pf.plot('list_input', [xa, xb], [ya, yb], ['\Phi'])