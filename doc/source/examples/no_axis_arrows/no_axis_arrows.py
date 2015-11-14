# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:04:55 2015

@author: Ben
"""
import clearplot.params
import clearplot.plot_functions as pf
import numpy as np

clearplot.params.axis_arrow_bool = False

x = np.arange(0,10,0.01)
y = np.sqrt(x)

pf.plot('no_axis_arrows.png', x, y, \
    ['\sf{Volume\;Change}', '\%'], ['\psi', 'GPa']);