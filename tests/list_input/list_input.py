# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:20:23 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import numpy as np

#Verify that plot function can handle curves input as lists as well as 
#numpy arrays
x1a = [1,2,3]
y1a = [1,2,3]
x1b = x1a
y1b = np.array([4,5,6])
pf.plot('list_input', [x1a, x1b], [y1a, y1b], ['\Phi'])