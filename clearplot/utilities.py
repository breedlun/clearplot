# -*- coding: utf-8 -*-
#Created on Sat Sep 20 11:38:23 2014
#@author: breedlu

import matplotlib as _mpl
import numpy as _np
import matplotlib.text as _mpl_text
from matplotlib.patches import Polygon as _mpl_Polygon
from matplotlib.lines import Line2D as _mpl_Line2D
from matplotlib.artist import Artist as _Artist
from matplotlib.transforms import Transform as _Transform
from matplotlib.transforms import Affine2D as _Affine2D
from matplotlib.transforms import BboxBase as _BboxBase
import axes as _axes
#import color_bar as _color_bar
from itertools import cycle as _cycle
from itertools import islice as _islice

def get_unique_rows(array):
    """
    Finds the unique rows of an array
    """
    #This should be a one line numpy command, but numpy does not have this 
    #feature as of August 2015.
    #(See https://github.com/numpy/numpy/pull/3584)
    #Instead I created a custom function.
    array = _np.ascontiguousarray(array)
    array = array.view([('', array.dtype)]*array.shape[1])
    [u_array, u_ndx] = _np.unique(array, return_index = True)
    u_ndx = _np.sort(u_ndx)
    u_array = array[u_ndx,:] 
    return(u_array, u_ndx)

def get_im_window_extent(im_obj, ax) :
    """
    Gets the bounding box for an image in display (pixel) coordinates
    """
    #(I orginally tried im_obj.get_window_extent(renderer), but as detailed
    #here: https://github.com/matplotlib/matplotlib/issues/2980
    #it did not work.  Here is my work around until the bug is fixed.)
    im_ext = im_obj.get_extent()
    im_pts = _np.array([[im_ext[0], im_ext[2]], [im_ext[1], im_ext[3]]])
    bbox = _mpl.transforms.Bbox(im_pts)
    #It is important to force matplotlib to draw the figure prior to the 
    #conversion from axes coordinates to display coordinates.  Ortherwise the
    #transformation does not work properly.
    ax.parent_fig.mpl_fig.canvas.draw()
    bbox = bbox.transformed(ax.mpl_ax.transData)
    return(bbox)

def set_im_interp(im_interp, im_obj, ax):
    """
    Sets the proper image interpolation type for an image.
    
    Parameters
    ----------
    im_interp : str
        Image interpolation type.  If 'auto', then algorithm choses either 
        'nearest' or 'none'.  If the image is blown up, then it uses 'nearest'.
        If the image is scaled down then it uses 'none'.  See
        `this matplotlib example <http://matplotlib.org/examples/images_contours_and_fields/interpolation_methods.html>`__
        and `this matplotlib example <http://matplotlib.org/examples/images_contours_and_fields/interpolation_none_vs_nearest.html>`__ 
        for further details.
    im_obj : image object
        Image to set the interpolation type on.
    ax : axes object
        Axes containing `im_obj`
    """
    #As shown here
    #https://github.com/matplotlib/matplotlib/issues/2972
    #it matters if you use interpolation = 'none' or interpolation = 'nearest'
    #when images are placed in vector graphics files.  Since neither one is 
    #perfect for all cases, we must select the appropriate one.
    if im_interp == 'auto':
        #Get the bounding box for the image in display (pixel) coordinates
        bbox = get_im_window_extent(im_obj, ax)
        #Compare the size of the image on the screen to the size of the image array 
        #size.  If the image is blown up, then use 'nearest'.  If the image is 
        #scaled down then use 'none'
        im = im_obj.get_array()
        #(Not sure whether I shoud use 'and' or 'or' here, but it typically 
        #doesn't matter.)
        if bbox.height > im.shape[0] * 2 or bbox.width > im.shape[1] * 2:
            im_interp = 'nearest'
        else:
            im_interp = 'none'
    #Set the interpolation type
    im_obj.set_interpolation(im_interp)

class Offset_From(object):
    """
    Generates a transformation object to offset from another object
    """
    #NOTE: This is a blantant copy from matplotlib.text.OffsetFrom 
    #(matplotlib v1.4.0).  I simply added the ability to work in mm units, 
    #added my axes class to the list of objects that can be offset from, and
    #changed the names of some variables
    def __init__(self, artist, ref_pt, units="mm"):
        """
        Parameters
        ----------
        artist : Artist, Bounding Box, or Transform
            object to offset from
        ref_pt : 1x2 list
            Point on the object to offset from.  Must be specified in 
            normalized bounding box coordinates of the object.
        units : 'points', 'pixels', or 'mm'
            Units for the offset
        """
        self._artist = artist
        self._ref_pt = ref_pt
        self.set_units(units)

    def set_units(self, units):
        assert units in ["points", "pixels", "mm"]
        self._units = units

    def get_units(self):
        return self._units

    def _get_scale(self, renderer):
        units = self.get_units()
        if units == "pixels":
            return 1.
        elif units == "mm":
            return renderer.dpi / 25.4
        else:
            return renderer.points_to_pixels(1.)

    def __call__(self, renderer):
        if isinstance(self._artist, _Artist):
            bbox = self._artist.get_window_extent(renderer)
            l, b, w, h = bbox.bounds
            xf, yf = self._ref_pt
            x, y = l + w * xf, b + h * yf
        elif isinstance(self._artist, _BboxBase):
            l, b, w, h = self._artist.bounds
            xf, yf = self._ref_pt
            x, y = l + w * xf, b + h * yf
        elif isinstance(self._artist, _Transform):
            x, y = self._artist.transform_point(self._ref_coord)
        elif isinstance(self._artist, _axes.Axes):
            l, b, w, h = self._artist.mpl_ax.bbox.bounds
            xf, yf = self._ref_pt
            x, y = l + w * xf, b + h * yf
#        elif isinstance(self._artist, _color_bar.Color_Bar):
#            l, b, w, h = self._artist.mpl_bar.ax.bbox.bounds
#            xf, yf = self._ref_pt
#            x, y = l + w * xf, b + h * yf
        else:
            raise RuntimeError("unknown type")

        sc = self._get_scale(renderer)
        tr = _Affine2D().scale(sc, sc).translate(x, y)

        return tr

#def move_obj_list(obj_list, dx, container):
#    """
#    Moves each element in a list of objects.
#    
#    Parameters
#    ----------
#    obj_list: list
#        contains objects you wish to move
#    dx: 1x2 numpy array
#        horizontal and vertical distance (in mm) to move objects
#    container: container object
#    """
#    container_size = container.size
#    for obj in obj_list:
#        #Text, patches, and lines all have different functions to get 
#        #and set their positions, so we need if statements for each 
#        #case
#        if obj.findobj(match=_mpl_text.Text):
#            #Move text                  
#            pos = obj.get_position() + dx / container_size
#            obj.set_position(pos)
#        elif obj.findobj(match=_mpl_Line2D):
#            #Move line
#            pos = obj.get_xydata() + dx / container_size
#            #The line object does not have a "set_xydata()" method and, 
#            #annoyingly, the "set_data" method requires the points to be 
#            #organized in columns instead of rows.
#            obj.set_data(pos.T)
#        elif obj.findobj(match=_mpl_Polygon):
#            #Move polygon
#            pos = obj.get_xy() + dx / container_size
#            obj.set_xy(pos)
#        else:
#            #Move patch
#            pos = obj.get_xy() + dx / container_size
#            obj.set_xy(pos.flatten())

def cycle_thru_list(list_obj, i):
    """
    Cycles through a list
    
    Parameters
    ----------
    list_obj : list
        List to be cycled through
    i : int
        Index of list to be put in the first position
    
    Returns
    -------
    cycled_list : list
        List with index `i` now in the first position
    """
    cycle_obj = _cycle(list_obj)
    L = len(list_obj)
    slice_obj = _islice(cycle_obj, i, i + L)
    cycled_list = list(slice_obj)
    return(cycled_list)   

def raw_string(txt):
    """
    Python automatically converts escape characters (i.e. \\n), which causes
    problems when inputing latex strings since they are full of backslashes.  
    This function returns a raw string representation of text
    
    Parameters
    ----------
    txt : string
        string that possibly contains escape characters
    
    Returns
    -------
    new_text : string
        same as 'text' but without any escape characters
    """
    escape_dict={'\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"'}
    #I used to have '\1' thru '\9' in the list above, but for some strange
    #reason '\a' and '\7' both get mapped to '\x07'.  Thus, when someone inputs 
    #'\alpha', it gets mapped to '\x07lpha'.  If '\7' is listed in the escape 
    #dictionary after '\a', then '\x07lpha' gets translated to '\\7lpha', which 
    #LaTeX cannot understand.  As far as I know, LaTeX never starts a command
    #with a number, so I just got rid of all the numbers in the escape 
    #dictionary.
    new_txt=''
    for char in txt:
        try: new_txt+=escape_dict[char]
        except KeyError: new_txt+=char
    return new_txt
    
def flatten(a):
    """
    Flattens list of lists with arbitrary depth into a 1-D list.

    Parameters
    ----------
    l : list
        list to be flattened
    
    Returns
    -------
    flat_l : list
        flattened list
    """
    flat_l = []
    for el in a:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            flat_l.extend(flatten(el))
        else:
            flat_l.append(el)
    return flat_l
    
def convert_err_to_nested_numpy_arrays(g):
    """
    Finds the bottom of nested lists and converts to N x 2 numpy arrays, as 
    needed.
    
    Parameters
    ----------
    a : list
        Nested list of arbitrary depth that may or may not have numpy arrays at
        the bottom
    
    Returns
    -------
    a : list
        Nested list of numpy arrays.
    not_numpy : boolean
        Used during the recurssion process.  Not intended for the end user.
    """
    #Initialize variables used in the recursion process
    not_numpy = False
    #Find out if input is a list
    if isinstance(g, (list)):
        for i, el in enumerate(g):
            #Use recursion to get to the bottom of the lists
            [g[i], not_numpy] = convert_err_to_nested_numpy_arrays(el)
            if not_numpy:
                if not [None]:
                    #Convert list into numpy array
                    g = _np.array(g)
                not_numpy = False
                break
    elif not isinstance(g, (_np.ndarray)):
        #Tell parent function to convert parent array into a numpy array
        not_numpy = True
    else:
        #Force numpy array to be 2-D
        if _np.ndim(g) == 1:
            #If error data is a 1-D array, assume that the error is symmetric, 
            #and turn into a 2-D array
            g = _np.vstack([[g], [g]])
        elif _np.ndim(g) > 2:
            raise ValueError("""Each data array should be N x 2 or N x 1""")
        else:
            if _np.shape(g)[0] != 2:
                #Make sure we have a Nx2 array, not a 2XN array
                g = g.transpose()
            
    return(g, not_numpy)
   
def find_depth(a):
    """
    Finds the depth of a list or numpy array using recursion
    
    Parameters
    ----------
    a : list or numpy array
        list or array of arbitrary depth
    
    Returns
    -------
    depth : integer
        depth of list
    """
    if isinstance(a, (list, tuple)):
        depth = 1 + max(find_depth(item) for item in a)
    elif isinstance(a, _np.ndarray):
        depth = a.ndim
    else:
        depth = 0
    return depth
    
def find_list_depth(a):
    """
    Finds the depth of a list using recursion
    
    Parameters
    ----------
    a : list
        list of arbitrary depth
    
    Returns
    -------
    depth : integer
        depth of list
    """
    if isinstance(a, (list, tuple)):
        depth = 1 + max(find_list_depth(item) for item in a)
    else:
        depth = 0
    return depth

def adjust_depth(a, proper_depth):
    """
    Finds the depth of a list or numpy array and adjusts it as necessary 
    
    Parameters
    ----------
    a : list or numpy array
        List or array to be modified
    proper_depth : integer
        Depth that `a` will be returned with
    
    Returns
    -------
    a: list or numpy array
        The input `a`, modified to have the proper depth
    """
    depth = find_depth(a)
    #Corrects the depth, if necessary
    depth_diff = proper_depth - depth 
    if isinstance(a, _np.ndarray):
        a.reshape([1] * depth_diff + list(a.shape))
    else:
        if depth_diff == 2:
            a = [[a]]
        if depth_diff == 1:
            a = [a]
    return a
    
def adjust_list_depth(a, proper_depth):
    """
    Finds the depth of a list and adjusts it as necessary 
    
    Parameters
    ----------
    a : list or any other object
        List to be modified
    proper_depth : integer
        Depth that `a` will be returned with

    Returns
    -------
    a: list
        The input `a`, modified to have the proper depth
    """
    depth = find_list_depth(a)
    #Corrects the depth, if necessary
    depth_diff = proper_depth - depth 
    if depth_diff == 2:
        a = [[a]]
    if depth_diff == 1:
        a = [a]
    return a

    
def preprocess_input(ui, depth, C):
    ui = adjust_depth(ui, depth)
    #Repeat inputs so that each curve has it's style defined
    ui = ui * C
    ui = ui[:C]
    return(ui)

def find_candidate_lim_and_tick(ui_lim, ui_tick, data_lim, \
    ax_scale, ax_log_base, exceed_lim):
    """
    Finds candidate limits and tick mark spacings
    
    Parameters
    ----------
    ui_lim : 1x2 list or numpy array
        User input axis limits.  Either element can be set to 'auto' to have 
        algorithm automatically select the low or high limit.
    ui_tick : float
        User input tick mark spacing.  Set to 'auto' to automatically select
        the tick mark spacing.
    data_lim : 1x2 list or numpy array
        Limits of the data on the axis.
    ax_scale : ['linear' | 'log']
        Axis scaling.
    ax_log_base : float
        Base of the logarithm for log scaled axes. (Not used for linearly 
        scaled axes.)
    exceed_lim : float
        When automatically selecting limits, the data is allowed to exceed the 
        limits by this ratio of the tick mark spacing.
        
    Returns
    -------
    lim_c : Nx2 list or numpy array
        A list of axis limit candidates
    tick_c : Nx1 list or numpy array
        A list of tick mark spacing candidates.
    n_tick_c : Nx1 list or numpy array
        A list of number of tick marks candidates
    """
    ui_lim = adjust_depth(ui_lim, 1)
    #If there isn't any data on the axes, just act as if the user specified
    #some limits
    if (data_lim[0] == _np.inf) or (data_lim[1] == _np.inf):
        if ui_lim[0] == 'auto' and ui_lim[1] == 'auto':
            if ax_scale == 'log':
                ui_lim = [ax_log_base**(-5),1.0]
            else:
                ui_lim = [0.0, 1.0]          
        elif ui_lim[0] == 'auto':
            if ui_tick != 'auto':                
                ui_lim[0] = ui_lim[1] - 5.0 * ui_tick
            else:
                ui_lim[0] = ui_lim[1] - 1.0
        elif ui_lim[1] == 'auto':
            if ui_tick != 'auto':                
                ui_lim[1] = ui_lim[0] + 5.0 * ui_tick
            else:
                ui_lim[1] = ui_lim[0] + 1.0

    #Combine the user input limits and the data limits into one list
    #so that it is easy to get the range
    lim = _np.zeros([2])
    if ui_lim[0] == 'auto':
        lim[0] = data_lim[0]
    else:
        lim[0] = float(ui_lim[0])
    if ui_lim[1] == 'auto':
        lim[1] = data_lim[1]
    else:
        lim[1] = float(ui_lim[1])

    #Check whether axis is on a linear or log scale
    if ax_scale == 'linear':
        #If tick mark spacing is not specified, select a tick mark spacing of 
        #either 1, 2, or 5, such that there are 3-6 tick marks, prefering less 
        #tick marks if multiple tick mark spacings qualify
        if ui_tick == 'auto':
            #If data scaling is really small, alert the user and quit
            if abs(_np.diff(lim)) < 2 * 10**(-10):
                raise ValueError("""Data scaling is too small: 
                Abs(Max-Min)<2*10^(-10).  Suggest rescaling data by using 
                different units.  If you still wish to use data where 
                Abs(Max-Min)<2*10^(-10) then specify a tick mark spacing.""")
            #If data scaling is really large, alert the user and quit
            elif abs(_np.diff(lim)) > 2 * 10**10:
                raise ValueError("""Data scaling is too big: 
                Abs(Max-Min)>2*10^(-10).  Suggest rescaling data by using 
                different units. If you still wish to use data where 
                Abs(Max-Min)>2*10^(-10) then specify a tick mark spacing.""") 
            #Specify candidate tick mark spacings that are within one order of 
            #magnitude
            tick_generic = _np.array([1.0, 2.0, 5.0])
            #The algorithm below starts at 1*10^(-10) and keeps increasing the
            #order of magnitude of the tick mark spacing until we get a 
            #reasonable number of tick marks.  It then increases the tick mark 
            #spacing by one more order of magnitude and calculates the 
            #corresponding number of tick marks.
            flag = 0
            s = -10
            tick_c = _np.array([]) 
            while flag < 2:
                s = s + 1
                #Quit if auto tick mark spacing routine fails
                if s==20:
                    raise ValueError("""Could not auto select tick mark 
                        spacing. Suggest specifying a tick mark spacing""")
                lim_s = _np.zeros((len(tick_generic), 2))
                tick_s = tick_generic * 10**s
                if ui_lim[0] == 'auto':
                    #round lmt for tick mark spacing candidate
                    lim_s_c = _np.floor(data_lim[0] / tick_s) * tick_s
                    #If minimum of data is nearly at the next tick mark, just 
                    #use the next tick mark as the limit and allow the data to 
                    #slightly exceed the limit.
                    lgc = (lim_s_c + tick_s - data_lim[0]) / tick_s < exceed_lim
                    lim_s[:,0] = lim_s_c + tick_s * lgc
                #or keep specified lmt
                else:
                    lim_s[:,0] = float(ui_lim[0])
                #round lmt for tick mark spacing candidate
                if ui_lim[1] == 'auto':
                    lim_s_c = _np.ceil(data_lim[1] / tick_s) * tick_s
                    #If maximum of data is nearly at the previous tick mark, 
                    #just use the previous tick mark as the limit and allow the 
                    #data to slightly exceed the limit.
                    lgc = (data_lim[1] - lim_s_c + tick_s) / tick_s < exceed_lim
                    lim_s[:,1] = lim_s_c - tick_s * lgc
                #or keep specified lmt
                else:
                    lim_s[:,1] = float(ui_lim[1])
                #find # of tick marks (not including the first tick mark) 
                #for tick mark spacing candidate
                #(rounding needed to get rid of numerical error)
                n_tick_s = _np.round(_np.diff(lim_s, axis = 1).flatten() / tick_s, 1)
                #Remove non-integers
                lgc = ~(_np.mod(n_tick_s,1.0)>0)
                n_tick_s = n_tick_s[lgc]
                tick_s = tick_s[lgc]
                #Find the indices in the acceptable range
                ndx = ((n_tick_s >= 2.0) & (n_tick_s <= 8.0)).nonzero()[0]
                if len(ndx) > 0:
                    tick_c = _np.hstack((tick_c, tick_s[ndx]))
                if len(tick_c) > 0:
                    flag = flag + 1
        else:
            tick_c = _np.array([float(ui_tick)])

        if ui_lim[0] == 'auto':
            #If limits were not specified, round limits to match tick mark 
            #spacing
            lo_lim_c = _np.floor(lim[0] / tick_c) * tick_c
            #If minimum of data is nearly at the next tick mark, just 
            #use the next tick mark as the limit and allow the data to 
            #slightly exceed the limit.
            lgc = (lo_lim_c + tick_c - lim[0]) / tick_c < exceed_lim
            lo_lim_c = lo_lim_c + tick_c * lgc
        else:
            lo_lim_c = float(ui_lim[0]) * _np.ones(len(tick_c))
        
        if ui_lim[1] == 'auto':
            #If limits were not specified, round limits to match tick mark 
            #spacing
            hi_lim_c = _np.ceil(lim[1] / tick_c) * tick_c
            #If maximum of data is nearly at the previous tick mark, 
            #just use the previous tick mark as the limit and allow the 
            #data to slightly exceed the limit.
            lgc = (lim[1] - hi_lim_c + tick_c) / tick_c < exceed_lim
            hi_lim_c = hi_lim_c - tick_c * lgc
        else:
            hi_lim_c = float(ui_lim[1]) * _np.ones(len(tick_c))

        #Combine hi and lo candidate limits into a single array
        lim_c = _np.vstack((lo_lim_c, hi_lim_c)).T            
        #find # of tick marks (not including the first tick mark) 
        #for tick mark spacing candidate
        #(rounding needed to get rid of numerical error)
        n_tick_c = _np.round(_np.diff(lim_c, axis = 1).flatten() / tick_c, 1)
    
    #If axis is on a log scale
    else:
        #If auto, set tick marks to be at powers of 10^1
        if ui_tick == 'auto':
            tick_c = _np.array([1])  
        else:
            tick_c = ui_tick
            
        #Initialize the limit candidates with the user input limits
        lim_c = _np.array([lim])      
        #Automatically round limits to the closest power of 10
        if _np.all(lim >= 0):
            #If limits were not specified, round limits to match tick mark spacing
            if ui_lim[0] == 'auto':
                exp = _np.floor(_np.log(data_lim[0]) / _np.log(ax_log_base))
                lim_c[0][0] = ax_log_base**exp
            if ui_lim[1] == 'auto':
                exp = _np.ceil(_np.log(data_lim[1]) / _np.log(ax_log_base))
                lim_c[0][1] = ax_log_base**exp
        elif _np.all(lim <= 0):
            #If limits were not specified, round limits to match tick mark spacing
            if ui_lim[0] == 'auto':
                exp = _np.ceil(_np.log(-data_lim[0]) / _np.log(ax_log_base))
                lim_c[0][0] = -ax_log_base**exp
            if ui_lim[1] == 'auto':
                exp = _np.floor(_np.log(-data_lim[1]) / _np.log(ax_log_base))
                lim_c[0][1] = -ax_log_base**exp
        else:
            raise ValueError("""You cannot have a logarithmic axis that spans 
                across negative and positive numbers""")

        #Calculate the number of tick marks
        n_tick_c = (_np.log(lim_c[0][1]) / _np.log(ax_log_base) \
            - _np.log(lim_c[0][0]) / _np.log(ax_log_base)) / tick_c
        
    return(lim_c, tick_c, n_tick_c)
    
def select_lim_and_tick(lim_c, tick_c, n_tick_c):
    """
    Select limits and tick mark spacings that give a pleasing number of tick 
    marks
    
    Parameters
    ----------
    lim_c : Nx2 list or numpy array
        A list of axis limit candidates
    tick_c : Nx1 list or numpy array
        A list of tick mark spacing candidates.
    n_tick_c : Nx1 list or numpy array
        A list of number of tick marks candidates
        
    Returns
    -------
    lim : 1x2 list or numpy array
        Optimum axis limits
    tick : float
        Optimum tick mark spacing
    n_tick_c : float or int
        Optimum number of tick marks
    """
    #Find tick mark spacings that give a # of tick marks in the ideal 
    #range
    ideal_ndx = ((n_tick_c >= 4.0) & (n_tick_c <= 6.0)).nonzero()[0]
    if len(ideal_ndx)>0:
        #If multiple tick mark spacings qualify, take the spacing that 
        #gives the smallest number of tick marks
        lim = lim_c[ideal_ndx[-1],:]
        tick = tick_c[ideal_ndx[-1]]
        n_tick = n_tick_c[ideal_ndx[-1]]
    else:
        good_ndx = ((n_tick_c >= 3.0) & (n_tick_c <= 7.0)).nonzero()[0]
        if len(good_ndx)>0:
            lim = lim_c[good_ndx[-1],:]
            tick = tick_c[good_ndx[-1]]
            n_tick = n_tick_c[good_ndx[-1]]
        else:
            #If none of the tick marks are ideal then use a large 
            #number of tick marks
            lim = lim_c[0,:]
            tick = tick_c[0]
            n_tick = n_tick_c[0]
    return(lim, tick, n_tick)
    
def find_and_select_lim_and_tick(ui_lim, ui_tick, data_lim, \
    ax_scale, ax_log_base, exceed_lim):
    """
    Convenience function that combines `find_candidate_lim_and_tick` with 
    `select_lim_and_tick`.
    """
    [lim_c, tick_c, n_tick_c] = find_candidate_lim_and_tick(ui_lim, ui_tick, \
        data_lim, ax_scale, ax_log_base, exceed_lim)
    [lim, tick, n_tick] = select_lim_and_tick(lim_c, tick_c, n_tick_c)
    return(lim, tick, n_tick)

    
def gen_tick_list(ui_tick_list, lim, tick, scale, log_base):
    """
    Generates a list of tick mark values
    
    Parameters
    ----------
    ui_tick_list : list or 'auto'
        User input list of tick mark values, or 'auto' to automatically 
        generate a tick mark list
    lim : 1x2 list or numpy array
        Axis limits.
    tick : float
        Tick mark spacing
    scale : ['log' | 'linear']
        Axis scaling
    log_base : float
        Logarithm base for log scaled axes
        
    Returns
    -------
    tick_list : list of floats
        List of tick mark values
    """
    if ui_tick_list is 'auto':
        #Set the list of tick marks
        if scale == 'log':
            #(range omits the last entry so we need to nudge it a bit)
            log_tick_list = _np.arange(\
                _np.log(lim[0]) / _np.log(log_base), \
                _np.log(lim[1]) / _np.log(log_base) + tick/100.0, tick)
            tick_list = log_base**log_tick_list
        else:
            #(range omits the last entry so we need to nudge it a bit)
            tick_list = _np.arange(lim[0], lim[1] + tick/100.0, tick)
    else:
        tick_list = ui_tick_list[:]
    return(tick_list)