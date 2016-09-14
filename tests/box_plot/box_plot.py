# -*- coding: utf-8 -*-
"""
Created on Mon May 30 20:52:21 2016

@author: Ben
"""

import clearplot.plot_functions as pf
import clearplot as cp
import os
import numpy as np
data_dir = os.path.join(os.path.dirname(os.path.dirname(cp.__file__)), \
    'doc', 'source', 'data')

#Verification that box plots work properly
path = os.path.join(data_dir, 'violin_plot_data.csv')
data = np.loadtxt(path, delimiter = ',')
pf.plot_box_and_whiskers('box_plot', \
    [np.array([1]), np.array([2]), np.array([3]), np.array([4])], \
    [data[:,0], data[:,1], data[:,2], data[:,3]], \
    ['\mathsf{Long\,Label}'], ['\varphi','km']);