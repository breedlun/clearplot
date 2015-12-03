# -*- coding: utf-8 -*-
"""
clearplot Tests:
Creates a series of test plots using clearplot. 
Created on Sun Dec 15 17:11:53 2013
@author: Ben
"""

import clearplot.plot_functions as pf
import clearplot.figure as figure
import clearplot as cp
import os, scipy.misc
import numpy as np
data_dir = os.path.join(os.path.dirname(os.path.dirname(cp.__file__)), \
    'doc', 'source', 'data')

#Verify that plot function can handle curves input as lists as well as 
#numpy arrays
x1a = [1,2,3]
y1a = [1,2,3]
x1b = x1a
y1b = np.array([4,5,6])
pf.plot('Test1-list_input', [x1a, x1b], [y1a, y1b], ['\Phi'])

#Verification that cropping algorithm is working properly
x2a = np.arange(-10, 10, 0.5)
y2a = 2.0 * np.sin(x2a)
y2b = np.arange(-2, 2, 0.1)
x2b = 7 * np.sin(y2b * 3.0 - 1.8) + 1.0
pf.plot('Test2-cropping_algorithm', [x2a, x2b], [y2a, y2b], \
    x_lim = [-4, 6], y_lim = [-1.5, 1.5])

#Verification that auto selected limits allow data to exceed limits by a 
#small amount
fig = figure.Figure()
ax = fig.add_axes()
ax.x_tick = 5
ax.y_tick = 0.5
ex = ax.exceed_lim * 0.99 * ax.x_tick
ey = ax.exceed_lim * 0.99 * ax.y_tick
x3a = np.arange(-10 - ex, 10 + ex, 0.01)
y3a = (1.0 + ey) * np.sin(x3a)
ax.plot([x3a], [y3a])
fig.auto_adjust_layout()
fig.save('Test3-slightly_exceed_limits')

#Verification that multiple y axes and linked x axes work properly
[fig, ax1] = pf.plot('', [0,1], [0,1], 'x', 'y1')
ax2 = fig.add_axes(share_x_ax = ax1)
ax2.y_tick = 0.1
ax2.y_label = ['y2']
ax2.plot([0,2], [0,0.3])
ax1.y_lim = [0.0, 0.4]
ax3 = fig.add_axes(link_x_ax = ax1)
ax3.y_label = ['y3']
ax3.plot([0, 0.6], [0, 0.2])
ax3.y_tick = 0.1
ax3.x_lim = [0, 1.5]
fig.auto_adjust_layout()
fig.save('Test4-multiple_y_axes-linked_x_axes')

#Verification that multiple x axes and linked y axes work properly
[fig, ax1] = pf.plot('', [0,1], [0,1], 'x1', 'y')
ax2 = fig.add_axes(share_y_ax = ax1)
ax2.x_tick = 0.1
ax2.x_label = ['x2']
ax2.plot([0,0.3], [0,2])
ax1.x_lim = [0.0, 0.4]
ax3 = fig.add_axes(link_y_ax = ax1)
ax3.x_label = ['x3']
ax3.plot([0, 0.2], [0, 0.6])
ax3.x_tick = 0.1
ax3.y_lim = [0, 1.5]
fig.auto_adjust_layout()
fig.save('Test5-multiple_x_axes-linked_y_axes')

#Verfication that multiple legends can be added to a plot
[fig, ax] = pf.plot('', [0,1], [0,1], 'x', 'y', legend = ['P'], \
    legend_loc = 'upper left')
ax.plot_markers([0.25, 0.75], [0.25, 0.75], shapes = '+', sizes = 10, \
    edge_widths = 2)
ax.add_marker_legend(['A'], loc = 'lower right')
fig.save('Test6-multiple_legends')

#Verification that scaling the plot works cprrectly
[fig, ax] = pf.plot('Test7-scaled_plot', [0,1,2], [0,0.1,0.15], \
    ['x', 'mm'], ['y', 'mm'], scale_plot = 1.5, font_size = 24)

#Verification that manually picked arrows work properly
x4a = np.arange(0, 1.001, 0.001)
y4a = np.sqrt(0.0625 - ((x4a-0.5)/2.0)**2.0) * 12.0
x4a = np.append(x4a, np.flipud(x4a))
y4a = np.append(y4a, -np.flipud(y4a))
x4b = x4a * 2.35
y4b = y4a * 1.45
[fig, ax] = pf.plot('', \
    [x4a, x4b], [y4a, y4b])
ax.add_arrowheads_to_curves(pick = 'middle')
fig.save('Test8-manually_picked_arrows')

#Verification that manually picking the label text works properly
x5a = np.arange(0,10,0.01)
y5a = np.sqrt(x5a)
x5b = x5a
y5b = np.log(x5a + 1.0)
[fig, ax] = pf.plot('', [x5a, x5b], [y5a, y5b])
ax.label_curves(['\Omega_1', '\Omega_2'], pick = 'text')
fig.save('Test9-manually_picked_label_text')

#Verification that manually picking the root of the label works properly
x6a = x5a
y6a = y5a
x6b = x5b
y6b = y5b
[fig, ax] = pf.plot('', [x6a, x6b], [y6a, y6b])
ax.label_curves(['\Omega_1', '\Omega_2'], pick = 'root', \
    angles = [120, -60]);
fig.save('Test10-manually_picked_label_root')

#Verification that bar plots work propery
x7a = np.arange(1,5,1)
y7a = np.arange(4,8,1)
y7a_err = y7a / 10.0
x7b = np.arange(1,4,1)
y7b = np.array([4, 3, 5.5])
y7b_err = np.array([y7b / 20.0, y7b / 10.0])
[fig, ax] = pf.plot_bars('', [x7a, x7b], [y7a, y7b], \
    ['\mathsf{Categories}'], ['d-D'], legend = ['\alpha', '\beta']);
ax.plot_error_bars([x7a, x7b], [y7a, y7b], y_err = [y7a_err, y7b_err])
fig.save('Test11-bar_plot')

#Verification that box plots work properly
path = os.path.join(data_dir, 'violin_plot_data.csv')
data = np.loadtxt(path, delimiter = ',')
[fig, ax] = pf.plot_box_and_whiskers('Test12-box_plot', \
    [np.array([1]), np.array([2]), np.array([3]), np.array([4])], \
    [data[:,0], data[:,1], data[:,2], data[:,3]], \
    ['\mathsf{Long\,Label}'], ['\varphi','km']);


#Verification that invisible axes work correctly and that we can save an image
#at full resolution as a png
delta = 0.01
x = np.arange(-1.5, 1.5 + delta/100, delta)
y = np.arange(-1.5, 1.5 + delta/100, delta)
x12a, y12a = np.meshgrid(x, y)
r = (x12a + 1.5)**2.0 + (y12a + 1.5)**2.0
size = np.array(r.shape) * 1.0 / cp.params.dpmm
#fig = brp.Figure(size = size)
fig = figure.Figure()
ax = fig.add_invisible_axes(position = [0,0], size = size)
ax.x_lim = [0, r.shape[0]]
ax.y_lim = [0, r.shape[1]]
ax.add_image(r)
fig.auto_adjust_layout()
fig.save('Test13-full_rez_image_plotted_on_invisible_ax.png')

#Verification that image background contour plot works
import matplotlib.mlab as mlab
delta = 0.025
x = np.arange(-1.5, 1.5 + delta/100, delta)
y = np.arange(-1.5, 1.5 + delta/100, delta)
x9a, y9a = np.meshgrid(x, y)
r = (x9a + 1.5)**2.0 + (y9a + 1.5)**2.0
z1 = mlab.bivariate_normal(x9a, y9a, 1.0, 1.0, 0.0, 0.0)
z2 = mlab.bivariate_normal(x9a, y9a, 1.5, 0.5, 1, 1)
z9a = 10.0 * (z2 - z1)
pf.plot_contours('Test14-image_contour', x9a, y9a, z9a, \
    ['\tau_1', 'kg'], ['\tau_2', 'kg'], \
    x_tick = 0.5, y_tick = 0.5, x_lim = [-1.5, 1.5], y_lim = [-1.5, 1.5], \
    c_label = ['E', 'kJ'], plot_type = 'image', im_interp = 'bilinear')
    
#Verification that a line only contour plot works and specify contour 
#levels
x10a = x9a
y10a = y9a
z10a = z9a
[fig, ax] = pf.plot_contours('Test15-contour_lines-custom_levels', x10a, y10a, z10a, \
    ['\tau_1', 'kg'], ['\tau_2', 'kg'], x_tick = 0.5, y_tick = 0.5, \
    c_label = ['E', 'kJ'], plot_type = 'lines', c_lim = [-1.5, 1.5], c_tick = 0.5, \
    cl_levels = np.linspace(-1.0, 1.0, 10), cl_label_fmt = '%.3f')

#Verification that the image position is consistent with the contour lines.  
#(This is best seen with a very coarse image.)  Also verify that multiple 
#contour plots can be placed in a figure window
#Generate a coarse data set so that individual image pixels are easily visible.
x = np.array([[0,1,2,3], [0,1,2,3], [0,1,2,3], [0,1,2,3]])
y = np.array([[0,0,0,0], [1,1,1,1], [2,2,2,2], [3,3,3,3]])
z = np.array([[0.25, 0.75, 1.0, 0.75], [0.1, 0.65, 0.5, 0.4], [0.6, 0.3, 0.0, 0.2], [0.7, 0.9, 0.4, 0.6]])
#Create figure window
fig_size = np.array([1200, 400]) / cp.params.dpmm
fig = figure.Figure(size = fig_size) 
#Add plots to figure window
[fig, ax] = pf.plot_contours('', x, y, z, plot_type = 'filled', \
    fig = fig, ax_pos = [35, 30], c_label = ['z', 'mm'], x_tick = 1, y_tick = 1)
ax.add_title('Filled')
[fig, ax] = pf.plot_contours('', x, y, z, plot_type = 'image', \
    fig = fig, ax_pos = [155, 30], c_label = ['z', 'mm'], \
    x_tick = 1, y_tick = 1, x_lim = [0,3], y_lim = [0,3])
ax.add_title('Image')
[fig, ax] = pf.plot_contours('', x, y, z, plot_type = 'lines', \
    fig = fig, ax_pos = [275, 30], c_label = ['z', 'mm'], x_tick = 1, y_tick = 1)
ax.add_title('Lines Only')
#Save result
fig.save('Test16-Three_Contours')

#Verification of adding an image and adding a color bar
#Load image data
path = os.path.join(data_dir, 'fiber_image.tiff')
im12a = scipy.misc.imread(path)
fig = figure.Figure()
ax = fig.add_axes()
ax.x_label = ['x', 'pix']
ax.y_label = ['y', 'pix']
im_obj = ax.add_image(im12a, im_interp = 'bilinear', c_map = cp.colors.c_maps['light_gray'])
ax.x_tick = 50
fig.add_color_bar(ax, im_obj)
fig.auto_adjust_layout()
#As reported in issue #4260 on Github 
#(https://github.com/matplotlib/matplotlib/issues/4260) matplotlib makes the
#axes background black when saving pdfs, with 1 image, grayscale colormaps, and
#transparent background.  So we avoid this by making the background opaque.
fig.save('Test17-im_plot-scaled_image2', transparent = False)

#Verification that adding an image works with RGB images, and that we can 
#specify the color bar orientation, position, limits, and tick marks
path = os.path.join(data_dir, 'hi-rez_field_images', 's140302C-eqps_field-frame_252.png')
im = scipy.misc.imread(path)
cols = range(350,850)
im13a = im[:, cols, :]
fig = figure.Figure()
ax = fig.add_axes()
ax.x_label = ['x', 'pix']
ax.y_label = ['y', 'pix']
im_obj = ax.add_image(im13a, \
    x = np.array([50,50+im13a.shape[1]]), y = np.array([50,50+im13a.shape[0]]))
ax.x_tick = 100
ax.y_tick = 100
fig.add_color_bar(ax, im_obj, label = ['\omega', '\%'], position = [50, 210], \
    orient = 'h', lim = [0,200], tick = 50)
fig.auto_adjust_layout()
fig.save('Test18-im_plot-RGB_image')

#Verification that duplicate legend labels are automatically removed
x19a = [0,1]
x19b = [0,1]
x19c = [0,1]
x19d = [0,1]
x19e = [0,1]
x19f = [0,1]
y19a = [0,0.1]
y19b = [0,0.2]
y19c = [0,0.3]
y19d = [0,0.4]
y19e = [0,0.5]
y19f = [0,0.6]
[fig, ax] = pf.plot('', [x19a, x19b, x19c, x19d, x19e, x19f], \
    [y19a, y19b, y19c, y19d, y19e, y19f], \
    curve_colors = [[1,0,0], [0,1,0], [0,1,0], [0,0,1], [0,0,1], [0,0,1]],\
    curve_widths = [1,2,2,3,3,3], curve_styles = ['-', '--', '--', ':', ':', ':'])
ax.add_legend(['\Omega_1', '\Omega_2', '\Omega_2', '\Omega_3', '\Omega_3', '\Omega_3']);
fig.save('Test19-duplicate_legend_labels')

#Verification that limits and ticks can be set on the first set of axes
#and do not get reset by the second set of axes.
fig = figure.Figure()
ax1 = fig.add_axes()
x20a = np.linspace(0,10,10)
y20a = np.linspace(0,1,10)
x20b = x20a
y20b = np.linspace(0,20,10)
ax1.x_label = ['x1']
ax1.y_label = ['y1']
ax1.plot(x20a, y20a)
ax1.x_tick = 1
ax1.x_lim = [0, 5]
ax1.y_tick = 0.5
ax2 = fig.add_axes(link_x_ax = ax1)
ax2.y_label = ['y2']
ax2.y_tick = 5
ax2.plot(x20b, y20b)
fig.auto_adjust_layout()
fig.save('Test20-linked_x_ax_with_specified_ticks_and_lims')

#Verification that the cropping algorithm works properly with log data
#(Select x values that are nearly the same as the limits on a linear scale, 
#but significantly different on a log scale.  Select y values that are totally 
#within the y limits, so that the data exceeds the x limits and not the y 
#limits.)
x21a = np.linspace(5.0e-13, 5.0e-6, 20)
y21a = np.linspace(1.0e8, 1.0e11, 20)
#(Select x values that are totally within the x limits, so that the data 
#exceeds the y limits and not the x limits.  Select y values that are 
#significantly  bigger/smaller than limits on a linear scale, but are nearly 
#the same on a log scale.)
x21b = np.linspace(1.0e-11, 1.0e-8, 20)
y21b = np.linspace(1.0e7 - 0.4e6, 1.0e12 + 0.04e12, 20)
pf.plot('Test21-cropping_algorithm-log_axes', \
    [x21a, x21b], [y21a, y21b], \
    x_scale = 'log', y_scale = 'log', \
    x_lim = [1.0e-12, 1.0e-7], y_lim = [1.0e7, 1.0e12])
    
#Verification that a linear scaled y-axis can share a x-axis with a log scaled
#y-axis.
x22a = np.linspace(0, 5, 10)
y22a = np.linspace(0, 5, 10)
x22b = np.linspace(1, 4, 10)
y22b = 10.0**x22b
fig = figure.Figure()
ax1 = fig.add_axes()
ax1.x_label = ['x1']
ax1.y_label = ['y1']
ax1.plot(x22a, y22a)
ax2 = fig.add_axes(share_x_ax = ax1)
ax2.y_scale = 'log'
ax2.y_label = ['y2']
ax2.plot(x22b, y22b)
fig.auto_adjust_layout()
fig.save('Test22-shared_x_ax_with_linear_and_log_y_axes')



############################
## Features in development #
############################
#
#
##3D Surface Plot
#x_list = np.linspace(-1.0,1.0,100)
#y_list = np.linspace(-1.0,1.0,100)
#[x, y] = np.meshgrid(x_list, y_list)
#z = np.sqrt(1.0-x**2.0+(y/2.0)**2.0)
#pf.surf('Ex18-surf', x, y, z, x_tick = 1, y_tick = 1, z_tick = 1, \
#    z_lim = [-2.0, 2.0], x_lim = [-2.0, 2.0], y_lim = [-2.0, 2.0], \
#    light_alt_angle = 60.0, light_azm_angle = 20.0);