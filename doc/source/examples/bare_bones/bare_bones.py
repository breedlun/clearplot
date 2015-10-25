# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:04:55 2015

@author: Ben
"""
import clearplot.plot_functions as pf
import numpy as np

x = np.arange(0,10,0.01)
y = np.sqrt(x)
pf.plot('bare_bones.png', x, y);