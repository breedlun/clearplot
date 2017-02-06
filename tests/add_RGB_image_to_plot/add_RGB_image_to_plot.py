# -*- coding: utf-8 -*-
"""
Created on Mon May 30 21:07:54 2016

@author: Ben
"""

import clearplot.figure as cpfig
import clearplot as cp
import os, scipy.misc
import numpy as np
data_dir = os.path.join(os.path.dirname(os.path.dirname(cp.__file__)), \
    'doc', 'source', 'data')

#Verification that adding an image works with RGB images, and that we can 
#specify the color bar orientation, position, limits, and tick marks
path = os.path.join(data_dir, 'hi-rez_field_images', 's140302C-eqps_field-frame_252.png')
im = scipy.misc.imread(path)
cols = range(350,850)
im13a = im[:, cols, :]
fig = cpfig.Figure()
ax = fig.add_axes()
ax.x_label = ['x', 'pix']
ax.y_label = ['y', 'pix']
im_obj = ax.add_image(im13a, \
    x = np.array([50,50+im13a.shape[1]]), y = np.array([50,50+im13a.shape[0]]))
ax.x_tick = 100
ax.y_tick = 100
fig.add_color_bar(im_obj, label = ['\omega', '\%'], position = [50, 210], \
    orient = 'h', lim = [0,200], tick = 50)
fig.auto_adjust_layout()
fig.save('add_RGB_image_to_plot')