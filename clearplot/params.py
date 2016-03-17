# -*- coding: utf-8 -*-
"""
Created on Sun May 10 09:20:28 2015

@author: breedlu
"""
import matplotlib as _mpl

#Set the backend for rendering the plot to screen.  (A different renderer is 
#used for saving the plot to a file.) (It is important to do this before 
#importing pyplot.  See 
#http://stackoverflow.com/questions/20025077/how-do-i-display-a-matplotlib-figure-window-on-top-of-all-other-windows-in-spyde
#for further details.)
#(We selected the TkAgg backend, since it is the only interactive backend that 
#is supposed to work "out of the box" with matplotlib.  See 
#http://matplotlib.org/faq/usage_faq.html#what-is-a-backend and 
#http://matplotlib.org/users/installing.html for more info.  Unfortunately, 
#Spyder 2.3.8 has a bug with adjusting the window size with TkAgg, as detailed 
#here https://github.com/spyder-ide/spyder/issues/1651.  We were using Qt4Agg 
#previously, but it requires PySide or PyQt.  Also, as noted in issue #2 on 
#Github, matplotlib 1.5.0 has a bug with Qt4Agg that causes python to crash.  
#Fortunately, this Qt4Agg bug does not appear when using Qt4Agg in Spyder.  
#Thus we can still specify TkAgg for general python usage, and avoid the 
#TkAgg/Spyder figure window size bug by specifying the QtAgg backend in Spyder 
#and turning on the scientific_startup.py script.)
_mpl.rcParams['backend'] = 'TkAgg'

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
_mpl.rcParams['font.sans-serif'] = ['TeXGyreHerosTXfonts', 'Bitstream Vera Sans'] 
_mpl.rcParams['mathtext.rm'] = 'sans'
_mpl.rcParams['mathtext.sf'] = 'sans'
_mpl.rcParams['mathtext.it'] = 'sans:italic'
_mpl.rcParams['mathtext.fontset'] = 'custom'
_mpl.rcParams['font.size'] = 16
_mpl.rcParams['legend.fontsize'] = 16
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

#Get the dots per mm
dpmm = _mpl.rcParams['figure.dpi'] / 25.4
#Define whether axis labels will have arrows
axis_arrow_bool = True

