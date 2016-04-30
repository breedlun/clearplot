# -*- coding: utf-8 -*-
#Created on Sat Sep 20 11:31:00 2014
#@author: Benjamin Reedlunn

import matplotlib as _mpl
import matplotlib.pyplot as _plt
import numpy as _np
from copy import deepcopy
import utilities as _utl
import warnings as _warnings
import matplotlib.patches as _mpl_patches
from matplotlib.path import Path as _mpl_Path
from matplotlib.lines import Line2D as _mpl_Line2D
import clearplot as _cp
import custom_annotations as _ca
import axis_label as _axis_label

class _Axes_Base(object):
    def __init__(self, fig, **kwargs):
        """
        Basic axes initialization
        """
        self.parent_fig = fig
        self.parent_fig.axes.append(self)
        self._ui_pos = kwargs.pop('position', 'auto')
        scale_plot = kwargs.pop('scale_plot', 1.0)
        #Define a scaling dimension for the plot.  This dimension is used in a 
        #number of places to scale the distances between different objects.  
        #Under default settings, the scaling dimension corresponds to the 
        #number of millimeters between tick marks.  
        self.sdim = 20.0 * scale_plot
    
    @property    
    def position(self):
        """
        Gets/sets the position of the axes lower left corner in mm, relative to
        the lower left corner of the figure window.
        """
        pos_nfc = self.mpl_ax.get_position().p0
        fig_size = self.parent_fig.size
        pos = pos_nfc * fig_size
        return(pos)

    @position.setter
    def position(self, pos):
        size_nfc = self.mpl_ax.get_position().size
        fig_size = self.parent_fig.size
        rect_nfc = _np.hstack([pos / fig_size, size_nfc])
        self.mpl_ax.set_position(rect_nfc)
    
    @property
    def size(self):
        """
        Get/set the size of the axes.  Supply a 1x2 numpy array in mm units to 
        specify a new size.
        """
        size_nfc = self.mpl_ax.get_position().size
        fig_size = self.parent_fig.size
        size = size_nfc * fig_size
        return(size)
     
    @size.setter 
    def size(self, size):
        pos_nfc = self.mpl_ax.get_position().p0
        fig_size = self.parent_fig.size
        rect_nfc = _np.hstack([pos_nfc, size / fig_size])
        self.mpl_ax.set_position(rect_nfc)

    @property
    def bbox(self):
        """
        Gets a bounding box for the axes plotting area in mm, relative to the
        lower left corner of the figure.
        """
        fig = self.parent_fig
        bbox_nfc = self.mpl_ax.get_position()
        bbox = bbox_nfc.transformed(fig.fig_to_mm_trans)
        return(bbox)
    
    @property
    def tight_bbox(self):
        """
        Gets a bounding box in mm that includes the tick marks and tick mark 
        labels, relative to the lower left corner of the figure area.
        """
        #mpl_ax.get_tightbbox() includes the tick mark labels, unlike
        #mpl_ax.get_position()
        bbox_pix = self.mpl_ax.get_tightbbox(self.parent_fig.renderer)
        #Transform the bbox from figure pixels to axes mm
        pix_to_mm = self.parent_fig.mm_to_pix_trans.inverted()
        bbox = bbox_pix.transformed(pix_to_mm)
        return(bbox)
        
#    @property
#    def mm_to_pix_trans(self):
#        """
#        Gets a transformation object to go from mm, relative to the lower left
#        corner of the plotting area, to pixels, relative to the lower left
#        corner of the plotting area.
#        """
#        trans = self.parent_fig.mm_to_pix_trans
#        return(trans)
        
    def get_obj_bbox(self, obj):
        """
        Finds the coordinates of the bounding box surrounding an object, in mm, 
        relative to the lower left corner of the axes
        
        Parameters
        ----------
        obj: graphics primitive object 
            object you wish to get the bounding box for
        
        Returns
        -------
        bbox: bounding box object
        """
        #Get bbox relative to figure window
        bbox_fig = self.parent_fig.get_obj_bbox(obj)
        #Convert to relative to axes
        ax_pos = self.position
        bbox = bbox_fig.translated(-ax_pos[0], -ax_pos[1])
        return(bbox)
        
    def annotate(self, text, x_1, cs_1, \
        x_2 = None, cs_2 = ['axes mm', 'axes mm'], **kwargs):
        """
        Adds an annotation to the axes.  Annotations can be just text or 
        complex arrows with circled text, depending on the keyword arguments.  
        This method is essentially a wrapper around matplotlib's ax.annotate 
        method.
        
        Parameters
        ----------
        text: string
            Text to add to the axes.  Input an empty string ('') to omit text.
        x_1: 1x2 numpy array or list
            Coordinates of the start of the annotation.  The coordinate 
            system(s) is specified in `cs_1`.  If text is supplied, it is 
            placed at this location.
        cs_1: string or list
            Coordinate system(s) for the values in `x_1`.  Input a single 
            string to make both coordinates in `x_1` use the same coordinate 
            system.  Input a 1x2 list to specify different coordinate systems 
            for each coordinate in `x_1`.  Valid coordinate system choices 
            include:
            
            * 'figure mm'       : mm from the lower left corner of the figure
            * 'figure fraction' : 0,0 is lower left of figure and 1,1 is upper, right
            * 'axes mm'         : mm from lower left corner of axes
            * 'axes fraction'   : 0,0 is lower left of axes and 1,1 is upper right
            * 'offset mm'       : Specify an offset (in mm) from the `x_2` value
            * 'data'            : use the axes data coordinate system
            
        x_2: 1x2 numpy array, optional
            Coordinates of the end of the annotation.  The coordinate system is 
            specified in `cs_2`.  If an arrow is specified, the arrowhead is
            placed at this location.
        cs_2: string or list, optional
            Coordinate system for the values in `x_2`.  See description for 
            `cs_1` for further information.
        kwargs:
            Keyword arguments to matplotlib's annotate function.  See the
            `matplotlib documentation <http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.annotate>`__
            for further details
            
        Returns
        -------
        ann_obj: annotation object
        
        See Also
        --------
        Axes.label_curve : Place multiple labels on a single curve
        Axes.label_curves : Place a label on each curve
        """
        #Matplotlib's annotation function cannot handle None for it's xy input
        if x_2 is None:
            x_2 = x_1
            cs_2 = cs_1
            
        def preprocess(x, cs):
            #Somehow the coordinates can get passed by reference, so we 
            #need to create copies
            x = deepcopy(x)
            #Force the coordinate system inputs to be lists
            cs = _utl.adjust_depth(cs, 1)
            #Matplotlib's annotation function cannot handle one coordinate 
            #system for x_1 and two coordinae systems for x_2, so we just
            #supply a coordinate system for each coordinate in x_1 and x_2                     
            if len(cs) == 1:
                cs.append(cs[0])
            #Convert mm to points
            for i, c in enumerate(cs):
                if c == 'axes mm':
                    cs[i] = 'axes points'
                    x[i] = x[i] * 72.0/25.4
                if c == 'offset mm':
                    cs[i] = 'offset points'
                    x[i] = x[i] * 72.0/25.4
            #Matplotlib's annotation function cannot use lists of coordinate 
            #systems, so we must convert the lists to tuples
            cs = tuple(cs)
            return(x, cs)
        
        [x_1, cs_1] = preprocess(x_1, cs_1)
        [x_2, cs_2] = preprocess(x_2, cs_2)
        
        #Add annotation
        ann_obj = self.mpl_ax.annotate(text, xytext = x_1, textcoords = cs_1, \
            xy = x_2, xycoords = cs_2, clip_on = False, **kwargs)
        return(ann_obj)
        
    def add_text(self, x, txt, font_size = _mpl.rcParams['font.size'], \
        **kwargs):
        """
        Adds text to the axes
        
        Parameters
        ----------
        x : 1x2 numpy array
            Coordinates of the text in mm, relative to the axes lower left 
            corner.
        txt : string
            Text to add to the figure
        font_size : float
            Text font size
        kwargs :
            Keyword arguments to matplotlib's text function
            
        Returns
        -------
        txt_obj : text object
        
        See Also
        --------
        annotate : adds an annotation to the axes
        """
        #Convert into normalized figure coordinates
        ax_size = self.size
        x_nac = _np.array(x) / ax_size
        #Convert to pixels
        x_pix = self.mpl_ax.transAxes.transform(x_nac)
        #Convert back to data coordinates
        pix_2_data = self.mpl_ax.transData.inverted()
        x_dc = pix_2_data.transform(x_pix)
        #Add text to the figure
        txt_obj = self.mpl_ax.text(x_dc[0], x_dc[1], txt, \
            fontsize = font_size, **kwargs)
        return(txt_obj)
    
    def add_line(self, x, **kwargs):
        """
        Adds a 2D line to the axes
        
        Parameters
        ----------
        x : Nx2 numpy array
            Coordinates of the line in mm, relative to the axes lower left 
            corner.  Each row contains a point on the line.  Coordinates can be
            outside the plotting area.
        kwargs :
            Keyword arguments to matplotlib's Line2D class
            
        Returns
        -------
        line_obj : matplotlib line object
        
        See Also
        --------
        annotate : adds an annotation to the axes
        """
        #Convert the coordinates into normalized axes coordinates
        ax_size = self.size
        x_nac = _np.array(x)
        x_nac[:,0] = x_nac[:,0] / ax_size[0]
        x_nac[:,1] = x_nac[:,1] / ax_size[1]
        #Create the line object
        line_obj = _mpl_Line2D(x_nac[:,0], x_nac[:,1], \
            transform = self.mpl_ax.transAxes, clip_on = False, **kwargs)
        #Add the line to the axes
        self.mpl_ax.add_line(line_obj)        
        return(line_obj)
        
    def add_circle(self, x, r, cs = 'axes mm', **kwargs):
        """
        Adds a circle to the axes
        
        Parameters
        ----------
        x : 1x2 numpy array
            Coordinates of the circle center.  The coordinate system is 
            specified in `cs`.
        r : float
            Radius of the circle.  The coordinate system is specified in `cs`.
        cs :             
            Coordinate system for the values in `x` and `r`.  Valid coordinate 
            system choices include:
            
            * 'axes mm'         : mm from lower left corner of axes
            * 'data'            : use the axes data coordinate system
            
        kwargs:
            Keyword arguments to matplotlib's Circle class
            
        Returns
        -------
        patch_obj: matplotlib patch object
        """
        x = _np.array(x)
        if cs == 'axes mm':
            #Convert the coordinates into normalized axes coordinates
            ax_size = self.size
            x_cs = x / ax_size
            trans_obj = self.mpl_ax.transAxes
        elif cs == 'data':
            x_cs = x
            trans_obj = self.mpl_ax.transData
        else:
            raise IOError('ERROR: Coordinate system not recognized')
        #Create the polygon object
        patch_obj = _mpl_patches.Circle(x_cs, r, \
            transform = trans_obj, clip_on = False, **kwargs)
        #Add the polygon to the axes
        self.mpl_ax.patches.append(patch_obj)
        return(patch_obj)
        
#    def add_polygon(self, x, **kwargs):
#        """
#        Adds a polygon to the axes
#        
#        Parameters
#        ----------
#        x: Nx2 numpy array
#            Coordinates of the polygon in mm, relative to the axes lower left 
#            corner.  Each row contains a vertex of the polygon.  Coordinates 
#            can be outside the plotting area.
#        kwargs:
#            Keyword arguments to matplotlib's Polygon class
#            
#        Returns
#        -------
#        patch_obj: matplotlib patch object
#        """
#        #Convert the coordinates into normalized axes coordinates
#        ax_size = self.size
#        x_nac = _np.array(x)
#        x_nac[:,0] = x_nac[:,0] / ax_size[0]
#        x_nac[:,1] = x_nac[:,1] / ax_size[1]
#        #Create the polygon object
#        patch_obj = _mpl_patches.Polygon(x_nac, \
#            transform = self.mpl_ax.transAxes, clip_on = False, **kwargs)
#        #Add the polygon to the axes
#        self.mpl_ax.patches.append(patch_obj)
#        return(patch_obj)
        
    

class _Data_Axes_Base(_Axes_Base):   
    
    def add_image(self, im, **kwargs):
        """
        Adds an image to the current axes
        
        Parameters
        ----------
        im : MxN or MxNx3 numpy array
            Image to be added to axes
        x : 1x2 numpy array, optional
            Image x position.
        y : 1x2 numpy array, optional
            Image y position.
        xy_coords : string, optional
            Defines the meaning of `x` and `y` coordinates.  If 'edges' is 
            input, then the image edges will correspond to the coordinates in 
            `x` and `y`.  If 'pixel centers' is input then the center of the 
            pixels at the image edges will correspond to the coordinates in 
            `x` and `y`.
        im_origin : string, optional
            Origin for the image indices.  If 'upper left' is input, then the 
            [0,0] index is the upper left of the image, with positive y being
            downwards.  If 'lower left' is input, then the [0,0] index is the 
            lower left of the image, with positive y being upwards.
        im_interp : string, optional
            Image interpolation method.  See the `matplotlib documentation
            <http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.imshow>`__
            for acceptable values.
        c_map : string, optional
            Image color map.
        c_lim : 1x2 list, optional
            Color map limits.  To automatically chose a limit, input 'auto' for
            either the upper or lower limit.
            
        Returns
        -------
        im_obj : matplotlib image object
        
        See Also
        --------
        Figure.add_color_bar() : Adds a color bar to the figure
        """
        x = kwargs.pop('x', _np.array([0.0, float(im.shape[1])]))
        y = kwargs.pop('y', _np.array([0.0, float(im.shape[0])]))
        xy_coords = kwargs.pop('xy_coords', 'edges')
        im_origin = kwargs.pop('im_origin', 'upper left')
        im_interp = kwargs.pop('im_interp', 'auto')
        c_map = kwargs.pop('c_map', 'auto')
        c_lim = kwargs.pop('c_lim', ['auto','auto'])
        
        self._ui_c_lim = c_lim
        im_error = """Do not recognize image type.  Please verify you have 
        supplied an image.  If so, additional functionality may need to be 
        implemented."""
        if im.ndim == 2:
            if im.dtype is _np.dtype('uint8'):
                #Set color map and limits for a grayscale image
                if c_map == 'auto':
                    c_map = _mpl.cm.gray
                if c_lim[0] == 'auto' and c_lim[1] == 'auto':
                    c_lim = [0, 255]
                im_type = 'grayscale'
            else:
                #Set the color map and limits for an image full of values
                if c_map == 'auto':
                    c_map = _cp.colors.c_maps['rainbow']
                #(Hard code auto tick spacing because the color bar tick 
                #spacing will be recalculated when the color bar is added to 
                #the figure.)
                [c_lim, c_tick, n_tick] = _utl.find_and_select_lim_and_tick(\
                    c_lim, 'auto', [_np.nanmin(im), _np.nanmax(im)], \
                    'linear', 10.0, 0.0)
                im_type = 'values'
        elif im.ndim == 3:
            if im.shape[2] == 3:
                #Set color map for a RGB image
#                if _np.min(im) < 0 or _np.max(im) > 1:
#                    raise ValueError("""The red, green, and blue channels in RGB 
#                    images should contain values between 0 and 1.""")
                if c_map == 'auto':
                    c_map = _cp.colors.c_maps['rainbow']
                im_type = 'RGB'
            else:
                raise ValueError(im_error)
        else:
            raise ValueError(im_error)  

        if xy_coords == 'pixel centers':
            #Find the x and y per image pixel distance
            dx = (x[1] - x[0]) / (im.shape[1] - 1)
            dy = (y[1] - y[0]) / (im.shape[0] - 1)
            #Define the image edge extents
            im_ext = [min(x) - dx / 2.0, max(x) + dx / 2.0, \
                         min(y) - dy / 2.0, max(y) + dy / 2.0]
        elif xy_coords == 'edges':
            #Define the image edge extents
            im_ext = [x[0], x[1], y[0], y[1]]
        else:
            raise IOError("ERROR: Did not recognize 'xy_coords' string")
        
        #Place image
        #(cmap is ignored if im has RGB(A) information)
        im_obj = self.mpl_ax.imshow(im, extent = im_ext, \
               cmap = c_map, aspect = 'auto', origin = im_origin.split()[0])
        #Store image type in case other methods, such as the colorbar need to 
        #know
        im_obj.im_type = im_type              
               
        #Set the color map limits 
        #(Note this must be done before c_bar.solids.set_edgecolor('face'), 
        #which is inside color_bar, or else you get white lines on the color 
        #bar.)
        if c_lim[0] != 'auto' and c_lim[1] != 'auto':
            im_obj.set_clim(c_lim[0], c_lim[1])
        #Select the proper interpolation type for the image
        _utl.set_im_interp(im_interp, im_obj, self)
        
        return(im_obj)

class Invisible_Axes(_Data_Axes_Base):
    """
    A lightweight set of invisible axes for images, annotations, diagrams, etc.
    """
    
    def __init__(self, fig, **kwargs):
        """
        Creates a lightweight set of invisible axes.
        
        Parameters
        ----------
        fig : figure object
            Figure to place the invisible axes in.
        position : 1x2 list or numpy array, optional
            Position of the lower left corner of the axes with respect to the 
            lower left corner of the figure (in mm)
        size : 1x2 list or numpy array, optional
            Width and height of axes (in mm)
        scale_plot : float, optional
            Scales distances between different objects associated with the axes
            
        Returns
        -------
        axes object
        """
        self.parent_fig = fig
        self.parent_fig.axes.append(self)
        self._ui_pos = kwargs.pop('position', 'auto')
        scale_plot = kwargs.pop('scale_plot', 1.0)
        #Define a scaling dimension for the plot.  This dimension is used in a 
        #number of places to scale the distances between different objects.  
        #Under default settings, the scaling dimension corresponds to the 
        #number of millimeters between tick marks.  
        self.sdim = 20.0 * scale_plot
        size = kwargs.pop('size', _np.array([100, 100]))
        if self._ui_pos == 'auto':
            position = _np.array([30, 30])
        else:
            position = self._ui_pos
        #Generate matplotlib axes object
        fig_size = fig.size
        rect_nfc = _np.hstack([position / fig_size, size / fig_size])
        self.mpl_ax = _plt.axes(rect_nfc, **kwargs)
        #Make the axes invisible 
        self.mpl_ax.set_axis_off()
        #Define how much the data min/max may exceed an axis limit (as a 
        #percentage of the tick mark spacing)        
        self.exceed_lim = 0.02 
        
    @property
    def x_lim(self):
        """
        Gets/sets the x axis limits.  Supply a 1x2 list of floats to 
        explicitly set the upper and lower limits.
        """
        return(self.mpl_ax.get_xlim())

    @x_lim.setter
    def x_lim(self, lim):
        self.mpl_ax.set_xlim(lim)
        
    @property
    def y_lim(self):
        """
        Gets/sets the y axis limits.  Supply a 1x2 list of floats to 
        explicitly set the upper and lower limits.
        """
        return(self.mpl_ax.get_ylim())

    @y_lim.setter
    def y_lim(self, lim):
        self.mpl_ax.set_ylim(lim)
        
    def add_scale_bar(self, length, text, loc = 'lower left', \
        font_size = _mpl.rcParams['font.size']):
        """
        Adds a scale bar just outside of the invisible axes.
        
        Parameters
        ----------
        length : float
            Length of the scale bar in axis data units
        text : str
            Label that delinates the physical length signified by the scale bar
        loc : ['lower left' | 'upper left'], optional
            Scale bar location.  ONLY 'LOWER LEFT' is implemented at this time.
        font_size : float
            Font size of the text
            
        Returns
        -------
        scale_bar : annotation object
        """

        root = [0.0, -5.0]
        gap = 4.0
        #I originally tried to do this with annotations, but I could not figure
        #out how to change the capstyle, as documented, here
        #https://github.com/matplotlib/matplotlib/issues/4332
#        offset_pos = [length + gap, 0.0]
#        scale_bar = self.annotate(text, offset_pos, 'offset mm', \
#            x_2 = root, cs_2 = 'axes mm', size = font_size, \
#            va = 'center', ha = 'left', fontname = 'sans-serif', \
#            arrowprops=dict(arrowstyle='-', connectionstyle='arc3, rad=0.0', \
#            fc='none', shrinkA = gap * 72.0 / 25.4, shrinkB = 0.0, \
#            linewidth = 8, solid_capstyle = 'butt'))
        x_lim = self.x_lim
        length_mm = length * self.size[0] / (x_lim[1] - x_lim[0])
        scale_bar = []
        scale_bar.append(self.add_line(_np.array([root, [length_mm, root[1]]]), \
            linewidth = 8.0, color = [0,0,0]))
        scale_bar.append(self.add_text(_np.array([root[0] + length_mm + gap, \
            root[1] - font_size * 25.4/72.0 * 0.1]), text, ha = 'left', va = 'center'))
        return(scale_bar)

class Axes(_Data_Axes_Base):
    """
    A generic axes class to plot data on.    
    """
    def __init__(self, fig, **kwargs):
        """
        Instantiates a generic axes object to plot data on.        
        
        Parameters
        ----------
        fig : figure object
            Figure to place the axes in.
        position : 1x2 numpy array, optional
            Position of axes in mm from the lower left corner of the figure.
        size : 1x2 numpy array, optional
            Width and height of axes in mm.
        scale_plot : float, optional
            Scales distances between different objects associated with the axes
        font_size : float, optional
            Font size of text associated with the axes
        share_x_ax : axes object, optional
            Share the x axis with a different set of axes to create a plot 
            with two y axes.
        share_y_ax : axes object, optional
            Share the y axis with a different set of axes to create a plot 
            with two x axes. 
        link_x_ax : axes object, optional
            Link the x axis with a different set of axes.  The linked x axes
            will be constrained to have the same limits and tick mark spacings.
            By default, the new axes will be placed above the original axes.
        link_y_ax : axes object, optional
            Link the y axis with a different set of axes.  The linked x axes
            will be constrained to have the same limits and tick mark spacings.
            By default, the new axes will be placed to the right of the 
            original axes.
        """      
        self.parent_fig = fig
        self.parent_fig.axes.append(self)
        self._ui_pos = kwargs.pop('position', 'auto')
        scale_plot = kwargs.pop('scale_plot', 1.0)
        #Define a scaling dimension for the plot.  This dimension is used in a 
        #number of places to scale the distances between different objects.  
        #Under default settings, the scaling dimension corresponds to the 
        #number of millimeters between tick marks.  
        self.sdim = 20.0 * scale_plot
        #Define how much the data min/max may exceed an axis limit (as a 
        #percentage of the tick mark spacing)        
        self.exceed_lim = 0.02 
        #Set the font size
        self.font_size = kwargs.pop('font_size', _mpl.rcParams['font.size'])
        #Set the physical distance between tick marks
        self._x_tick_mm = 20 * scale_plot
        self._y_tick_mm = 20 * scale_plot
        
        #Set the log base for log scaled axes
        self._x_scale_log_base = 10.0
        self._y_scale_log_base = 10.0
        
        #Set default lims and ticks
        self._ui_x_lim = ['auto', 'auto']
        self._ui_y_lim = ['auto', 'auto']
        self._ui_x_tick = 'auto'
        self._ui_y_tick = 'auto'
        self._ui_x_tick_list = 'auto'
        self._ui_y_tick_list = 'auto'
        self._ui_x_tick_labels = 'auto'
        self._ui_y_tick_labels = 'auto'
        
        #Set the initial tick spacing values
        self._x_tick = 0.2
        self._y_tick = 0.2
        #Set auto color index to zero
        #(This keeps track of the last color used, so that it is easy to add 
        #curves to a set of axes)
        self.color_ndx = 0
        self.marker_color_ndx = 0
        self.err_color_ndx = 0        
        
        self.shared_x_ax = kwargs.pop('share_x_ax', None)
        self.shared_y_ax = kwargs.pop('share_y_ax', None)
        #Create a set to store the linked x and y axes.  (Sets make it easy
        #to have a list of unique items.)
        self.linked_x_ax = set()
        link_x_ax = kwargs.pop('link_x_ax', None)
        self.linked_y_ax = set()
        link_y_ax = kwargs.pop('link_y_ax', None)
        fig_size = fig.size          
                 
        if self.shared_x_ax is not None:
            #Generate matplotlib axes object 
            self.mpl_ax = self.shared_x_ax.mpl_ax.twinx()
            #Add the axes object to the linked set
            self.linked_x_ax.add(self.shared_x_ax)
            self.linked_x_ax.update(self.shared_x_ax.linked_x_ax)
            #Inform the other axes object that its x-axis is being shared
            self.shared_x_ax.shared_x_ax = self
            #Inform the other linked axes that their x-axis is being linked
            for la in self.linked_x_ax:
                la.linked_x_ax.add(self)
            #Make the number of y ticks match the shared axis
            n_tick = self.shared_x_ax.size[1]/self._y_tick_mm
            self.mpl_ax.set_ylim(0.0, self._y_tick * n_tick)
        elif self.shared_y_ax is not None:
            #Generate matplotlib axes object 
            self.mpl_ax = self.shared_y_ax.mpl_ax.twiny()
            #Add the axes object to the linked set
            self.linked_y_ax.add(self.shared_y_ax)
            self.linked_y_ax.update(self.shared_y_ax.linked_y_ax)
            #Inform the other axes object that its y-axis is being shared
            self.shared_y_ax.shared_y_ax = self
            #Inform the other linked axes that their y-axis is being linked
            for la in self.linked_y_ax:
                la.linked_y_ax.add(self)
            #Make the number of x ticks match the shared axis
            n_tick = self.shared_y_ax.size[1]/self._x_tick_mm
            self.mpl_ax.set_xlim(0.0, self._x_tick * n_tick)
        else:
            #Set the position of the axes
            if self._ui_pos == 'auto':
                position = _np.array([30, 30])
            else:
                position = self._ui_pos
            #Initialize an array to store the initial size of the axes
            size = _np.zeros([2])
            if link_x_ax is not None:
                #Add specified axes and its linked axes to linked axes set
                self.linked_x_ax.add(link_x_ax)
                self.linked_x_ax.update(link_x_ax.linked_x_ax)
                #Inform the other axes objects that their x-axis obects are 
                #being linked
                for la in link_x_ax.linked_x_ax:
                    la.linked_x_ax.add(self)
                #(Make sure to add the current axis to the linked axes last, so 
                #that the current axis doesn't get added to itself)
                link_x_ax.linked_x_ax.add(self)
                #Define the axis object that mpl will actually share
                link_mpl_x = link_x_ax.mpl_ax
                #Initialize the linked axis with the same physical distance
                #between the tick marks
                self._x_tick_mm = link_x_ax._x_tick_mm
                if self._ui_pos == 'auto':
                    #Place the linked axes above the original axes
                    position = link_x_ax.position
                    position[1] = position[1] + link_x_ax.size[1] + self.sdim
                    size[0] = link_x_ax.size[0]
            else:
                link_mpl_x = None
                size[0] = 1.0 / self._x_tick * self._x_tick_mm
            if link_y_ax is not None:
                #Add specified axes and its linked axes to linked axes set
                self.linked_y_ax.add(link_y_ax)
                self.linked_y_ax.update(link_y_ax.linked_y_ax)
                #Inform the other axes object that its x-axis is being linked
                for la in link_y_ax.linked_y_ax:
                    la.linked_y_ax.add(self)
                #(Make sure to add the current axis to the linked axes last, so 
                #that the current axis doesn't get added to itself)
                link_y_ax.linked_y_ax.add(self)
                #Define the axis object that mpl will actually share
                link_mpl_y = link_y_ax.mpl_ax
                #Initialize the linked axis with the same physical distance
                #between the tick marks
                self._y_tick_mm = link_y_ax._y_tick_mm
                if self._ui_pos == 'auto':
                    #Place the linked axes to the right of the original axes
                    position = link_y_ax.position
                    position[0] = position[0] + link_y_ax.size[0] + self.sdim
                    size[1] = link_y_ax.size[1]
            else:
                link_mpl_y = None
                size[1] = 1.0 / self._y_tick * self._y_tick_mm
            #Generate matplotlib axes object
            rect_nfc = _np.hstack([position / fig_size, size / fig_size])
            self.mpl_ax = fig.mpl_fig.add_axes(rect_nfc, sharex = link_mpl_x, \
                sharey = link_mpl_y, **kwargs)
        
        #Set tick mark properties: fontsize, remove tick marks from top 
        #and right of plot
        self.mpl_ax.xaxis.set_tick_params(which = 'both', \
            labelsize = self.font_size, top = False)
        self.mpl_ax.yaxis.set_tick_params(which = 'both', \
            labelsize = self.font_size, right = False)
        if abs(scale_plot - 1.0) > 1e-10:
            _warnings.warn("""Warning: Due to a bug in matplotlib (github issue #4346)
                the tick marks and the spaced between the tick marks and the
                tick mark labels cannot be scaled while creating the plot.  
                You can, however, scale them after the plot has been created.""")
            
#        self.mpl_ax.xaxis.set_tick_params(which = 'major', \
#            labelsize = self.font_size, top = False, \
#            size = _mpl.rcParams['xtick.major.size'] * scale_plot, \
#            pad = _mpl.rcParams['xtick.major.pad'] * scale_plot)
#        self.mpl_ax.yaxis.set_tick_params(which = 'major', \
#            labelsize = self.font_size, right = False, \
#            size = _mpl.rcParams['ytick.major.size'] * scale_plot, \
#            pad = _mpl.rcParams['ytick.major.pad'] * scale_plot)
#        self.mpl_ax.xaxis.set_tick_params(which = 'minor', \
#            labelsize = self.font_size, top = False, \
#            size = _mpl.rcParams['xtick.minor.size'] * scale_plot, \
#            pad = _mpl.rcParams['xtick.minor.pad'] * scale_plot)
#        self.mpl_ax.yaxis.set_tick_params(which = 'minor', \
#            labelsize = self.font_size, right = False, \
#            size = _mpl.rcParams['ytick.minor.size'] * scale_plot, \
#            pad = _mpl.rcParams['ytick.minor.pad'] * scale_plot)
            
        #Instantiate the x and y labels       
        self.x_label_obj = _axis_label.Axis_Label(self, 0)
        self.y_label_obj = _axis_label.Axis_Label(self, _np.pi/2.0)
        
        #Initialize the list of curves
        #(The mpl axes object has it's own list of line objects, but that 
        #includes any lines that have been added to the axes.  I want just a
        #list of curves that have been plotted.)
        self.curves = []
        #Initialize the list of markers and bars
        #(Separating out different objects makes it easier to label just the 
        #curves or just the markers)
        self.markers = []
        self.bars = []
        self.boxes = []
        self.violins = []            
            
        if self.shared_x_ax is not None:
            self.mpl_ax.yaxis.set_ticks_position('right')
            #There is no need to have overlapping axis spines.
            for key in self.mpl_ax.spines.keys():
                self.mpl_ax.spines[key].set_visible(False)
            #Start the auto color indexing where the last axes left off
            self.color_ndx = self.shared_x_ax.color_ndx
            self.marker_color_ndx = self.shared_x_ax.marker_color_ndx
            self.err_color_ndx = self.shared_x_ax.err_color_ndx
            self.y_tick_list = self._ui_y_tick_list
        if self.shared_y_ax is not None:
            self.mpl_ax.xaxis.set_ticks_position('top')
            #There is no need to have overlapping axis spines.
            for key in self.mpl_ax.spines.keys():
                self.mpl_ax.spines[key].set_visible(False)
            #Start the auto color indexing where the last axes left off
            self.color_ndx = self.shared_y_ax.color_ndx
            self.marker_color_ndx = self.shared_y_ax.marker_color_ndx
            self.err_color_ndx = self.shared_y_ax.err_color_ndx
        if link_x_ax is not None:
            self._ui_x_lim = link_x_ax._ui_x_lim
            self._ui_x_tick = link_x_ax._ui_x_tick
#            self._set_x_lim_and_tick(self.linked_x_ax.x_lim, self.linked_x_ax.x_tick)
        if link_y_ax is not None:
            self._ui_y_lim = link_y_ax._ui_y_lim
            self._ui_y_tick = link_y_ax._ui_y_tick
#            self._set_y_lim_and_tick(self.linked_y_ax.y_lim, self.linked_y_ax.y_tick)
        
#        #Set the axis scaling.  (This appears to change the limits and tick 
#        #marks in matplotlib 1.3.1, which might be a bug.  We avoid the issue 
#        #by setting the scaling before setting the tick marks.)
#        self.x_scale = 'linear'
#        self.y_scale = 'linear'
#        self.mpl_ax.set_xlim(0,1)
#        self.mpl_ax.set_ylim(0,1)

    @property
    def x_scale(self):
        """
        Gets/sets the scaling for the x-axis.  Valid inputs include 'linear' 
        and 'log'.  Note: if you change the scaling when the axis limits 
        and ticks are set to 'auto' (the default), then the limits and ticks 
        will be recomputed.
        """
        return(self.mpl_ax.get_xscale())

    @x_scale.setter
    def x_scale(self, x_scale):
        b = self._x_scale_log_base
        #Matplotlib places floor(b) - 2 minor ticks at 2*b^n, 3*b^n, 4*b^n, 
        #etc.  This results in only one minor tick mark for natural log scaled 
        #axes.  Instead we just place 9 linearly spaced tick marks.
        if _np.abs(b - _np.e) < 1e-12:
            minor_ticks = _np.arange(0.1*(b-1.0)+1.0, \
                0.9*(b-1.0)+1.0+b/100.0, 0.1*(b-1.0))
        else:
            minor_ticks = None
        self.mpl_ax.set_xscale(x_scale, basex = b, subsx = minor_ticks)
        self._select_and_set_x_lim_and_tick(self._ui_x_lim[:], self._ui_x_tick)
        #If using a base e logarithm, label major ticks using 'e^z' rather
        #than 2.718281828459045^z
        #(We need to put this here rather than inside the x_scale_log_base 
        #setter because the mpl_ax.set_xscale() method overrides any previously
        #specified formatters.)
        if _np.abs(b - _np.e) < 1e-12:
            def ticks(n, pos):
                return r'e$^{:.0f}$'.format(_np.log(n))
            self.mpl_ax.xaxis.set_major_formatter(\
                _mpl.ticker.FuncFormatter(ticks))

    @property
    def x_scale_log_base(self):
        """
        Gets/sets the logarithmic base for log scaling on the x-axis.
        """
        return(self._x_scale_log_base)
       
    @x_scale_log_base.setter
    def x_scale_log_base(self, log_base):
        self._x_scale_log_base = log_base
        #Reset the axis scaling
        self.x_scale = self.x_scale
    
    @property
    def y_scale(self):
        """
        Gets/sets the scaling for the y-axis.  Valid inputs include 'linear' 
        and 'log'.  Note: if you change the scaling when the axis limits 
        and ticks are set to 'auto' (the default), then the limits and ticks 
        will be recomputed.
        """
        return(self.mpl_ax.get_yscale())
    
    @y_scale.setter
    def y_scale(self, y_scale):
        b = self._y_scale_log_base
        #Matplotlib places floor(b) - 2 minor ticks at 2*b^n, 3*b^n, 4*b^n, 
        #etc.  This results in only one minor tick mark for natural log scaled 
        #axes.  Instead we just place 9 linearly spaced tick marks.
        if _np.abs(b - _np.e) < 1e-12:
            minor_ticks = _np.arange(0.1*(b-1.0)+1.0, \
                0.9*(b-1.0)+1.0+b/100.0, 0.1*(b-1.0))
        else:
            minor_ticks = None
        self.mpl_ax.set_yscale(y_scale, basey = b, subsy = minor_ticks)
        self._select_and_set_y_lim_and_tick(self._ui_y_lim[:], self._ui_y_tick)
        #If using a base e logarithm, label major ticks using 'e^z' rather
        #than 2.718281828459045^z
        #(We need to put this here rather than inside the y_scale_log_base 
        #setter because the mpl_ax.set_yscale() method overrides any previously
        #specified formatters.)
        if _np.abs(b - _np.e) < 1e-12:
            def ticks(n, pos):
                return r'e$^{{{:.0f}}}$'.format(_np.log(n))
            self.mpl_ax.yaxis.set_major_formatter(\
                _mpl.ticker.FuncFormatter(ticks))

            
    @property
    def y_scale_log_base(self):
        """
        Gets/sets the logarithmic base for log scaling on the y-axis.
        """
        return(self._y_scale_log_base)
       
    @y_scale_log_base.setter
    def y_scale_log_base(self, log_base):
        self._y_scale_log_base = log_base
        #Reset the axis scaling
        self.y_scale = self.y_scale
        
    @property
    def x_lim(self):
        """
        Gets/sets the x axis limits.  Supply a 1x2 list of floats to 
        explicitly set the upper and lower limits.  If the string 'auto' is 
        input instead of a float, then the corresponding limit will be 
        automaticaly selected.
        """
        return(list(self.mpl_ax.get_xlim()))

    @x_lim.setter
    def x_lim(self, lim):
        #(Copy the limits in case `lim` changes later)
        self._ui_x_lim = lim[:]
        tick = self._ui_x_tick
        [lim, tick] = self._select_and_set_x_lim_and_tick(lim, tick)
        return(lim, tick)
        
    @property
    def x_tick(self):
        """
        Gets/sets the x axis tick mark spacing.  Supply a float to explicitly
        set the tick marks spacing.  If `x_tick` is set to 'auto', then the 
        tick mark spacing will be automatically selected.
        """
        return(self._x_tick)
        
    @x_tick.setter
    def x_tick(self, tick):
        self._ui_x_tick = tick
        lim = self._ui_x_lim
        [lim, tick] = self._select_and_set_x_lim_and_tick(lim, tick)
        return(lim, tick)
    
    @property
    def _num_x_tick(self):
        """
        Gets the number of x-axis tick marks
        """
        lim = self.x_lim
        if self.x_scale == 'log':
            num_tick = (_np.log(lim[1])/_np.log(self._x_scale_log_base) - \
                _np.log(lim[0])/_np.log(self._x_scale_log_base)) / self.x_tick
        else:
            num_tick = (lim[1] - lim[0]) / self.x_tick
        return(num_tick)
        
    def _select_and_set_x_lim_and_tick(self, lim, tick):
        """
        Selects and sets the x limits and the x tick spacing.  The x_lim and 
        x_tick setters perform the same operation, but they each recalculate 
        the automatically selected limits and tick spacing in order to keep the 
        user interface simple.  This method computes the limits and tick 
        spacing once.
        """
        #Get the data limits on current and linked axes
        data_lims = []
        data_lims.append(self.mpl_ax.xaxis.get_data_interval())
        for la in self.linked_x_ax:
            data_lims.append(la.mpl_ax.xaxis.get_data_interval()) 
        data_lims = _np.array(data_lims)
        data_lim = [_np.min(data_lims[:,0]), _np.max(data_lims[:,1])]
        #Automatically select candidates for the limits and tick mark spacing
        [lim_c, tick_c, n_tick_c] = _utl.find_candidate_lim_and_tick(lim, \
            tick, data_lim, self.x_scale, self._x_scale_log_base, self.exceed_lim)

        #The automatically found limits and tick mark spacings can result in an 
        #unequal number of tick marks on the first y-axis and the second 
        #y-axis.  This is not good, and should be rectified if possible.
        if self.shared_y_ax is not None:
            #Find the possible limits and tick mark spacings for the x-axis 
            #whose corresponding y-axis is being shared
            s_data_lim = self.shared_y_ax.mpl_ax.xaxis.get_data_interval()
            [s_lim_c, s_tick_c, s_n_tick_c] = _utl.find_candidate_lim_and_tick(\
                self.shared_y_ax._ui_x_lim, self.shared_y_ax._ui_x_tick, \
                s_data_lim, self.shared_y_ax.x_scale, self.shared_y_ax._x_scale_log_base, \
                self.shared_y_ax.exceed_lim)
            #Find the differences between the number of tick marks on the two
            #x-axes
            abs_diff = _np.zeros([len(n_tick_c), len(s_n_tick_c)])
            for i, n_tick in enumerate(n_tick_c):
                abs_diff[i,:] = _np.abs(s_n_tick_c - n_tick)
            #Select the limits and tick mark spacing combo with the smallest
            #difference in the number of tick marks
            [a,b] = _np.where(abs_diff == _np.min(abs_diff))
            a = a[0]
            b = b[0]
            tick = tick_c[a]
            n_tick = n_tick_c[a]
            s_tick = s_tick_c[b]
            s_n_tick = s_n_tick_c[b]
            #If there is a combo that has the same number of tick marks, select
            #it.  If not then adjust the limits, tick mark spacing, or the 
            #physical distance between the tick marks.
            if abs_diff[a,b] < 1e-10:
                lim = lim_c[a,:]
                s_lim = s_lim_c[b,:]
            else:
                [lim, tick_mm, s_lim] = self._adjust_shared_lim( \
                    self._ui_x_lim, lim_c[a,:], tick, self.x_tick_mm, n_tick, \
                    self.x_scale, self._x_scale_log_base, \
                    self.shared_y_ax._ui_x_lim, s_lim_c[b,:], s_tick, \
                    self.shared_y_ax.x_tick_mm, s_n_tick, \
                    self.shared_y_ax.x_scale, self.shared_y_ax._x_scale_log_base)
                self._x_tick_mm = tick_mm
                self.x_label_obj._tick_mm = tick_mm 
            self.shared_y_ax._set_x_lim_and_tick(s_lim, s_tick)
        else:
            [lim, tick, n_tick] = _utl.select_lim_and_tick(lim_c, tick_c, \
                n_tick_c) 

        #Force the linked/shared axis to have the same limits and ticks
        for la in self.linked_x_ax:
            la._set_x_lim_and_tick(lim, tick)
        #Apply the limits and tick mark spacing
        self._set_x_lim_and_tick(lim, tick)
        return(lim, tick)
        
    def _set_x_lim_and_tick(self, lim, tick):
        """
        Sets the x limits and the x tick spacing
        """
        #Set the limits and tick mark spacing
        self.mpl_ax.set_xlim(lim)
        self._x_tick = tick
        #Get the number of tick marks (not including the first one)
        #(we make sure to do this after the limits and tick mark spacing have
        #been set)
        n_tick = self._num_x_tick        
        self.x_tick_list = self._ui_x_tick_list
        self.x_tick_labels = self._ui_x_tick_labels
        self.size = _np.array([n_tick * self._x_tick_mm, self.size[1]])
        self._update_clipping_mask()
        if self.x_label_obj.anno is not None:
            self.x_label_obj.place_label()
        if self.mpl_ax.yaxis.get_label_position() == 'right' and \
            self.y_label_obj.anno is not None:
            self.y_label_obj.place_label()
        #Draw a dashed line across plot if axis spans zero 
        self._line_at_zero(lim, tick, [0.0, 0.0], [0.0, 1.0], \
            self.mpl_ax.transData, self.mpl_ax.transAxes)      
            
    @property
    def y_lim(self):
        """
        Gets/sets the y axis limits.  Supply a 1x2 list of floats to 
        explicitly set the upper and lower limits.  If the string 'auto' is 
        input instead of a float, then the corresponding limit will be 
        automaticaly selected.
        """
        return(list(self.mpl_ax.get_ylim()))
        
    @y_lim.setter
    def y_lim(self, lim):
        #Copy the limits in case `lim` changes later
        self._ui_y_lim = lim[:]
        tick = self._ui_y_tick
        [lim, tick] = self._select_and_set_y_lim_and_tick(lim, tick)
        return(lim, tick)
        
    @property
    def y_tick(self):
        """
        Gets/sets the y axis tick mark spacing.  Supply a float to explicitly
        set the tick marks spacing.  If `y_tick` is set to 'auto', then the 
        tick mark spacing will be automatically selected.
        """
        return(self._y_tick)
        
    @y_tick.setter
    def y_tick(self, tick):
        self._ui_y_tick = tick
        lim = self._ui_y_lim
        [lim, tick] = self._select_and_set_y_lim_and_tick(lim, tick)
        return(lim, tick)
        
    @property
    def _num_y_tick(self):
        """
        Gets the number of y-axis tick marks
        """
        lim = self.y_lim
        if self.y_scale == 'log':
            num_tick = (_np.log(lim[1])/_np.log(self._y_scale_log_base) - \
                _np.log(lim[0])/_np.log(self._y_scale_log_base)) / self.y_tick
        else:
            num_tick = (lim[1] - lim[0]) / self.y_tick
        return(num_tick)
        
    def _select_and_set_y_lim_and_tick(self, lim, tick):
        """
        Selects and sets the y limits and the y tick spacing.  The y_lim and 
        y_tick setters perform the same operation, but they each recalculate 
        the automatically selected limits and tick spacing in order to keep the 
        user interface simple.  This method computes the limits and tick 
        spacing once.
        """
        #Get the data limits on current and linked axes
        data_lims = []
        data_lims.append(self.mpl_ax.yaxis.get_data_interval())
        for la in self.linked_y_ax:
            data_lims.append(la.mpl_ax.yaxis.get_data_interval())
        data_lims = _np.array(data_lims)
        data_lim = [_np.min(data_lims[:,0]), _np.max(data_lims[:,1])]
        #Automatically select candidates for the limits and tick mark spacing
        [lim_c, tick_c, n_tick_c] = _utl.find_candidate_lim_and_tick(lim, \
            tick, data_lim, self.y_scale, self._y_scale_log_base, self.exceed_lim)
        
        #The automatically found limits and tick mark spacings can result in an 
        #unequal number of tick marks on the first y-axis and the second 
        #y-axis.  This is not good, and should be rectified if possible.
        if self.shared_x_ax is not None:
            #Find the possible limits and tick mark spacings for the y-axis 
            #whose corresponding x-axis is being shared
            s_data_lim = self.shared_x_ax.mpl_ax.yaxis.get_data_interval()
            [s_lim_c, s_tick_c, s_n_tick_c] = _utl.find_candidate_lim_and_tick(\
                self.shared_x_ax._ui_y_lim, self.shared_x_ax._ui_y_tick, \
                s_data_lim, self.shared_x_ax.y_scale, self.shared_x_ax._y_scale_log_base, \
                self.shared_x_ax.exceed_lim)
            #Select the limits and tick mark spacing combo with the smallest
            #difference in the number of tick marks
            abs_diff = _np.zeros([len(n_tick_c), len(s_n_tick_c)])
            for i, n_tick in enumerate(n_tick_c):
                abs_diff[i,:] = _np.abs(s_n_tick_c - n_tick)
            [a,b] = _np.where(abs_diff == _np.min(abs_diff))
            a = a[0]
            b = b[0]
            tick = tick_c[a]
            n_tick = n_tick_c[a]
            s_tick = s_tick_c[b]
            s_n_tick = s_n_tick_c[b]
            #If there is a combo that has the same number of tick marks, select
            #it.  If not then adjust the limits, tick mark spacing, or the 
            #physical distance between the tick marks.
            if abs_diff[a,b] < 1e-10:
                lim = lim_c[a,:]
                s_lim = s_lim_c[b,:]
            else:
                [lim, tick_mm, s_lim] = self._adjust_shared_lim( \
                    self._ui_y_lim, lim_c[a,:], tick, self.y_tick_mm, n_tick, \
                    self.y_scale, self._y_scale_log_base, \
                    self.shared_x_ax._ui_y_lim, s_lim_c[b,:], s_tick, \
                    self.shared_x_ax.y_tick_mm, s_n_tick, \
                    self.shared_x_ax.y_scale, self.shared_x_ax._y_scale_log_base)
                self._y_tick_mm = tick_mm
                self.y_label_obj._tick_mm = tick_mm 
            self.shared_x_ax._set_y_lim_and_tick(s_lim, s_tick)
        else:
            [lim, tick, n_tick] = _utl.select_lim_and_tick(lim_c, tick_c, \
                n_tick_c)  

        #Force the shared/linked axis to have the same limits and ticks
        for la in self.linked_y_ax:
            la._set_y_lim_and_tick(lim, tick)
        #Apply the limits and tick mark spacing
        self._set_y_lim_and_tick(lim, tick)
        return(lim, tick)
        
    def _set_y_lim_and_tick(self, lim, tick):
        """
        Sets the y limits and the y tick spacing
        """
        #Set the limits and tick mark spacing
        self.mpl_ax.set_ylim(lim)
        self._y_tick = tick
        #Get the number of tick marks (not including the first one)
        #(we make sure to do this after the limits and tick mark spacing have
        #been set)
        n_tick = self._num_y_tick    
        self.y_tick_list = self._ui_y_tick_list
        self.y_tick_labels = self._ui_y_tick_labels  
        self.size = _np.array([self.size[0], n_tick * self._y_tick_mm])
        self._update_clipping_mask()
        if self.y_label_obj.anno is not None:
            self.y_label_obj.place_label()
        if self.mpl_ax.xaxis.get_label_position() == 'top' and \
            self.x_label_obj.anno is not None:
            self.x_label_obj.place_label()
        #Draw a dashed line across plot if axis spans zero
        self._line_at_zero(lim, tick, [0.0, 1.0], [0.0, 0.0], \
            self.mpl_ax.transAxes, self.mpl_ax.transData)
        
    def _adjust_shared_lim(self, ui_lim, lim, tick, tick_mm, n_tick, \
        ax_scale, ax_log_base, s_ui_lim, s_lim, s_tick, s_tick_mm, \
        n_s_tick, s_ax_scale, s_ax_log_base):
        """
        Adjusts x/y axis limits for axes with shared y/x axes.  This method
        kinda works, but perhaps it could be better.
        """
        #Define a function to decide which limit to adjust on a given axis, 
        #and to perform the adjustment
        def select_and_adjust_lim(ui_lim, lim, length_diff, tick, \
            ax_scale, ax_log_base):
            #Define a function to adjust the limits            
            def adjust_lim(lmt, n_tick_diff, tick, sign, ax_scale, ax_log_base):
                if ax_scale == 'log':
                    lmt = ax_log_base**(_np.log(lmt)/_np.log(ax_log_base) \
                        + sign * n_tick_diff * tick)
                else:
                    lmt = lmt + sign * n_tick_diff * tick
                return(lmt)
            
            #Find which, if any, limits are to be automatically selected
            ndx_list = _np.where(_np.array(ui_lim) == 'auto')[0]
            if len(ndx_list) > 1:
                #If both limits are 'auto' selected and one limit is 
                #currently at 0, then attempt to preserve it.  Otherwise,
                #adjust the top limit.
                if lim[1] == 0.0:
                    lim[0] = adjust_lim(lim[0], n_tick_diff, tick, -1.0, \
                        ax_scale, ax_log_base)
                else:
                    lim[1] = adjust_lim(lim[1], n_tick_diff, tick, 1.0, \
                        ax_scale, ax_log_base)
            else:
                #Adjust whichever limit is automatically selected.
                ndx = ndx_list[0]
                if ndx == 0:
                    lim[0] = adjust_lim(lim[0], n_tick_diff, tick, -1.0, \
                        ax_scale, ax_log_base)
                else:
                    lim[1] = adjust_lim(lim[1], n_tick_diff, tick, 1.0, \
                        ax_scale, ax_log_base)
            return(lim)
            
            
        length_diff = n_tick * tick_mm - n_s_tick * s_tick_mm
        if length_diff > 1e-12 and 'auto' in s_ui_lim:
            #If the current axes are longer than the shared, adjust the shared.
            n_tick_diff = _np.floor(length_diff / s_tick_mm + 1e-12)
            s_lim = select_and_adjust_lim(s_ui_lim, s_lim, length_diff, \
                s_tick, s_ax_scale, s_ax_log_base)
        elif length_diff < -1e-12 and 'auto' in ui_lim:
            #If the current axes are shorter than the shared, adjust the 
            #current.
            n_tick_diff = -_np.floor(length_diff / tick_mm + 1e-12)
            lim = select_and_adjust_lim(ui_lim, lim, length_diff, tick, \
                ax_scale, ax_log_base)
        
        #Define a function to calculate the number of tick marks along an axis
        def calc_n_tick(lim, tick, ax_scale, ax_log_base):
            if ax_scale == 'log':
                n_tick = (_np.log(lim[1])/_np.log(ax_log_base) - \
                    _np.log(lim[0])/_np.log(ax_log_base)) / tick
            else:
                n_tick = (lim[1] - lim[0]) / tick
            return(n_tick)
        #If physical tick mark spacings are different, then it may be 
        #impossible to make the lengths agree by only adjusting the number of
        #tick marks.  So we need to check if lengths are still different.
        n_tick = calc_n_tick(lim, tick, ax_scale, ax_log_base)
        n_s_tick = calc_n_tick(s_lim, s_tick, s_ax_scale, s_ax_log_base)
        length_diff = n_tick * tick_mm - n_s_tick * s_tick_mm
        #Adjust physical tick mark spacing as a last resort
        if abs(length_diff) > 1E-12:
            tick_mm = n_s_tick * s_tick_mm / n_tick
            _warnings.warn( """Warning: There are two sets of axes that share a 
                x / y axis.  The auto selected (or specified) limits, tick mark
                spacing, and physical distance between tick marks resulted in 
                unequal  y / x axis lengths.  The physical distance between 
                tick marks has been adjusted to force the y / x axis lengths 
                to be equal, which may make the plot aesthetics suffer.""")
        return(lim, tick_mm, s_lim)

    def _update_clipping_mask(self):
        """Cycle thru the curves in the plot, and clip each of them"""
        for line in self.curves:
            #Save the full data set before clipping
            if not hasattr(line, 'full_x_data'):
                line.full_x_data = line.get_xdata()
            if not hasattr(line, 'full_y_data'):
                line.full_y_data = line.get_ydata()
            #Perform the clipping on a copy of the full data set 
            x = _np.copy(line.full_x_data)
            y = _np.copy(line.full_y_data)
            #Clip the copy and update the curve with the clipped data
            #Clip the x data first
            [x_c, y_c] = self._clip_data(x, y, \
                self.x_lim, self.x_tick, self.x_scale, self._x_scale_log_base, \
                line.get_linestyle())
            line.set_xdata(x_c)
            line.set_ydata(y_c)
            #Clipd the y data second
            [y_c, x_c] = self._clip_data(y_c, x_c, \
                self.y_lim, self.y_tick, self.y_scale, self._y_scale_log_base, \
                line.get_linestyle())
            line.set_xdata(x_c)
            line.set_ydata(y_c)
             
    def _clip_data(self, x, y, lims, tick, ax_scale, ax_log_base, line_style):
        """Clips data to limits"""

        #If clip_on = True in ax.plot(), then each curve has it's own 
        #clipping mask, which is really annoying when you just want to 
        #select a curve in Adobe Illustrator. In addition, the data outside
        #the clipping mask is visible once you release the clipping mask.
        #Instead, I have set clip_on = False, and do the clipping by setting
        #the data outside the clipping mask to nan.
        
        #Find the data outside the limits
        #(The following can give "RuntimeWarning: invalid value encountered in 
        #less/greater" when x contains nan, so we temporarily turn off the 
        #warning)
        with _np.errstate(invalid = 'ignore'):
            lgcs = [x < lims[0], x > lims[1]]
        #Don't clip data if the max or min is just slightly beyond the limit
        #(The distance beyond the limit must be calculated differently if 
        #axis has a log scale instead of a normal linear scale.)
        if ax_scale == 'log':
            diff = [_np.log(lims[0])/_np.log(ax_log_base) - \
                _np.log(_np.nanmin(x))/_np.log(ax_log_base), \
                _np.log(_np.nanmax(x))/_np.log(ax_log_base) - \
                _np.log(lims[1])/_np.log(ax_log_base)]
        else:
            diff = [lims[0] - _np.nanmin(x), _np.nanmax(x) - lims[1]]
        if diff[0] < tick * self.exceed_lim:
            lgcs[0] = _np.array([False] * len(x), bool)
        if diff[1] < tick * self.exceed_lim:
            lgcs[1] = _np.array([False] * len(x), bool)
        #Cycle thru the limits
        for lgc, lim in zip(lgcs, lims):
            #We only want to interpolate to the axis limits if lines are being 
            #drawn between the data points
            if line_style.lower() != 'none':
                #Find the indices where the data crosses the limit
                cross_ndx = _np.where(_np.diff(lgc))[0]
                #The data can increase or decrease with index number. In either 
                #case, we want the data point just inside and just outside the limit.
                inside_ndx = _np.concatenate((cross_ndx[lgc[cross_ndx]] + 1, \
                    cross_ndx[~lgc[cross_ndx]]))
                outside_ndx = _np.concatenate((cross_ndx[lgc[cross_ndx]], \
                    cross_ndx[~lgc[cross_ndx]] + 1))
                for i_ndx, o_ndx in zip(inside_ndx, outside_ndx):
                    #Create data points right at the limits using linear 
                    #interpolation
                    #It is important to use only a subset of the data during 
                    #interpolation because there may not always be a 1-to-1 mapping 
                    #between x and y
                    ndx = _np.sort(_np.array([i_ndx,o_ndx]))
                    #Interpolant requires monotonically increasing values of x
                    if _np.diff(x[ndx]) >= 0:
                        y[o_ndx] = _np.interp(lim, x[ndx], y[ndx])
                    else:
                        xr = x[ndx]
                        yr = y[ndx]
                        y[o_ndx] = _np.interp(lim, xr[::-1], yr[::-1])
                    x[o_ndx] = lim
                    lgc[o_ndx] = False
            #Clip the data outside the limits
            #(If the user input a list of integers then they must be converted to
            #floats, since nan is a float)
            try:
                x[lgc] = _np.nan
            except ValueError:
                x = x.astype(float)
                x[lgc] = _np.nan
            try:
                y[lgc] = _np.nan
            except ValueError:
                y = y.astype(float)
                y[lgc] = _np.nan
        return(x, y)

    @property
    def x_tick_mm(self):
        """
        Gets/sets the physical distance (in mm) between the tick marks on the
        x axis.  Input a float to specify a new spacing.
        """
        return(self._x_tick_mm)
        
    @x_tick_mm.setter
    def x_tick_mm(self, tick_mm):
        self._x_tick_mm = tick_mm
        self.size = _np.array([self._num_x_tick * self._x_tick_mm * self.sdim/20.0, \
            self.size[1]])
        if self.x_label_obj is not None:
            self.x_label_obj._tick_mm = tick_mm
            if self.x_label_obj.anno is not None:
                self.x_label_obj.place_label()
            
    @property
    def y_tick_mm(self):
        """
        Gets/sets the physical distance (in mm) between the tick marks on the
        y axis.  Input a float to specify a new spacing.
        """
        return(self._y_tick_mm)
        
    @y_tick_mm.setter
    def y_tick_mm(self, tick_mm):
        self._y_tick_mm = tick_mm
        self.size = _np.array([self.size[0], \
            self._num_y_tick * self._y_tick_mm * self.sdim/20.0])
        if self.y_label_obj is not None:
            self.y_label_obj._tick_mm = tick_mm
            if self.y_label_obj.anno is not None:
                self.y_label_obj.place_label()

    @property
    def x_tick_list(self):
        """
        Gets/sets x-axis tick mark positions.  Supply a list of values to 
        explicitly set the tick mark values.  If `x_tick_list` is set to 
        'auto', then the tick marks will be automaticaly selected.
        """
        return(self.mpl_ax.get_xticks())
        
    @x_tick_list.setter
    def x_tick_list(self, tick_list):
        self._ui_x_tick_list = tick_list
        tick_list = _utl.gen_tick_list(tick_list, self.x_lim, self.x_tick, \
            self.x_scale, self._y_scale_log_base)
        self.mpl_ax.set_xticks(tick_list)
        
    @property
    def y_tick_list(self):
        """
        Gets/sets y-axis tick mark positions.  Supply a list of values to 
        explicitly set the tick mark values.  If `y_tick_list` is set to 
        'auto', then the tick marks will be automaticaly selected.
        """
        return(self.mpl_ax.get_yticks())
        
    @y_tick_list.setter
    def y_tick_list(self, tick_list):
        self._ui_y_tick_list = tick_list
        tick_list = _utl.gen_tick_list(tick_list, self.y_lim, self.y_tick, \
            self.y_scale, self._y_scale_log_base)
        self.mpl_ax.set_yticks(tick_list)
    
    @property
    def x_tick_labels(self):
        """
        Gets/sets x axis tick labels.  Assign a list of strings to set the 
        labels.
        """
        return(self.mpl_ax.get_xticklabels())
    
    @x_tick_labels.setter
    def x_tick_labels(self, labels):
        self._ui_x_tick_labels = labels
        if labels != 'auto':
            set_tick_labels = []
            for label in labels:
                txt = _utl.raw_string(label)
                set_tick_labels.append('$\sf{' + txt + '}$')
            self.mpl_ax.set_xticklabels(set_tick_labels)

    @property
    def y_tick_labels(self):
        """
        Gets/sets y axis tick labels.  Assign a list of strings to set the 
        labels.
        """
        return(self.mpl_ax.get_xticklabels())

    @y_tick_labels.setter
    def y_tick_labels(self, labels):
        self._ui_y_tick_labels = labels
        if labels != 'auto':
            set_tick_labels = []
            for label in labels:
                txt = _utl.raw_string(label)
                set_tick_labels.append('$\sf{' + txt + '}$')
            self.mpl_ax.set_yticklabels(set_tick_labels)

    def _data_preprocessor(self, x, y, x_y_equal_length, n_dim):
        """
        Formats data arrays
        """
        #User may have input x and y data in the form of nested lists.  Data 
        #should be in the form of nested lists of numpy arrays.
        x = self._convert_to_nested_numpy_arrays(x, n_dim)[0]
        y = self._convert_to_nested_numpy_arrays(y, n_dim)[0]
        #Put variables in the proper format        
        x = _utl.adjust_list_depth(x, 1)
        y = _utl.adjust_list_depth(y, 1)

        #Do some input checking
        if len(x) != len(y):
            raise IOError("""The number of x-data sets does not match the number of y-data sets for y-axis""")
        if x_y_equal_length:
            C = len(y)
            for c in range(C):
                if len(x[c]) != len(y[c]):
                    raise IOError("""The length of the x-data and the y-data are not equal for curve %r.""" %(c+1))
        
        return(x, y)
    
    def _convert_to_nested_numpy_arrays(self, g, n_dim):
        """
        Finds the bottom of nested lists and converts to numpy arrays, as 
        needed.
        
        Parameters
        ----------
        g: list
            Nested list of arbitrary depth that may or may not have numpy 
            arrays at the bottom
        n_dim: int
            Number of dimensions for each numpy array
        
        Returns
        -------
        g: list
            Nested list of numpy arrays.
        not_numpy: boolean
            Used during the recurssion process.  Not intended for the end user.
        """
        #Initialize variables used in the recursion process
        not_numpy = False
        #Find out if input is a list
        if isinstance(g, (list)):
            for i, el in enumerate(g):
                #Use recursion to get to the bottom of the lists
                [g[i], not_numpy] = self._convert_to_nested_numpy_arrays(el, n_dim)
                if not_numpy:
                    #Convert list into numpy array
                    g = _np.array(g)
                    not_numpy = False
                    break
        elif not isinstance(g, (_np.ndarray)):
            #Tell parent function to convert parent array into a numpy array
            not_numpy = True
        else:
            #Force numpy array to be 1-D
            if _np.ndim(g) != n_dim:
                if n_dim == 1:
                    g = g.flatten()
                else:
                    raise ValueError("Each data array should be " + str(n_dim) + "-D")
                
        return(g, not_numpy)

    @property
    def x_label(self):
        """Gets/sets the x axis label.  Supply a 1x2 list of strings (in LaTeX 
        syntax) to specify the axis label text and axis units.  The units will 
        automatically be wrapped in paranthesises.  Supply a 1x1 list with a
        single string to create a label without any units."""
        return(self.x_label_obj.str_list)
    
    @x_label.setter   
    def x_label(self, str_list):
        if str_list is not None:
            str_list = _utl.adjust_depth(str_list, 1)
            self.x_label_obj.gen_label(str_list, self.font_size)
            self.x_label_obj.place_label()
    
    @property
    def y_label(self):
        """Gets/sets the y axis label.  Supply a 1x2 list of strings (in LaTeX 
        syntax) to specify the axis label text and axis units.  The units will 
        automatically be wrapped in paranthesises.  Supply a 1x1 list with a 
        single string to create a label without any units."""
        return(self.x_label_obj.str_list)
    
    @y_label.setter
    def y_label(self, str_list):
        if str_list is not None:
            str_list = _utl.adjust_depth(str_list, 1)
            self.y_label_obj.gen_label(str_list, self.font_size)
            self.y_label_obj.place_label()
     
#    def label_x(self, text, units = None):
#        """
#        Label the x-axis.
#        
#        Parameters
#        ----------
#        text : string
#            Axis label text
#        units : string, optional
#            Axis units.  Units are automatically put in parenthesis.
#        """
#        self.x_label.gen_label(text, units, font_size = self.font_size)
#        self.x_label.place_label()
#    
#    def label_y(self, text, units = None):
#        """
#        Label the y-axis.
#        
#        Parameters
#        ----------
#        text : string
#            Axis label text
#        units : string, optional
#            Axis units.  Units are automatically put in parenthesis.
#        """
#        self.y_label.gen_label(text, units, font_size = self.font_size)
#        self.y_label.place_label()
        
    def _err_data_preprocessor(self, x_err, y_err, colors, line_widths, \
        cap_widths, cap_lengths, C):
        """
        Formats error data arrays and error styles
        """
        #Put the error data in the proper format
        x_err = _utl.convert_err_to_nested_numpy_arrays(x_err)[0]
        y_err = _utl.convert_err_to_nested_numpy_arrays(y_err)[0]
        x_err = _utl.adjust_depth(x_err, 1)
        y_err = _utl.adjust_depth(y_err, 1)
    
        #Populate the error data sets with None if they were not specified
        x_err = x_err + (C - len(x_err)) * [None]
        y_err = y_err + (C - len(y_err)) * [None]
        
        #Ajust to the proper depth and repeat until every curve has a specified
        #style
        colors = _utl.preprocess_input(colors, 2, C)
        line_widths = _utl.preprocess_input(line_widths, 1, C)
        cap_widths = _utl.preprocess_input(cap_widths, 1, C)
        cap_lengths = _utl.preprocess_input(cap_lengths, 1, C)
        
        return(x_err, y_err, colors, line_widths, cap_widths, cap_lengths)
            
    def _marker_preprocessor(self, shapes, sizes, colors, edge_widths, \
        edge_colors, C):
        """
        Format marker styles
        """
        #Ajust to the proper depth and repeat until every curve has a specified
        #style
        shapes = _utl.preprocess_input(shapes, 1, C)
        sizes = _utl.preprocess_input(sizes, 1, C)
        colors = _utl.preprocess_input(colors, 2, C)
        edge_widths = _utl.preprocess_input(edge_widths, 1, C)
        edge_colors = _utl.preprocess_input(edge_colors, 2, C)
        return(shapes, sizes, colors, edge_widths, edge_colors)
    
    def _curve_preprocessor(self, styles, widths, colors, C):
        """
        Format curve styles
        """
        #Ajust to the proper depth and repeat until every curve has a specified
        #style
        styles = _utl.preprocess_input(styles, 1, C)
        widths = _utl.preprocess_input(widths, 1, C)
        colors = _utl.preprocess_input(colors, 2, C)
        return(styles, widths, colors)
        
    def _polygon_preprocessor(self, widths, colors, edge_styles, edge_widths, \
        edge_colors, C):
        """
        Format polygon styles
        """
        #Ajust to the proper depth and repeat until every curve has a specified
        #style
        widths = _utl.preprocess_input(widths, 1, C)
        colors = _utl.preprocess_input(colors, 2, C)
        edge_styles = _utl.preprocess_input(edge_styles, 1, C)
        edge_widths = _utl.preprocess_input(edge_widths, 1, C)
        edge_colors = _utl.preprocess_input(edge_colors, 2, C)
        #For some crazy reason bar plot edge line styles are different than 
        #normal plot line styles, so they need to be converted.
        lstyle_dict = dict({'-'  : 'solid', 
                            '--' : 'dashed', 
                            '-.' : 'dashdot', 
                            ':'  : 'dotted'})
        for i, lstyle in enumerate(edge_styles):
            edge_styles[i] = lstyle_dict[lstyle]
        return(widths, colors, edge_styles, edge_widths, edge_colors)
        
    def _line_at_zero(self, lim, tick, coord1, coord2, trans1, trans2):
        """
        Draws a vertical/horizontal line across zero if axis limits span 
        zero
        """
        #(the sign function says zero is a negative number so we nudge things
        #very slightly to avoid issue)
        if _np.sign(lim[0] + tick / 10.0**10) != _np.sign(lim[1] - tick / 10.0**10):
            #Use a blended transformation so that y data points correspond 
            #to axes/data coordinates, while x data points correspond to data/axes 
            #coordinates.  This way the dashed line will remain in the 
            #right spot even if you pan, zoom, and change axis limits. 
            #(I could use axvline()/axhline() here, but I like to have things 
            #explicit.)
            trans = _mpl.transforms.blended_transform_factory(trans1, trans2)
            l = _mpl_Line2D(coord1, coord2, \
                linestyle = '--', linewidth = 1, color = [0,0,0], \
                transform = trans, zorder = 1)
            #Add the line to the axes container 
            self.mpl_ax.lines.append(l)
        
    def add_title(self, text):
        """
        Adds a title above axes.  I plan to enhance this later...
        """
        self.mpl_ax.set_title(text)

    def add_legend(self, labels = None, curves = 'auto', loc = 'best', \
        outside_ax = False, **kwargs):
        """
        Adds a legend to label curves plotted with ax.plot()
        
        Parameters
        ----------
        labels : list of strings, optional
            Label strings
        curves : list of curve objects, optional
            Curves that will be labeled
        loc : string, optional
            Location of legend.  Valid options include, 'best', 'upper left',
            'upper center, 'upper right', 'center left', 'center', 
            'center right', 'lower left', 'lower center', 'lower right'.
        outside_ax : bool, optional
            Specifies whether to place the legend outside the axes.
                
        Returns
        -------
        legend : legend object
        """
        if curves is 'auto':
            #Collect the curve attributes and labels into a series of rows
            c_data = []
            for curve, label in zip(self.curves, labels):
                color = curve.get_color()
                c_data.append([label, color[0], color[1], color[2], \
                    curve.get_linestyle(), curve.get_linewidth(), \
                    ])
                if curve.get_marker() is not None:
                    #We only care that two curves have different marker colors if
                    #the curves have markers.
                    e_color = curve.get_markeredgecolor()
                    f_color = curve.get_markerfacecolor()
                    c_data[-1].extend([curve.get_marker(), \
                        curve.get_markersize(), curve.get_markeredgewidth(), \
                        e_color[0], e_color[1], e_color[2], \
                        f_color[0], f_color[1], f_color[2]])
                else:
                    #Otherwise assign the same marker properties to all curves 
                    #without markers
                    c_data[-1].extend(['None', \
                        0.0, 0.0, \
                        0, 0, 0, \
                        0, 0, 0])
            #Isolate the unique curve and label combinations, so that we
            #don't get duplicate labels in the legend
            [u_c_data, u_ndx] = _utl.get_unique_rows(c_data)
            curves = _np.array(self.curves)[u_ndx]
            labels = _np.array(labels)[u_ndx]
        #Create the legend
        legend = self._add_legend(curves, labels, loc, outside_ax, **kwargs)
        return(legend)
    
    def add_marker_legend(self, labels = None, markers = 'auto', loc = 'best', \
        outside_ax = False, **kwargs):
        """
        Adds a legend to label markers plotted with ax.plot_markers()
                
        Parameters
        ----------
        labels : list of strings, optional
            Label strings
        markers : list of marker objects, optional
            Markers that will be labeled
        loc : string, optional
            Location of legend.  Valid options include, 'best', 'upper left',
            'upper center, 'upper right', 'center left', 'center', 
            'center right', 'lower left', 'lower center', 'lower right'.
        outside_ax : bool, optional
            Specifies whether to place the legend outside the axes.
                
        Returns
        -------
        legend : legend object
        """
        if markers is 'auto':
            #Collect the marker attributes and labels into a series of rows
            m_data = []
            for marker, label in zip(self.markers, labels):
                e_color = marker.get_markeredgecolor()
                f_color = marker.get_markerfacecolor()
                m_data.append([label, marker.get_marker(), e_color[0], e_color[1], e_color[2], \
                    f_color[0], f_color[1], f_color[2], marker.get_markeredgewidth(), \
                    marker.get_markersize()])
            #Isolate the unique marker and label combinations, so that we
            #don't get duplicate labels in the legend
            [u_m_data, u_ndx] = _utl.get_unique_rows(m_data)
            markers = _np.array(self.markers)[u_ndx]
            labels = _np.array(labels)[u_ndx]
        #Create the legend
        legend = self._add_legend(markers, labels, loc, outside_ax, **kwargs)
        return(legend)
            
    def add_bar_legend(self, labels = None, bars = 'auto', loc = 'best', \
        outside_ax = False, **kwargs):
        """
        Adds a legend to label markers plotted with ax.plot_bars()
                
        Parameters
        ----------
        labels : list of strings, optional
            Label strings
        bars : list of bar objects, optional
            Bars that will be labeled
        loc : string, optional
            Location of legend.  Valid options include, 'best', 'upper left',
            'upper center, 'upper right', 'center left', 'center', 
            'center right', 'lower left', 'lower center', 'lower right'.
        outside_ax : bool, optional
            Specifies whether to place the legend outside the axes.
            
        Returns
        -------
        legend : legend object
        """
        if bars is 'auto':
            bars = self.bars
        legend = self._add_legend(bars, labels, loc, outside_ax, **kwargs)
        return(legend)
            
    def _add_legend(self, data_obj, labels, loc, outside_ax, **kwargs):
        """
        Places a legend on the axes
        """
        #Get rid of escape characters (ex: \n) and make into a latex string.
        #Flatten the list since plt.legend can only handle 1-D lists
        #(The reason I have legend[:] instead of legend is python passes lists by 
        #reference.  The [:] causes python to pass a copy.  This way you can 
        #reuse the labels list for a future plot without stripping the 
        #$ delimiters.)
        raw_labels = _utl.flatten(labels[:])
        for i, el in enumerate(raw_labels):
            if el[0] is not '$':
                raw_labels[i] = '$' + _utl.raw_string(el) + '$'
        if outside_ax:
            if loc.lower() == 'best':
                #If legend is to be placed outside of data axes, select a new
                #default location
                loc = 'upper center'
            #Matplotlib's behavior for placing legends outside of the data axes
            #is a bit confusing.  When you do not specify the 'bbox_to_anchor'
            #keyword, then the 'loc' keyword specifies where to place the 
            #legend.  When you do specify the 'bbox_to_anchor' keyword, then 
            #the 'loc' keyword specifies what part of the legend box that the
            #'bbox_to_anchor' coordinates pertain to.  The dictionary below 
            #translates between these two behaviors so the user doesn't have to
            #worry about it.
            loc_dict = {'upper right' : ['upper left', 1 , 1],
                        'upper_right' : ['upper left', 1 , 1],
                        'right' : ['center left', 1, 0.5],
                        'center right' : ['center left', 1, 0.5],
                        'center_right' : ['center left', 1, 0.5],
                        'lower right' : ['lower left', 1, 0],
                        'lower_right' : ['lower left', 1, 0],
                        'upper center' : ['lower center', 0.5, 1],
                        'upper_center' : ['lower center', 0.5, 1]}
            try:
                ax_coord = loc_dict[loc][1:]                
                loc = loc_dict[loc][0]                
            except KeyError:
                _warnings.warn("Warning: The legend_pos keyword argument was not recognized.  Defaulting to 'upper center' instead.")
                ax_coord = loc_dict['upper center'][1:]
                loc = loc_dict['upper center'][0]                
        else:
            ax_coord = None
        #The legend command normally works without explicitly specifying which 
        #curves to label, but the dashed lines that mark zero cause it to get
        #confused, so I found I had to explicitly specify the curves to label.
        legend = self.mpl_ax.legend(data_obj, raw_labels, loc = loc, \
            bbox_to_anchor = ax_coord, **kwargs)
        #We must add the artist to the axes, so that the next call to legend()
        #creates a new legend instead of overwriting the old one.
        self.mpl_ax.add_artist(legend)
        #The legend has some sort of clipping box that causes the 
        #fig.tight_bbox() code to ignore the legend.  fig.tight_bbox() is used
        #to appropriately size the figure window before saving, so this 
        #resulted in clipped legends.  The solution is to simply turn off the
        #clipping box.
        legend.set_clip_on(False)
        return(legend)

    def add_arrowhead(self, x, cs, orient, length = 7.0, aspect_ratio = 2.5, \
        color = [0,0,0]):
        """
        Creates an arrowhead with a curved back. The arrow can be placed
        relative to several coordinate systems, yet it retains it's shape, even 
        when the data limits, axes, or figure window change size.
        
        Parameters
        ----------
        x : 1x2 numpy array
            Tip of arrowhead, in the coordinate system(s) specified in 
            `x_coord_sys`
        cs : string or 1x2 list
            Specifies the coordinate system for the coordinates in `x`.  See
            description of `cs_1` in the axes.annotate method for further 
            information.
        orient :  float
            Orientation angle (rad) of arrowhead
        length : float, optional
            Length of the arrowhead, in mm
        aspect_ratio : float, optional
            Length/width ratio of the arrowhead
        color : 1x3 list, optional
            RGB value for the arrowhead
        
        Returns
        -------
        arrowhead : annotation object
        """
        arrowhead = self._add_arrow('-)>', x, cs, orient, 0, \
            length, aspect_ratio, color)
        return(arrowhead)

    def _add_arrow(self, style_str, x, cs, orient, length, \
        head_length, head_aspect_ratio, color):
        """
        Add an arrow to the axes
        """
        #Convert the head length from mm into points (1/72")
        head_length_pts = head_length * 72.0/25.4
        #Calculate the head width
        head_width_pts = head_length_pts / head_aspect_ratio
        #Matplotlib annotations take two points as inputs, not one point and
        #an orientation, so we must create a second point
        x_offset = _np.array([-head_length * _np.cos(orient), \
                              -head_length * _np.sin(orient)])
        #(We use an annotation instead of a low level patch, because
        #annotations can retain their shape even when the figure or axes are
        #resized)
        arrowstyle_str = style_str + ', head_width = ' + str(head_width_pts) + \
            ', head_length = ' + str(head_length_pts) + ', length = ' + str(length * 72/25.4)
        #Generate arrow
        arrow = self.annotate('', x_offset, 'offset mm', x_2 = x, cs_2 = cs, \
            arrowprops = dict(arrowstyle = arrowstyle_str, mutation_scale = 1.0, \
            linewidth = 0, facecolor = color, connectionstyle = 'arc3', \
            shrinkA = 0, shrinkB = 0))
        return(arrow)  
                
    def add_arrowheads_to_curves(self, **kwargs):
        """
        Adds arrowheads to curves showing the direction of the curves
        
        Parameters
        ----------
        ndx : list of lists or numpy array, optional
            Specifies the index along the curve to place the tip of the 
            arrowhead.  If there are M curves and you want N arrowheads on each 
            curves, input a MxN array of indices.
        length : float, optional
            Arrowhead length from tip to tail
        color : 1x3 list, optional
            Arrowhead RGB color
        pick : bool, optional
            Specifies whether or not to manually pick the arrow positions
        """
        ndx = kwargs.pop('ndx', [None])
        length = kwargs.pop('length', 5.6)
        color = kwargs.pop('color', [0,0,0])
        pick = kwargs.pop('pick', False)  
        
        if pick is not False:
            ndx = 'pick'      
        
        def _find_arrowhead_end(self, xi, yi, ndx1, step, target_length):
            """Given a index along the curve, and a target arrowhead length, 
            the algorithm finds the end of the arrowhead"""
            #Specify annotation position by converting data axes
            #coordinates to figure axes coordinates (different conversion
            #depending on the axis scaling)
            pos1 = _np.array([[xi[ndx1]], [yi[ndx1]]])
            pos1_mm = self.mpl_ax.transData.transform(pos1.T).T / _cp.params.dpmm
            #Find the location of the end of the arrowhead by moving along the curve 
            #in small increments until the distance between the first index and the 
            #second index is greater than the target arrowhead length
            length_mm=0
            ndx2 = ndx1
            #The arrow length pertains to the tip to the tail.  The length 
            #of the arrow along a straight line is the tip to back length,
            #For John Shaw arrowheads, the tip to back length is 80% of the 
            #total arrow length.
            while length_mm < target_length:
                ndx2 = ndx2 + step
                pos2 = _np.array([[xi[ndx2]], [yi[ndx2]]])
                pos2_mm = self.mpl_ax.transData.transform(pos2.T).T / _cp.params.dpmm
                delta_mm = pos1_mm - pos2_mm
                length_mm = _np.linalg.norm(delta_mm)
            return(ndx2, pos1, delta_mm)        
        
        if pick is not False:
            #If the user is specifying the arrow positions, create the index list 
            #filled with with default values.  This list will be populated later 
            #when the arrow locations are specified
            ndx = []
            for curve in self.curves:
                ndx.append([None])     
            ndx_pick = True
            if pick.lower() not in ['tip', 'center', 'middle']:
                raise ValueError("""The input for 'arrow_pick' was not recognized""")
            #Inform the user what to do
            print 'Select the ' + pick.lower() + 'of the arrowhead location(s) for each curve of each axis.'
            print 'Left click all the locations for a single curve, then press enter (or right click) to proceed to the next curve/axis.'
            print 'Alternatively, press enter, without left clicking any locations, to skip to the next curve.'
        else:
            #If the arrow indices have been specified, make sure the list has the 
            #proper depth
            ndx_pick = False
            ndx = _utl.adjust_depth(ndx, 2)
        
        for c, curve in enumerate(self.curves):
            xi = curve.full_x_data
            yi = curve.full_y_data
            if ndx_pick:
                print 'Curve # %r' %(c + 1)
                #Get user specified location for text, in the data coordinate
                #system
                c_ndx = []
                apick = _plt.ginput(100, mouse_add = 1, mouse_pop = 2, \
                    mouse_stop = 3)
                for pt in apick:
                    #Find the delta between the current curve and the manually 
                    #selected point close to the curve
                    delta = _np.array([[pt[0] - xi], [pt[1] - yi]])
                    #Find the distance between every point on the current curve
                    #and the manually selected point
                    dist = ((delta[0,:]**2.0 + delta[1,:]**2.0)**0.5)[0]                    
                    #Save the index for arrowhead tip location.  In case
                    #there are multiple points that are closest, just 
                    #use the first one.
                    c_ndx.append(_np.where(dist == _np.nanmin(dist))[0][0])
                if pick.lower() in ['center', 'middle']:
                    #If the user picked the center of the arrowhead, we must 
                    #find the tip of the arrowhead
                    for i, ndx1 in enumerate(c_ndx):
                        c_ndx[i] = _find_arrowhead_end(self, xi, yi, ndx1, 1, \
                            0.5 * length)[0]
                #Save arrow positions
                ndx[c] = c_ndx
            for ndx1 in ndx[c]:
                [ndx_back, pos_tip, arrow_delta_mm] = _find_arrowhead_end(\
                    self, xi, yi, ndx1, -1,  0.8 * length)
                #Use the delta across the arrowhead to find the angle
                orient = _np.arctan2(arrow_delta_mm[1,0], arrow_delta_mm[0,0])
#                #Take the arrowhead position from data coordinates to 
#                #normalized figure coordinates
#                #(One must first convert to display coordinates and then conert 
#                #to normalized figure coordinates.  There does no appear to be 
#                #a direct way to convert from data to normalized figure 
#                #coordinates.)
#                pos_tip_pix = self.mpl_ax.transData.transform(pos_tip.T).T
#                pos_tip_fig = self.parent_fig.mpl_fig.transFigure.inverted().transform(pos_tip_pix.T).T
                #Print the arrowhead
                arrowhead = self.add_arrowhead(pos_tip, 'data', orient, \
                    length = length, color = color)
                self.mpl_ax.draw_artist(arrowhead)
            self.parent_fig.update()
        if ndx_pick:
            print """Here are the arrow indices so that you can input them directly next time."""
            print """arrow_ndx = """
            print ndx
            
    def label_curves(self, labels, **kwargs):
        """
        Labels curves, either at interactively picked points or at user 
        specified locations.
        
        Parameters
        ----------
        labels : string or list of strings
            Label strings (in LaTeX format)
        ndx : integer or list of integers, optional
            list of indices that specify the location of the leader line root
        angles : float or list of floats, optional
            list of leader line angles or a single angle (in degrees)
        lengths : float or list of floats, optional
            list of leader line lengths or a single length (in points) 
        pick : 'root', 'text', or False, optional
            Input 'root' or 'text' to interactively chose the label positions.  
            If 'root' is specified, the user selects the leader line root 
            position with the cursor, and specified or default values are used 
            for the leader line length and angle.  If 'text' is specified, the 
            user selects the position of the text and the leader line is 
            extended until it intersects the curve at the specified or default 
            angle.
        style : 'normal' or 'balloon', optional, default: 'normal'
            Input 'normal' to create labels without circles around them.  The 
            default is 'balloon' labels, with circles around them.
        font_size : float, optional
            font size (in points) for label text
        
        Returns
        -------
        If labels have been interactively picked, prints `ndx`, `angles`, and
        `lengths` so the user can input them directly next time.
            
        See Also
        --------
        Axes.label_curve : Place multiple labels on a single curve
        """
        ndx = kwargs.pop('ndx', ['auto'])
        angles = kwargs.pop('angles', ['auto'])
        lengths = kwargs.pop('lengths', [12])
        pick = kwargs.pop('pick', False)
        style = kwargs.pop('style', 'normal')
        font_size = kwargs.pop('font_size', 14)
        self._add_labels(labels, ndx, angles, lengths, style, pick, font_size, \
            True, self.curves)
        
    def label_curve(self, **kwargs):
        """
        Prints one or more labels on a single curve, either at interactively 
        picked points or at user specified locations.
        
        Parameters
        ----------
        x : 1D numpy array, optional
            x coordinates of the data to be labeled
        y : 1D numpy array, optional
            y coordinates of the data to be labeled
        curve : curve object, optional
            Curve to label.  Either `curve` or both `x` and `y` must be 
            specified
            
        See Axes.label_curves for descriptions of other input parameters
        
        Returns
        -------
        If labels have been interactively picked, prints `ndx`, `angles`, and
        `lengths` so the user can input them directly next time.
        
        See Also
        --------
        Axes.label_curves : Place a label on each curve
        """
        x = kwargs.pop('x', None)
        y = kwargs.pop('y', None)
        curve = kwargs.pop('curve', None)
        labels = kwargs.pop('labels', 'auto')
        ndx = kwargs.pop('ndx', 'auto')
        angles = kwargs.pop('angles', 'auto')
        lengths = kwargs.pop('lengths', [12])
        pick = kwargs.pop('pick', False)
        style = kwargs.pop('style', 'balloon')
        font_size = kwargs.pop('font_size', 14)
        if curve is None:
            if x is None or y is None:
                raise IOError("""ERROR: either a curve object or both x and y 
                    data must be supplied""")
            flag = False            
            for i, curve in enumerate(self.curves):
                if _np.max(_np.abs(x.flatten() - curve.full_x_data)) < 1e-12:
                    if _np.max(_np.abs(y.flatten() - curve.full_y_data)) < 1e-12:
                        flag = True
                        continue
            if not flag:
                raise IOError("ERROR: x and y data do not correspond to an existing curve")
        
        self._add_labels(labels, ndx, angles, lengths, style, pick, font_size, \
            False, [self.curves[i]])
    
    def _add_labels(self, labels, ndx, angles, lengths, style, pick, font_size, \
        labeling_curves, curves):
        """Places mutliple labels on a single curve or one label on each curve
        """
        
        #Preprocess the label text
        if labels is 'auto':
            if ndx is 'auto':
                raise IOError("""Text and ndx cannot both be 'auto'""")
            else:
                labels = range(1, len(ndx) + 1)
                labels = map(lambda x: str(x), labels)
        
        #Preprocess lists
        labels = _utl.adjust_depth(labels, 1)
        ndx = _utl.adjust_depth(ndx, 1)
        angles = _utl.adjust_depth(angles, 1)
        lengths = _utl.adjust_depth(lengths, 1)
        
        #Preprocess the pick options
        if pick is not False:
            if pick.lower() == 'root':
                ndx = ['auto']
                if angles == ['auto']:
                    angles = [120]
                print """Click on the plot to select the leader line root location for each curve of each axis."""
            elif pick.lower() == 'text':
                ndx = ['auto']
                lengths = ['auto']
                print """Click on the plot to select the label text location for each curve of each axis."""
            else:
                raise IOError("""The input for 'pick' was not recognized""")
        else:
            if angles == ['auto']:
                angles = [120]

        #Specify a list of candidate angles.  If auto selecting angle, then 
        #the algorithm below will chose the angle that gives the shortest 
        #leader line.  Using candidate angles instead of freely varying 
        #angles causes the leader lines to look more orderly
        angle_cand = _np.array([30, 60, 120, 150, -150, -120, -60, -30])
        
        if (style is 'balloon') or (style is 'balloons'):
            #As of matplotlib 1.5.0, you can specify the padding.  Earlier 
            #versions cannot.
            if _cp.mpl_version < (1,5,0):
                l_bbox = dict(boxstyle='circle', fc = [1,1,1]) 
            else:   
                l_bbox = dict(boxstyle='circle', fc = [1,1,1], pad = 0.2) 
        else:
            l_bbox = None    
        
        #Extend the label lists so that they are all the same length
        def extend_list(l, N):
            l = l + [l[0]] * (N - len(l))
            return(l)    
        N = len(labels)
        ndx = extend_list(ndx, N)
        angles = extend_list(angles, N)
        lengths = extend_list(lengths, N)

        for n, t in enumerate(labels):
            #Convert the label text to raw LaTeX format
            labels[n] = '$' + _utl.raw_string(t) + '$'
    
        if labeling_curves:       
            c = -1
        else:
            c = 0
        i = 0
        for n, t in enumerate(labels):
            #Specify the text that will be printed to the console if labels are 
            #manually picked
            if labeling_curves:
                c = c + 1
                console_text = 'Curve # %r' %(c + 1)
            else:
                console_text = 'Label # %r' %(n + 1)
            xi = curves[c].full_x_data
            yi = curves[c].full_y_data
            if pick is not False:
                print console_text
                #Get user specified location for text, in the data coordinate
                #system
                lpick = _plt.ginput(1)[0]
                if pick.lower() == 'root':
                    #Find the delta between the current curve and the manually 
                    #selected point close to the curve
                    delta = _np.array([lpick[0] - xi, lpick[1] - yi])
                    #Find the distance between every point on the current curve
                    #and the manually selected point
                    dist = (delta[0,:]**2.0 + delta[1,:]**2.0)**0.5
                    #Save the index for leader line location.  In case
                    #there are multiple points that are closest, just 
                    #use the first one.
                    ndx[n] = _np.where(dist == _np.nanmin(dist))[0][0]
                if pick.lower() == 'text':
                    #Convert picked location and current curve into mm
                    lpick_mm = self.mpl_ax.transData.transform(lpick) / _cp.params.dpmm
                    xy_mm = self.mpl_ax.transData.transform(_np.vstack([xi,yi]).T).T / _cp.params.dpmm
                    #Find the delta between the current curve and the manually 
                    #selected point close to the curve
                    delta_mm = _np.array([lpick_mm[0] - xy_mm[0,:], lpick_mm[1] - xy_mm[1,:]])
                    #Find the angle of the label text to each of the data 
                    #points along the curve, in the data coordinate system
                    beta = _np.arctan2(delta_mm[1,:], delta_mm[0,:]) * 180.0/_np.pi
                    if angles[n] == 'auto':
                        #Find the leader line length for each of the candidate 
                        #angles
                        cand_ndx = _np.zeros(angle_cand.shape)
                        cand_l = _np.zeros(angle_cand.shape)
                        for k, ac in enumerate(angle_cand):
                            cand_ndx[k] = _np.where(_np.nanmin(_np.abs(beta - ac)) \
                                == _np.abs(beta - ac))[0][0]
                            cand_l[k] = (delta_mm[0, cand_ndx[k]]**2.0 + \
                                delta_mm[1, cand_ndx[k]]**2.0)**0.5
                        #Select the candidate angle that produces the shortest 
                        #leader line
                        m = _np.where(_np.min(cand_l) == cand_l)[0][0]
                        angles[n] = angle_cand[m]
                        ndx[n] = int(cand_ndx[m])
                        lengths[n] = _np.round(cand_l[m], decimals = 2)
                    else:
                        #Find the index of the angle that most closely 
                        #matches the specified angle and use that for the 
                        #leader line root
                        ndx = _np.where(_np.nanmin(_np.abs(beta - angles[n])) \
                            == _np.abs(beta - angles[n]))[0][0]
                        ndx[n] = int(ndx)
                        #Compute the distance between the root and the text
                        lengths[n] = \
                            (delta_mm[0, ndx]**2.0 + delta_mm[1, ndx]**2.0)**0.5
                        lengths[n] = _np.round(lengths[n], decimals = 2)
            else:
                if ndx[n] is 'auto':
                    ndx[n] = _np.round(len(yi) / 2.0)
            #Convert input angle from degrees to radians
            a = angles[n] * _np.pi/180.0
            #Only bother doing the following steps if a label position 
            #was selected and label text was specified
            if not any(map(lambda x: x is None, [labels[n], ndx[n]])):
                #Convert from polar coordinates to rectangular coordinates
                offset_pos = lengths[n] * _np.array([_np.cos(a), _np.sin(a)])
                #Create the annotation
                root = [xi[ndx[n]], yi[ndx[n]]]
                l_obj = self.annotate(labels[n], offset_pos, 'offset mm', \
                    x_2 = root, cs_2 = 'data', \
                    size = font_size, va = 'center', ha = 'center', \
                    fontname = 'sans-serif', bbox = l_bbox, \
                    arrowprops=dict(arrowstyle='-', \
                    connectionstyle='arc3, rad=0.0', fc='none', \
                    shrinkA = 0.0, shrinkB = 0.0))
                self.mpl_ax.draw_artist(l_obj)
                if style is 'balloon':
                    #Place the white background of the balloon behind the 
                    #label text
                    patch = l_obj.get_bbox_patch()
                    patch.set_zorder(2)
                #Increment the marker style index by one
                i = i + 1
            #Update the canvas so that the labels appear
            self.parent_fig.update()
        
        #After the last label has been placed, inform the user of the
        #following:
        if pick is not False:
            print """Here is the label information so that you can input it 
            directly next time."""
            print """ndx = """
            print ndx
            print """angles = """
            print angles
            print """lengths = """
            print lengths
            #TODO: Print label info in a more user friendly way.  Round numbers,
            #get rid of the latex formatting.
            
    def add_image(self, im, **kwargs):
        """
        Adds an image to the axes
        
        Parameters
        ----------
        See clearplot.axes._Data_Axes_Base.add_image()
        """
        #Use the add image on the parent of the Axes class
        im_obj = super(Axes, self).add_image(im, **kwargs)        
        #Set the limits and ticks
        self._select_and_set_x_lim_and_tick(self._ui_x_lim, self._ui_x_tick)
        self._select_and_set_y_lim_and_tick(self._ui_y_lim, self._ui_y_tick)
        return(im_obj)
            
    def plot(self, x, y, **kwargs):
        """
        Plots x and y data as 2D curves on the axes
        
        Parameters
        ----------
        x : 1xN list of numpy arrays
            x-coordinates of curves
        y : 1xN list of numpy arrays
            y-coordinates of curves
        curve_colors : list of 1x3 lists, optional
            Colors of curves.  RGB values should be between 0 and 1.
        curve_styles : list of strings, optional
            Styles of curves.  Valid styles include '-', '--', '-.', ':'.
        curve_widths : list of floats or ints, optional
            Width of curves in points.
        marker_shapes : list of strings, optional
            Shapes of markers.  See the `matplotlib documentation 
            <http://matplotlib.org/api/markers_api.html>`__ for valid shapes.
        marker_sizes : list of floats or ints, optional
            Sizes of markers, in points.
        marker_colors : list of 1x3 lists, optional
            Colors of marker faces.  RGB values should be between 0 and 1.
        marker_edge_widths : list of floats or ints, optional
            Width of marker edges in points.
        marker_edge_colors: list of 1x3 lists, optional
            Colors of marker edges.  RGB values should be between 0 and 1.
            
        See Also
        --------
        Axes.plot_markers : similar to Axes.plot, except it plots markers that
            can be added to the marker legend
        """
        curve_colors = kwargs.pop('curve_colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['std'], self.color_ndx))
        curve_styles = kwargs.pop('curve_styles', ['-'])
        curve_widths = kwargs.pop('curve_widths', [2]) 
        marker_shapes = kwargs.pop('marker_shapes', [None])
        marker_sizes = kwargs.pop('marker_sizes', [6])
        marker_colors = kwargs.pop('marker_colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['std'], self.color_ndx))
        marker_edge_widths = kwargs.pop('marker_edge_widths', [1.0])
        marker_edge_colors = kwargs.pop('marker_edge_colors', [[0,0,0]])
        
        #Preprocess inputs
        [x, y] = self._data_preprocessor(x, y, True, 1)
        C = len(x)
        [curve_styles, curve_widths, curve_colors] = self._curve_preprocessor( \
            curve_styles, curve_widths, curve_colors, C)
        [marker_shapes, marker_sizes, marker_colors, marker_edge_widths, \
            marker_edge_colors ] = self._marker_preprocessor(marker_shapes, \
            marker_sizes, marker_colors, marker_edge_widths, \
            marker_edge_colors, C)
        
        #Cycle thru the pairs of data in x and y
        #(I tried to do the plot command all at once, but multiple curves must 
        #be input as plot(x1, y1, '-', x2, y2, '--'), which isn't easy to 
        #extend to an arbitrary number of curves.)
        #Set the color/style/marker iterator to zero
        i = 0
        for xi, yi in zip(x, y):
            #Plot data
            #(See the axes clipping methods for why clip_on = False.)
            self.curves.extend(self.mpl_ax.plot(xi, yi, \
                linestyle = curve_styles[i], \
                linewidth = curve_widths[i], \
                color = curve_colors[i], \
                marker = marker_shapes[i], \
                markersize = marker_sizes[i], \
                markerfacecolor = marker_colors[i], \
                markeredgewidth = marker_edge_widths[i], \
                markeredgecolor = marker_edge_colors[i], \
                clip_on = False, scalex = False, scaley = False, zorder = 3))
            i = i + 1
        #Update the auto color index, in case further curves are plotted on 
        #this set of axes
        self.color_ndx = self.color_ndx + i
            
        #Set the limits and ticks
        self._select_and_set_x_lim_and_tick(self._ui_x_lim, self._ui_x_tick)
        self._select_and_set_y_lim_and_tick(self._ui_y_lim, self._ui_y_tick)

    def plot_markers(self, x, y, **kwargs):
        """
        Plots x and y data as markers on the axes
        
        Parameters
        ----------
        x : 1xN list of numpy arrays
            x-coordinates of markers
        y : 1xN list of numpy arrays
            y-coordinates of markers
        shapes : list of strings, optional
            Shapes of markers.  See the `matplotlib documentation 
            <http://matplotlib.org/api/markers_api.html>`__ for valid shapes.
        sizes : list of floats or ints, optional
            Sizes of markers, in points.
        colors : list of 1x3 lists, optional
            Colors of marker faces.  RGB values should be between 0 and 1.
        edge_widths : list of floats or ints, optional
            Width of marker edges in points.
        edge_colors: list of 1x3 lists, optional
            Colors of marker edges.  RGB values should be between 0 and 1.
            
        See Also
        --------
        Axes.plot : Similar to Axes.plot_markers, except it plots curves that
            can be added to the curve legend
        Axes.plot_error_bars : Plots error bars at each data point
        """
        shapes = kwargs.pop('shapes', ['o'])
        sizes = kwargs.pop('sizes', [6])
        colors = kwargs.pop('colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['std'], self.marker_color_ndx))
        edge_widths = kwargs.pop('edge_widths', [0.0])
        edge_colors = kwargs.pop('edge_colors', [[0,0,0]])   
          
        [x, y] = self._data_preprocessor(x, y, True, 1)
        C = len(x)
        [shapes, sizes, colors, edge_widths, edge_colors ] = \
            self._marker_preprocessor(shapes, sizes, colors, edge_widths, \
                edge_colors, C)
        
        #Cycle thru the pairs of data in x and y
        #(I tried to do the plot command all at once, but multiple curves must 
        #be input as plot(x1, y1, '-', x2, y2, '--'), which isn't easy to 
        #extend to an arbitrary number of curves.)
        #Set the color/style/marker iterator to zero
        i = 0
        for xi, yi in zip(x, y):
            #Plot data
            #(See the axes clipping methods for why clip_on = False.)
            self.markers.extend(self.mpl_ax.plot(xi, yi, \
                linestyle = 'none', \
                marker = shapes[i], \
                markersize = sizes[i], \
                markerfacecolor = colors[i], \
                markeredgewidth = edge_widths[i], \
                markeredgecolor = edge_colors[i], \
                clip_on = False, scalex = False, scaley = False, zorder = 3))
            i = i + 1
        self.marker_color_ndx = self.marker_color_ndx + i
            
        #Set the limits and ticks
        self._select_and_set_x_lim_and_tick(self._ui_x_lim, self._ui_x_tick)
        self._select_and_set_y_lim_and_tick(self._ui_y_lim, self._ui_y_tick)
    
    def plot_error_bars(self, x, y, **kwargs):
        """
        Plots error bars at each x--y data point
        
        Parameters
        ----------
        x : 1xN list of numpy arrays
            x-coordinates of error bar centers
        y : 1xN list of numpy arrays
            y-coordinates of error bar centers
        x_err : 1xN list of numpy arrays or None objects, optional
            x error deltas.  Supply 1xM numpy array(s) to draw symmetric error 
            bars or 2xM numpy array(s) to draw assymetric error bars.  Supply
            None object(s) to skip drawing x error bars for a given data set.
        y_err : 1xN list of numpy arrays or None objects, optional
            y error deltas.  Supply 1xM numpy array(s) to draw symmetric error 
            bars or 2xM numpy array(s) to draw assymetric error bars.  Supply
            None object(s) to skip drawing x error bars for a given data set.
        colors : list of 1x3 lists, optional
            Colors of error bars.  RGB values should be between 0 and 1.
        bar_line_widths : list of floats or ints, optional
            Width of error bar lines in points.
        cap_line_widths : list of floats or ints, optional
            Width of error bar cap line widths in points.
        cap_lengths: list of floats or ints, optional
            Length of error bar cap in points.
            
        See Also
        --------
        Axes.plot : similar to Axes.plot_markers, except it plots curves that
            can be added to the curve legend
        Axes.plot_error_bars : plots error bars
        """
        x_err = kwargs.pop('x_err', [None])
        y_err = kwargs.pop('y_err', [None])
        colors = kwargs.pop('colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['dark'], self.err_color_ndx))
        bar_line_widths = kwargs.pop('bar_line_widths', [1.0])
        cap_line_widths = kwargs.pop('cap_line_widths', [2.0])
        cap_lengths = kwargs.pop('cap_lengths', [4.0])
        
        #Preprocess inputs
        C = len(x)
        [x_err, y_err, colors, bar_line_widths, cap_line_widths, \
            cap_lengths] = self._err_data_preprocessor(x_err, y_err, \
            colors, bar_line_widths, cap_line_widths, cap_lengths, C)
            
        #Cycle thru the pairs of data in x and y
        #(I tried to do the plot command all at once, but multiple curves must 
        #be input as plot(x1, y1, '-', x2, y2, '--'), which isn't easy to 
        #extend to an arbitrary number of curves.)
        #Set the color/style/marker iterator to zero
        i = 0
        for xi, yi, xei, yei in zip(x, y, x_err, y_err):
            #Plot data
            self.mpl_ax.errorbar(xi, yi, xerr = xei, yerr = yei, \
                ecolor = colors[i], \
                elinewidth = bar_line_widths[i], \
                capthick = cap_line_widths[i], \
                capsize = cap_lengths[i], \
                linestyle = 'none', zorder = 3)
            i = i + 1
        #Update the auto color index, in case further curves are plotted on 
        #this set of axes
        self.err_color_ndx = self.err_color_ndx + i
        
    def plot_bars(self, x, y, **kwargs):
        """
        Plots x--y data as vertical bars on the axes
        
        Parameters
        ----------
        x : 1xN list of numpy arrays
            x coordinates of bars
        y : 1xN list of numpy arrays
            Height of bars
        widths : list of floats or ints, optional
            Width of bars in x-coordinate units
        colors : list of 1x3 lists, optional
            Colors of bars.  RGB values should be between 0 and 1.
        edge_styles : list of strings, optional
            Styles of bar edges.  Valid options include '-', '--', '-.', ':', 
            or 'None'
        edge_widths : list of floats, optional
            Width of bar edges (in points).  
        edge_colors : list of 1x3 lists, optional
            Colors of bar edges.  RGB values should be between 0 and 1.
        align : ['center' | 'edge'], optional
            Specifies which part of the bar to align to the x coordinate
        """
        widths = kwargs.pop('widths', [0.5])
        colors = kwargs.pop('colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['pastel'], self.color_ndx))
        edge_styles = kwargs.pop('edge_styles', ['-'])
        edge_widths = kwargs.pop('edge_widths', [1.5])
        edge_colors = kwargs.pop('edge_colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['darker'], self.color_ndx))
        align = kwargs.pop('align', 'center')
        
        #Preprocess inputs
        [x, y] = self._data_preprocessor(x, y, True, 1)
        C = len(x)
        [widths, colors, edge_styles, edge_widths, edge_colors] = \
            self._polygon_preprocessor(widths, colors, edge_styles, \
            edge_widths, edge_colors, C)
        
        #Cycle thru the pairs of data in x and y
        #Set the color/style/marker iterator to zero
        i = 0
        for xi, yi in zip(x, y):
            #Plot data
            self.bars.append(self.mpl_ax.bar(xi, yi, \
                width = widths[i], \
                color = colors[i], \
                linestyle = edge_styles[i], \
                linewidth = edge_widths[i], \
                edgecolor = edge_colors[i], \
                clip_on = True, align = align, zorder = 2))
            i = i + 1
        #Update the auto color index, in case further curves are plotted on 
        #this set of axes
        self.color_ndx = self.color_ndx + i
            
        #Set the limits and ticks
        self._select_and_set_x_lim_and_tick(self._ui_x_lim, self._ui_x_tick)
        self._select_and_set_y_lim_and_tick(self._ui_y_lim, self._ui_y_tick)
        
    def plot_violins(self, x, y, **kwargs):
        """
        Plot distributions of data in a violin plot on the axes
        
        Parameters
        ----------
        x : 1xN list of numpy arrays
            x coordinates of violins
        y : 1xN list of numpy arrays
            Distributions of data
        body_widths : list of floats, optional
            Horizontal width of violin bodies in x data units
        body_colors : list of 1x3 lists, optional
            Colors of violin bodies.  RGB values should be between 0 and 1.
        body_edge_styles : list of strings, optional
            Styles of violin body edges.  Valid options include '-', 
            '--', '-.', ':', or 'None'
        body_edge_widths : list of floats, optional
            Widths of violin body edges, in points.
        body_edge_colors : list of 1x3 lists of , optional
            Colors of violin body edges.  RGB values should be between 0 and 1.
        show_means : bool, optional
            Show mean of each distribution of data
        show_medians : bool, optional
            Show median of each distribution of data
        show_extrema : bool, optional
            Show extrema of each distribution of data
        line_styles : list of strings, optional
            Styles of mean/median/extrema edges.  Valid options include '-', 
            '--', '-.', ':', or 'None'
        line_widths : list of floats, optional
            Widths of mean/median/extrema edges, in points.
        line_colors : list of 1x3 lists, optional
            Colors of mean/median/extrema edges.  RGB values should be between 
            0 and 1.
            
        See Also
        --------
        Axes.plot_box_and_whiskers()
        """
        
        body_widths = kwargs.pop('body_widths', [0.75])
        body_colors = kwargs.pop('body_colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['pastel'], self.color_ndx))
        body_edge_styles = kwargs.pop('body_edge_styles', ['-'])
        body_edge_widths = kwargs.pop('body_edge_widths', [1.5])
        body_edge_colors = kwargs.pop('body_edge_colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['dark'], self.color_ndx))
        show_means = kwargs.pop('show_means', True)
        show_medians = kwargs.pop('show_medians', False)
        show_extrema = kwargs.pop('show_extrema', True)
        line_styles = kwargs.pop('line_styles', ['-'])
        line_widths = kwargs.pop('line_widths', [2])
        line_colors = kwargs.pop('line_colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['dark'], self.color_ndx))
        
        #Preprocess inputs
        [x, y] = self._data_preprocessor(x, y, False, 1)
        C = len(x)
        [body_widths, body_colors, body_edge_styles, body_edge_widths, \
            bar_edge_colors] = self._polygon_preprocessor(body_widths, \
            body_colors, body_edge_styles, body_edge_widths, body_edge_colors, C)
        [line_styles, line_widths, line_colors] = self._curve_preprocessor( \
            line_styles, line_widths, line_colors, C)
        
        #Cycle thru the pairs of data in x and y
        #Set the color/style/marker iterator to zero
        i = 0
        for xi, yi in zip(x, y):
            #Plot data
            self.violins.append(self.mpl_ax.violinplot(yi, positions = xi, \
                widths = body_widths[i], showmeans = show_means, \
                showmedians = show_medians, showextrema = show_extrema))
            #As I mention in https://github.com/matplotlib/matplotlib/pull/3875
            #I cannot set the alpha value for facecolor and edgecolor 
            #independently.  Hopefully this will get fixed soon.
            _plt.setp(self.violins[i]['bodies'][0], \
                facecolor = body_colors[i], \
                alpha = 1.0, \
                linestyle = body_edge_styles[i], \
                linewidth = body_edge_widths[i], \
                edgecolor = body_edge_colors[i])
            for key in ['cbars', 'cmins', 'cmeans', 'cmedians', 'cmaxes']:
                if self.violins[i].has_key(key):
                    _plt.setp(self.violins[i][key], \
                        linestyle = line_styles[i], \
                        color = line_colors[i], \
                        linewidth = line_widths[i])
            i = i + 1
        #Update the auto color index, in case further curves are plotted on 
        #this set of axes
        self.color_ndx = self.color_ndx + i
            
        #Set the limits and ticks
        self._select_and_set_x_lim_and_tick(self._ui_x_lim, self._ui_x_tick)
        self._select_and_set_y_lim_and_tick(self._ui_y_lim, self._ui_y_tick)
        
    def plot_box_and_whiskers(self, x, y, **kwargs):
        """
        Plot distributions of data in a box and whiskers plot on the axes 
        
        Parameters
        ----------
        x : 1xN list of numpy arrays
            x coordinates of boxes
        y : 1xN list of numpy arrays
            Distributions of data
        box_widths : list of floats, optional
            Horizontal width of boxes in x data units
        box_colors : list of 1x3 lists, optional
            Colors of boxes.  RGB values should be between 0 and 1.
        box_edge_styles : list of strings, optional
            Styles of box edges.  Valid options include '-', '--', '-.', ':', 
            or 'None'
        box_edge_widths : list of floats, optional
            Widths of box edges, in points.
        box_edge_colors : list of 1x3 lists of , optional
            Colors of box edges.  RGB values should be between 0 and 1.
        whisker_styles : list of strings, optional
            Styles of whiskers.  Valid options include '-', '--', '-.', ':', 
            or 'None'
        whisker_widths : list of floats, optional
            Widths of whiskers, in points.
        whisker_colors : list of 1x3 lists, optional
            Colors of whiskers.  RGB values should be between 0 and 1.
        cap_styles : list of strings, optional
            Styles of caps.  Valid options include '-', '--', '-.', ':', 
            or 'None'
        cap_widths : list of floats, optional
            Widths of caps, in points.
        cap_colors : list of 1x3 lists, optional
            Colors of caps.  RGB values should be between 0 and 1.
        flier_shapes : list of strings, optional
            Shapes of fliers.  See the `matplotlib documentation 
            <http://matplotlib.org/api/markers_api.html>`__ for valid shapes.
        flier_sizes : list of floats, optional
            Size of fliers in points.
        flier_colors : list of 1x3 lists, optional
            Colors of flier faces.  RGB values should be between 0 and 1.
        flier_edge_widths : list of floats, optional
            Widths of flier edges, in points.
        flier_edge_colors : list of 1x3 lists, optional
            Colors of flier edges.  RGB values should be between 0 and 1.
            
        See Also
        --------
        Axes.plot_violins()
        """
        
        box_widths = kwargs.pop('box_widths', [0.75])
        box_colors = kwargs.pop('box_colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['pastel'], self.color_ndx))
        box_edge_styles = kwargs.pop('box_edge_styles', ['-'])
        box_edge_widths = kwargs.pop('box_edge_widths', [1.5])
        box_edge_colors = kwargs.pop('box_edge_colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['dark'], self.color_ndx))
        whisker_styles = kwargs.pop('whisker_styles', ['--'])
        whisker_widths = kwargs.pop('whisker_widths', [2])
        whisker_colors = kwargs.pop('whisker_colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['dark'], self.color_ndx))
        cap_styles = kwargs.pop('cap_styles', ['-'])
        cap_widths = kwargs.pop('cap_widths', [2])
        cap_colors = kwargs.pop('cap_colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['dark'], self.color_ndx))
        flier_shapes = kwargs.pop('flier_shapes', ['+'])
        flier_sizes = kwargs.pop('flier_sizes', [6])
        flier_colors = kwargs.pop('flier_colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['dark'], self.color_ndx))
        flier_edge_widths = kwargs.pop('flier_edge_widths', [2])
        flier_edge_colors = kwargs.pop('flier_edge_colors', \
            _utl.cycle_thru_list(_cp.colors.c_lists['dark'], self.color_ndx))
        
        #Preprocess inputs
        [x, y] = self._data_preprocessor(x, y, False, 1)
        C = len(x)
        [box_widths, box_colors, box_edge_styles, box_edge_widths, \
            bar_edge_colors] = self._polygon_preprocessor(box_widths, \
            box_colors, box_edge_styles, box_edge_widths, box_edge_colors, C)
        [whisker_styles, whisker_widths, whisker_colors] = \
            self._curve_preprocessor(whisker_styles, whisker_widths, \
            whisker_colors, C)
        [cap_styles, cap_widths, cap_colors] = self._curve_preprocessor( \
            cap_styles, cap_widths, cap_colors, C)
        [flier_shapes, flier_sizes, flier_colors, flier_edge_widths, \
        flier_edge_colors] = self._marker_preprocessor(flier_shapes, \
        flier_sizes, flier_colors, flier_edge_widths, flier_edge_colors, C)
        
        #Set the axis data types
#        self.x_data_type    
        
        #Cycle thru the pairs of data in x and y
        #Set the color/style/marker iterator to zero
        i = 0
        for xi, yi in zip(x, y):
            #Plot data
            self.boxes.append(self.mpl_ax.boxplot(yi, positions = xi, \
                widths = box_widths[i], notch = True, patch_artist = True))
            for box in self.boxes[i]['boxes']:
                _plt.setp(box, \
                    facecolor = box_colors[i], \
                    linestyle = box_edge_styles[i], \
                    linewidth = box_edge_widths[i], \
                    edgecolor = box_edge_colors[i])
            for key in ['medians', 'means']:
                for el in self.boxes[i][key]:
                    _plt.setp(el, \
                        linestyle = box_edge_styles[i], \
                        color = box_edge_colors[i], \
                        linewidth = box_edge_widths[i])
            for cap in self.boxes[i]['caps']:
                _plt.setp(cap, \
                    linestyle = cap_styles[i], \
                    color = cap_colors[i], \
                    linewidth = cap_widths[i])
            for whisker in self.boxes[i]['whiskers']:
                _plt.setp(whisker, \
                    linestyle = whisker_styles[i], \
                    color = whisker_colors[i], \
                    linewidth = whisker_widths[i])
            for flier in self.boxes[i]['fliers']:
                _plt.setp(flier, \
                    marker = flier_shapes[i], \
                    markersize = flier_sizes[i], \
                    color = flier_colors[i], \
                    markeredgecolor = flier_edge_colors[i], \
                    markeredgewidth = flier_edge_widths[i])
            i = i + 1
        #Update the auto color index, in case further curves are plotted on 
        #this set of axes
        self.color_ndx = self.color_ndx + i
            
        #Set the limits and ticks
        self._select_and_set_x_lim_and_tick(self._ui_x_lim, self._ui_x_tick)
        self._select_and_set_y_lim_and_tick(self._ui_y_lim, self._ui_y_tick)
        #Boxplot resets the x-axis limits and tick marks.  This issue has been 
        #reported (https://github.com/matplotlib/matplotlib/issues/2921), but 
        #until it is fixed, it is important to set the limits and ticks after 
        #the data has been plotted. (If the ticks labels are set to 'auto', the 
        #self.x_tick_label setter does nothing.)
        if self._ui_x_tick_labels == 'auto':
            formatter = _mpl.ticker.ScalarFormatter()
            self.x_tick_labels = map(lambda x: formatter.format_data(x), self.x_tick_list)
            self._ui_tick_labels = 'auto'
        
    def plot_contours(self, x, y, z, **kwargs):
        """
        Plot three dimensional data as contours on the axes        
        
        Parameters
        ----------
        x : MxN numpy array
            x-coordinates of points
        y : MxN numpy array
            y-coordinates of points
        z : MxN numpy array
            z-coordinates of points. z-coordinates are used to create contours.
        plot_type : ['filled' | 'image' | 'lines'], optional, default: 'filled'
            Type of contour plot.  Valid options are:
            
            - filled: the area between two neighboring contour lines is filled 
              in with a single color.
            - image: contour lines are overlaid on the `z` data, which is 
              plotted as an image.  The `x` and `y` data must be on a uniform 
              grid.  In other words, all the columns of `x` must have the same 
              spacing dx, and all the rows of `y` must have the same spacing 
              dy.  (If your data is on an irregular grid, you can always 
              interpolate it onto a uniform grid.)  Because a uniform grid is 
              assumed, only the min and max values of `x` and `y` are used to 
              place the image.
            - lines: plots only contour lines.
             
        cl_levels : list of floats, optional
            Contour line levels.
        cl_labels : list of floats, optional
            Contour lines to label.
        cl_label_fsize : float or int, optional
            Contour line labels font size (in points).
        cl_label_fmt : string, optional
            Label format string. Ex: '%.2f', '%g', or '%d'
        cl_width : float or int, optional
            Contour line width (in points).
        cl_style : ['_' | '-' | '--' | ':' | None], optional, default: '-'
            Contour line style.
        cl_colors : list, optional
            Contour line colors (in RGB format).
            
        Returns
        -------
        b_obj : contourf object, image object, or None
            background object
        cl_obj : contour line object
        
        See Also
        --------
        Axes.add_image() : Adds an image to axes
        plot_functions.show_imgs() : Displays image(s) with an optional color 
            bar
        """
        plot_type = kwargs.pop('plot_type', 'filled')
        im_interp = kwargs.pop('im_interp', 'auto')
        c_map = kwargs.pop('c_map', _cp.colors.c_maps['rainbow'])
        c_lim = kwargs.pop('c_lim', ['auto', 'auto'])
        cl_levels = kwargs.pop('cl_levels', 'auto')
        cl_labels = kwargs.pop('cl_labels', 'auto')
        cl_label_fsize = kwargs.pop('cl_label_fsize', 14)
        cl_label_fmt = kwargs.pop('cl_label_fmt', '%g')
        cl_width = kwargs.pop('cl_width', 'auto')
        cl_style = kwargs.pop('cl_style', '-')
        cl_colors = kwargs.pop('cl_colors', 'auto')

        self._ui_c_lim = c_lim
        #Select color bar limits and tick spacing
        #(Hard code auto tick spacing because the color bar tick spacing
        #will be recalculated when the color bar is added to the figure.)
        [c_lim_c, c_tick_c, n_tick_c] = _utl.find_candidate_lim_and_tick(\
            c_lim, 'auto', [_np.min(z), _np.max(z)], 'linear', 10.0, self.exceed_lim)
        [c_lim, c_tick, n_tick] = _utl.select_lim_and_tick(c_lim_c, c_tick_c, \
            n_tick_c)
        #We have to include the limits in the levels because the colorbar seems
        #to disregard c_obj.set_clim() and c_bar.set_clim().
        #Round is needed so that the contour line labels match up exactly with 
        #the levels.
        if cl_levels is 'auto':
            cl_levels = _np.round(_np.arange(c_lim[0], \
                c_lim[1] + c_tick/100.0, c_tick/4.0), 12)
        else:
            if c_lim[0] not in cl_levels:
                cl_levels = _np.hstack([c_lim[0], cl_levels])
            if c_lim[1] not in cl_levels:
                cl_levels = _np.hstack([cl_levels, c_lim[1]])
            #Sort just in case the user specified levels outside of the limits
            cl_levels = _np.round(_np.sort(cl_levels), 12)
        
        #Define the contour line labels
        if cl_labels is 'auto':
            cl_labels = cl_levels[::2]
        else:
            cl_labels = _np.round(cl_labels, 12)
     
        #Verify that a proper plot type was specified   
        if plot_type not in ['filled', 'image', 'lines']:
            raise IOError("Did not recognize the plot type")    
        
        if cl_width is 'auto':
            #Define the contour line width
            if plot_type == 'filled':
                cl_width = 0.5
            elif plot_type == 'image':
                cl_width = 1
            else:
                cl_width = 2
        
        if cl_colors is 'auto':
            #If only showing contour lines, then color lines according to the 
            #colormap.  Otherwise make the lines black.
            if plot_type is 'lines':
                cl_colors = None
            else:
                cl_colors = [[0, 0, 0]]
        else:
            cl_colors = _utl.adjust_depth(cl_colors, 2)
        
        #Generate background
        if plot_type is 'filled':
            b_obj = self.mpl_ax.contourf(x, y, z, cl_levels, cmap = c_map)
        elif plot_type is 'image':
            #Verify that x and y data are appropriate for the 'image' plot type
            dx = _np.diff(x, axis = 1)
            avg_dx = _np.mean(dx)
            if ((_np.max(dx) - avg_dx) / avg_dx > 10e-3) or \
                ((avg_dx - _np.min(dx)) / avg_dx > 10e-3):
                raise IOError("x-data must be evenly spaced for 'image' plot type.")
            dy = _np.diff(y, axis = 0)
            avg_dy = _np.mean(dy)
            if ((_np.max(dy) - avg_dy) / avg_dy > 10e-3) or \
                ((avg_dy - _np.min(dy)) / avg_dy > 10e-3):
                raise IOError("y-data must be evenly spaced for 'image' plot type")
            del dx, dy
            #Plot the background image
            b_obj = self.add_image(z, c_map = c_map, \
                x = [x.min(), x.max()], y = [y.min(), y.max()], \
                im_origin = 'lower left', xy_coords = 'pixel centers', \
                c_lim = c_lim, interp = im_interp)
            #Clip the extra half a pixel on the edges
                
            xy_clip = _np.array([[_np.min(x), _np.min(y)], \
                                 [_np.max(x), _np.min(y)], \
                                 [_np.max(x), _np.max(y)], \
                                 [_np.min(x), _np.max(y)]])
            clip_patch = _mpl_patches.Polygon(xy_clip, \
                transform = self.mpl_ax.transData)
            b_obj.set_clip_path(clip_patch)
            
        #Generate contour lines
        if plot_type is 'lines':
            cl_obj = self.mpl_ax.contour(x, y, z, cl_levels, cmap = c_map, \
                linewidths = cl_width, linestyles = cl_style)
            b_obj = None
        else:
            cl_obj = self.mpl_ax.contour(x, y, z, cl_levels, colors = cl_colors, \
                linewidths = cl_width, linestyles = cl_style)
        
#        pcolor: contour lines are overlaid on the `z` data plotted using 
#        matplotlib's pcolormesh() function.  Unlike the 'image' plot type,
#        'pcolor' can handle unevenly spaced rows/columns of `x` and `y` 
#        data, but it is slower and creates bigger file sizes.
        ## I don't like pcolor compared to imshow.  pcolor's file size is 
        ## 10 times bigger (or more), it takes longer to execute, and you have to 
        ## extrapolate the x and y data on the last row and column to make it plot all 
        ## the z data.  pcolor can plot irregularly spaced data, but the user can 
        ## always interpolate onto a regular grid, so I like imshow better.
        #    elif plot_type == 'pcolor':
        #        dx0 = np.mean(np.diff(xy[0][0][0][:,0:2]))
        #        dy0 = np.mean(np.diff(xy[0][0][0][0:2,:]))
        #        c_obj = data_ax[0].pcolormesh(xy[0][0][0] - dx0/2.0, xy[1][0][0] - dy0/2.0, z, \
        #            cmap = c_dict['map'])
        #        c_obj.set_edgecolor('face')
        
        if cl_labels is not None:
            cl_obj.clabel(cl_labels, fmt = cl_label_fmt, \
                fontsize = cl_label_fsize)
        
        #Set the limits and ticks
        self._select_and_set_x_lim_and_tick(self._ui_x_lim, self._ui_x_tick)
        self._select_and_set_y_lim_and_tick(self._ui_y_lim, self._ui_y_tick)        
        
        return(b_obj, cl_obj)
        