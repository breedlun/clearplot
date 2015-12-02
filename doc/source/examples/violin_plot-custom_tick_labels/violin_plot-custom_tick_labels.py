# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:27:24 2015

@author: Ben
"""
import clearplot.figure as figure
import numpy as np
import os

#Load the data
data_dir = os.path.join(os.path.dirname(figure.__file__), os.pardir, 'doc', \
    'source', 'data')
path = os.path.join(data_dir, 'violin_plot_data.csv')
data = np.loadtxt(path, delimiter = ',')

#Plot the data
fig = figure.Figure()
ax = fig.add_axes()
ax.x_label_obj.arrow_bool = False
ax.x_label = ['\mathsf{Categories}']
ax.y_label = ['\varphi', 'km']
ax.plot_violins([np.array([1]), np.array([2]), np.array([3]), np.array([4])], \
    [data[:,0], data[:,1], data[:,2], data[:,3]]);
ax.x_tick_list = [1, 2, 3, 4]
ax.x_tick_labels = ['a', 'b', 'c', 'd']
fig.auto_adjust_layout()
fig.save('violin_plot-custom_tick_labels.png')