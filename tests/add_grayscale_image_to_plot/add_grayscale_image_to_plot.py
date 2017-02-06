# -*- coding: utf-8 -*-
"""
Created on Mon May 30 21:04:47 2016

@author: Ben
"""

import clearplot.figure as cpfig
import clearplot as cp
import os, scipy.misc
data_dir = os.path.join(os.path.dirname(os.path.dirname(cp.__file__)), \
    'doc', 'source', 'data')

#Verification of adding an image and adding a color bar
#Load image data
path = os.path.join(data_dir, 'fiber_image.tiff')
im = scipy.misc.imread(path)
fig = cpfig.Figure()
ax = fig.add_axes()
ax.x_label = ['x', 'pix']
ax.y_label = ['y', 'pix']
im_obj = ax.add_image(im, im_interp = 'bilinear', c_map = cp.colors.c_maps['light_gray'])
ax.x_tick = 50
fig.add_color_bar(im_obj)
fig.auto_adjust_layout()
#As reported in issue #4260 on Github 
#(https://github.com/matplotlib/matplotlib/issues/4260) matplotlib makes the
#axes background black when saving pdfs, with 1 image, grayscale colormaps, and
#transparent background.  So we avoid this by making the background opaque.
fig.save('add_grayscale_image_to_plot', transparent = False)