# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:35:34 2015

@author: Ben
"""
import clearplot
import clearplot.plot_functions as pf
import numpy as np

x = np.arange(0,10,0.01)
y = np.sqrt(x)

pf.plot('math_text_typesetting.png', x, y, \
    x_label = ['\int_0^x \exp\left[\hat{x}\right]\,\mathrm{d}\hat{x}'], \
    y_label = ['\frac{P}{A}', 'GPa'])
    
clearplot.params.use_latex(True)
[fig, ax, curves] = pf.plot('LaTeX_typesetting.png', x, y, \
    x_label = ['\int_0^x \exp\left[\hat{x}\right]\,\mathrm{d}\hat{x}'], \
    y_label = ['\displaystyle \frac{P}{A}', 'GPa'])