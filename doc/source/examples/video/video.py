# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:50:49 2015

@author: Ben
"""
import scipy.misc, clearplot, os, pickle
import numpy as np
import clearplot.figure as figure
import clearplot.plot_functions as pf
import matplotlib.animation as ani
import matplotlib.pyplot as plt

#Load response curve
data_dir = os.path.join(os.path.dirname(clearplot.__file__), os.pardir, 'doc', \
    'source', 'data')
print data_dir
path = os.path.join(data_dir, 's140302C-mechanical_response.pkl')
f = open(path, 'rb')
[xa, ya, blah] = pickle.load(f)
f.close()
#Specify the indices of the field images to be plotted
ndx_list = range(0, 253)
#Specify the column indices to crop the image data to
cols = range(110, 110+115)
#Specify the initial marker location
xb = np.array(xa[0])
yb = np.array(ya[0])
#Load the first image
im_filename = os.path.join('lo-rez_field_images', \
    's140302C-eqps_field-frame_%r.png' %(1))
im_path = os.path.join(data_dir, im_filename)
im = scipy.misc.imread(im_path)

#Create figure window (specify in pixels, but convert to mm)
fig_size = np.array([680.0, 380.0]) / clearplot.params.dpmm
fig = figure.Figure(size = fig_size)
#Create mechanical response plot
[fig, ax] = pf.plot('', xa, ya, ['\varepsilon', '\%'], ['\sigma', 'GPa'], \
    fig = fig, ax_pos = [35.0, 23.0])
ax.plot_markers(xb, yb, colors = [1,1,1], edge_widths = [2], sizes = [8])
#Create image plot
[fig, im_ax, imgs] = pf.show_im('', im[:, cols], scale_im = 1.15, \
    c_label = ['\bar{\varepsilon}^p', '\%'], c_lim = [0, 100], c_tick = 25, \
    c_bar = True, fig = fig, ax_pos = [140.0, 18.0], im_interp = 'bicubic')

#Get the marker and image objects to be updated with each frame
marker = ax.markers[0]
img = imgs[0]
def init():
    marker.set_data([], [])
    img.set_data([[]])
    return marker, img,
#Define how the figure will be updated with each new frame
def update_fig(i):
    #Update marker position
    marker.set_data(xa[2*i], ya[2*i])
    ##Load field image
    im_filename = os.path.join('lo-rez_field_images', \
        's140302C-eqps_field-frame_%r.png' %(2*i+1))
    im_path = os.path.join(data_dir, im_filename)
    im = scipy.misc.imread(im_path)
    #Update image
    img.set_data(im[:,cols])
    return marker, img,
    
#Create the animation
anim = ani.FuncAnimation(fig.mpl_fig, update_fig, init_func = init, \
    frames = max(ndx_list)/2, interval = 2, blit = True)
plt.close(fig.mpl_fig)
#Specify ffmpeg installation path
plt.rcParams['animation.ffmpeg_path'] = '/opt/local/bin/ffmpeg'
#Save the animation
writer = ani.FFMpegWriter(fps = 15, bitrate = 300)
anim.save('video.mp4', writer = writer)