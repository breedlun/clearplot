# -*- coding: utf-8 -*-
"""
Created on Sun May 10 09:20:28 2015

@author: breedlu
"""
import matplotlib as _mpl
try:
   import cPickle as _pickle
except:
   import _pickle
import os as _os

#Set the backend for rendering the plot to screen.  (A different renderer is 
#used for saving the plot to a file.) (It is important to do this before 
#importing pyplot.  See 
#http://stackoverflow.com/questions/20025077/how-do-i-display-a-matplotlib-figure-window-on-top-of-all-other-windows-in-spyde
#for further details.)
_mpl.rcParams['backend'] = 'Qt4Agg'

#Misc Settings
#The default background is gray, change it to white 
_mpl.rcParams['figure.facecolor'] = 'white'
_mpl.rcParams['image.interpolation'] = 'none'
_mpl.rcParams['figure.figsize'] = [150.0/25.4, 150.0/25.4]

#Line Settings
_mpl.rcParams['lines.linewidth'] = 2
_mpl.rcParams['lines.solid_capstyle'] = 'butt'
_mpl.rcParams['lines.dash_capstyle'] = 'butt'

#Tick mark settings    
_mpl.rcParams['xtick.major.width'] = 1
_mpl.rcParams['ytick.major.width'] = 1
_mpl.rcParams['xtick.major.size'] = 4.5
_mpl.rcParams['ytick.major.size'] = 4.5
_mpl.rcParams['xtick.major.pad'] = 4.5
_mpl.rcParams['ytick.major.pad'] = 4.5
_mpl.rcParams['xtick.minor.width'] = 1
_mpl.rcParams['ytick.minor.width'] = 1
_mpl.rcParams['xtick.minor.size'] = 2
_mpl.rcParams['ytick.minor.size'] = 2
_mpl.rcParams['xtick.direction'] = 'out' 
_mpl.rcParams['ytick.direction'] = 'out'

#Legend settings
_mpl.rcParams['legend.borderpad'] = 0.35
_mpl.rcParams['legend.handletextpad'] = 0.25

#Font settings
_mpl.rcParams['font.family'] = 'sans-serif'
#Matplotlib 1.3.1 has a bug where 'Bitstream Vera Sans' is automatically 
#selected if it is anywhere in the list, so I have removed it for now.
#See http://matplotlib.1069221.n5.nabble.com/font-setting-in-matplotlib-1-3-1-td42662.html
#for further details.
_mpl.rcParams['font.sans-serif'] = ['TeXGyreHerosTXfonts'] 
_mpl.rcParams['mathtext.rm'] = 'sans'
_mpl.rcParams['mathtext.sf'] = 'sans'
_mpl.rcParams['mathtext.it'] = 'sans:italic'
_mpl.rcParams['mathtext.fontset'] = 'custom'
_mpl.rcParams['font.size'] = 16
_mpl.rcParams['legend.fontsize'] = 14
#The font type must be set to 42 (TrueType) so that Acrobat/Illustrator can 
#edit the text
_mpl.rcParams['pdf.fonttype'] = 42
_mpl.rcParams['ps.fonttype'] = 42

#LaTeX Text Rendering
##If using latex to render everything, you may need to do 
##os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin'
##to put latex on executable path
_mpl.rcParams['text.usetex'] = False
def use_latex(boolean):
    """
    Specify whether to use matplotlib's math text engine (fast) or LaTeX (slow) 
    to render mathematical expressions and other text.  The default is math 
    text.
    """
    _mpl.rcParams['text.usetex'] = boolean
#If 'text.usetex' is True, then the following preamble is run prior to 
#typsetting. The newtxfonts package was chosen because it consists of several 
#fonts and it has full math support.  Its sans-serif font is TeXGyreHeros (a 
#Helvetica clone) and the greek letters in its math font are similar to 
#computer modern, except they have heavier line weights, so they match the 
#TeXGyreHeros line weights.  
_mpl.rcParams['text.latex.preamble'] = [
    r'\usepackage{newtxtext}',                        #loads a family of fonts
    r'\renewcommand*\familydefault{\sfdefault}',    #causes the sans-serif font from the above font family to be used for normal text
    r'\usepackage[italic]{mathastext}',             #causes the latin letters from the font family to be used in math mode
    r'\usepackage{newtxmath}']
#'text.latex.preview' must be set to True, otherwise the baseline will be 
#underneath subscripts, which is wrong.  (I believe this setting causes
#matplotlib to 'preview' the typeset version of the LaTeX string before placing
#it.  This allows matplotlib to find the proper baseline rather than just 
#using the bounding box.)
_mpl.rcParams['text.latex.preview'] = True           

#Save settings
#We add padding to the automaticaly selected layout and the save the figure 
#as is, without any additional padding.
_mpl.rcParams['savefig.pad_inches'] = 0.0
auto_layout_pad = 2.0 #mm
#In matplotlib 1.3.1 and earlier, _mpl.rcParams['savefig.bbox'] = 'tight' causes 
#videos to be all garbled (see https://github.com/matplotlib/matplotlib/issues/2483).
_mpl.rcParams['savefig.format'] = 'pdf'
#For some crazy reason, the default image dpi for files is different than the 
#figure window dpi
_mpl.rcParams['savefig.dpi'] = _mpl.rcParams['figure.dpi']
_mpl.rcParams['path.snap'] = False
_mpl.rcParams['path.simplify'] = False

#Explicitly specify the color cycle (mpl.rcParams['axes.color_cycle'])
#If you let matplotlib go through he color cycle on it's own, it will reset 
#when it switches to the second y-axis.
colors = [[1,0,0], [0,0,1], [0,.6,0], [1,.5,0], [.7,0,.5], [0,.5,.5], \
    [.4,0,.7], [0.45,0.33,0.22], [0,0,0]]
#Uniformly scale down all the colors to create sets of darker colors
dark_colors = [[0.5,0,0,1], [0,0,0.5,1], [0,.3,0,1], [0.5,.25,0,1], \
    [.35,0,.25,1], [0,.25,.25,1], [.2,0,.35,1], [0.225,0.165,0.11,1], \
    [0,0,0,1]]
darker_colors = [[0.35,0,0], [0,0,0.35], [0,.21,0], [0.35,.175,0], \
    [.245,0,.175], [0,.175,.175], [.14,0,.245], [0.1575,0.1155,0.077], \
    [0,0,0]]
#Create pastel version of the color list
#These were generated by setting the alpha channel to 0.7, and then using the
#following pseudocode to convert to plain RGB values with a white background
#Source => Target = (BGColor + Source) =
#Target.R = ((1 - Source.A) * BGColor.R) + (Source.A * Source.R)
#Target.G = ((1 - Source.A) * BGColor.G) + (Source.A * Source.G)
#Target.B = ((1 - Source.A) * BGColor.B) + (Source.A * Source.B)
pastel_colors = [[1,0.3,0.3], [0.3,0.3,1], [0.3,0.72,0.3], [1,0.65,0.3], \
    [0.79,0.3,0.65], [0.3,0.65,0.65], [0.58,0.3,0.79], [0.615,0.531,0.454], \
    [0.3,0.3,0.3]]

#Get the dots per mm
dpmm = _mpl.rcParams['figure.dpi'] / 25.4
#Define whether axis labels will have arrows
axis_arrow_bool = True

#Load custom colormaps
#(The _os.path.dirname(__file__) gives the directory that clearplot is installed 
#in.  The 'r' tells open() to open as read only, and the 'b' tells Python to 
#open the file as a binary and ignore '\n' - type characters since they only 
#apply to text files.)
_c_maps_file = open(_os.path.join(_os.path.dirname(__file__),'custom_colormaps.pkl'), 'rb')
c_maps = _pickle.load(_c_maps_file)
_c_maps_file.close()