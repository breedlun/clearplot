# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:07:09 2015

@author: Ben
"""
import clearplot.plot_functions as pf
import numpy as np

x = np.arange(0,10,0.01)
y = np.sqrt(x)

pf.plot('basic.png', x, y, \
	x_label = ['\phi', '\%'], y_label = ['\psi', 'GPa'], \
    x_lim = [None, 16], x_tick = 4);