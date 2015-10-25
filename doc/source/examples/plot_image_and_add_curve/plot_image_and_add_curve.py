# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:39:21 2015

@author: Ben
"""
import clearplot.figure as figure
import os, scipy.misc, pickle

#Load image into python
data_dir = os.path.join(os.path.dirname(figure.__file__), os.pardir, 'doc', \
    'source', 'data')
path = os.path.join(data_dir, 'fiber_image.tiff')
im = scipy.misc.imread(path)
#Load edge dectection results
path = os.path.join(data_dir, 'fiber_data.pkl')
f = open(path, 'rb')
[im_x, im_y, x, y] = pickle.load(f)
f.close()

#Place the image on a set of axes
fig = figure.Figure()
ax = fig.add_axes()
im_obj = ax.add_image(im, x = im_x, y = im_y)
ax.x_label = ['x', 'mm']
ax.y_label = ['y', 'mm']
ax.x_tick = 2
ax.y_tick = 2
ax.x_lim = [0,'auto']
ax.y_lim = [-2, 'auto']
#Add edge detected data
ax.plot(x, y)

#Save the data
fig.auto_adjust_layout()
fig.save('plot_image_and_add_curve.png')