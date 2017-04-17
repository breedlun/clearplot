# -*- coding: utf-8 -*-
#Created on Fri Jan 23 20:31:53 2015
#@author: Benjamin Reedlunn

import numpy as _np
from clearplot import utilities as _utl
from clearplot import axes as _axes
import matplotlib as _mpl

class Color_Bar(_axes._Axes_Base):
    """
    A color bar class
    """
    
    def __init__(self, data_obj, **kwargs):
        """
        Instantiates a color bar object        
        
        Parameters
        ----------
        data_obj : data object or a list of data objects
            Image or contours that the color bar pertains to
        position : 1x2 list or numpy array, optional
            Position of color bar lower left corner from the figure lower left 
            corner, in mm.
        ax_2_bar_gap : float, optional
            Gap between axes and color bar, in mm.  Only utilized if `postion`
            is automatically determined.
        orient : ['v', 'h'], optional
            Orientation of the color bar
        tick : float, optional
            Tick mark spacing.  If `tick` is set to 'auto', then the tick mark 
            spacing will be automatically selected.
        tick_list : list, optional
            Tick mark positions.  If `tick_list` is set to 'auto', then the 
            tick marks will be automaticaly selected.
        tick_labels : list of strings, optional
            Tick mark labels.  If `tick_labels` is set to 'auto', then the 
            tick marks will be automaticaly selected.
        lim : 1x2 list, optional
            Lower and upper limits.  If the string 'auto' is input instead of 
            a float, then the corresponding limit will be automaticaly 
            selected.
        scale : [ 'linear' | 'log' ], optional
            Color bar scaling.  The default is 'linear'.
        """
        self.data_objs = _utl.adjust_list_depth(data_obj, 1)
        self.data_ax = []
        for data_obj in self.data_objs:
             self.data_ax.append(data_obj.parent_ax)
        self.parent_fig = self.data_objs[0].parent_ax.parent_fig
        self.parent_fig.color_bars.append(self)
        self._ui_pos = kwargs.pop('position', 'auto')
        self.orient = kwargs.pop('orient', 'v')
        #Set the font size
        self.font_size = kwargs.pop('font_size', _mpl.rcParams['font.size'])
        self._ui_tick = kwargs.pop('tick', 'auto')
        self._ui_tick_list = kwargs.pop('tick_list', 'auto')
        self._ui_tick_labels = kwargs.pop('tick_labels', 'auto')
        #Use the user input color limits specified when the data object was 
        #added to the data axes as the default
        self._ui_lim = kwargs.pop('lim', data_obj._ui_c_lim)
        self._ui_scale = kwargs.pop('scale', 'linear')
        #Store information
        self.sdim = 20.0
        self._tick_mm = self.sdim
        self.ax_2_bar_gap = kwargs.pop('ax_2_bar_gap', 'auto')
        if self.ax_2_bar_gap == 'auto':
            self.ax_2_bar_gap = self.sdim * 0.5
            

        #Create axes that will contain the color bar
        #(When you do not supply axes, fig.colorbar() creates a color bar by 
        #dividing up the space in the original axes that the color bar 
        #pertains to.  Also, you can only specify the color bar position and 
        #size as fractions of the original axes.  Thus, it is much easier to 
        #specify the color bar axes.)
        #We do not know the size or position of the bar at this point, so we
        #just instantiate a color bar and update it with the proper size and
        #position later.  
        #(We could calculate the bar size and position ahead of time, the 
        #methods that set the limits and tick marks assume that a bar exits.  
        #We could write specialized methods to select the limits and tick 
        #marks without setting them, but that would duplicate a lot of code.  
        #It makes the most sense to just instantiate and update later.)
        #Find the data axes position in mm
        #Generate matplotlib axes object
        #(The random width is used to avoid a bug in concert with a supposed
        #feature of matplotlib.  If the user tries to create axes with the 
        #same dimensions and other properties as an existing set of axes, 
        #then matplotlib will return the existing axes, and not create a new
        #set of axes.  This "feature" should not affect anything here, because
        #axes are always moved from the coordinates below to some other 
        #location.  However, matplotlib 1.5.1 seems to have a bug, because it 
        #seems to think the original set of axes are still in their original
        #location, even though I moved them.)
        mpl_ax = self.parent_fig.mpl_fig.add_axes([0.0, 0.0, _np.random.rand(1)[0]/20, 0.5])
        #Generate the color bar
        if self.orient == 'v':
            orient = 'vertical'
        elif self.orient == 'h':
            orient = 'horizontal'
        else:
            raise ValueError("""ERROR: Orientation should be either 'h' or 'v'""")
        self.mpl_bar = self.parent_fig.mpl_fig.colorbar(data_obj, \
            cax = mpl_ax, orientation = orient, spacing = 'proportional')
        #Make the mpl axes object available on the top level so that 
        #_Axes_Base.annotate can find it
        self.mpl_ax = self.mpl_bar.ax
        #Make the tick marks point outward        
        self.mpl_ax.tick_params(axis = 'both', direction = 'out')
        #Only solid colorbars have the 'set_edgecolor' method.  Unfilled 
        #contour plots give non-solid colorbars that have colors only at the 
        #contour lines.
        if hasattr(self.mpl_bar.solids, 'set_edgecolor'):
            #It is known that some vector graphics viewer (svg and pdf) renders 
            #white gaps between segments of the colorbar. This is due to bugs 
            #in the viewers not matplotlib. As a workaround the colorbar can be 
            #rendered using the line below.  However this has negative 
            #consequences in other circumstances. Particularly with semi 
            #transparent images (alpha < 1) and colorbar extensions and is not 
            #enabled by default  (see matplotlib github issue #1188).
            self.mpl_bar.solids.set_edgecolor('face')
        #Specifying the scaling also sets the limits, the ticks, the size, and
        #the position of the color bar
        self.scale = self._ui_scale
        #Now that the matplotlib axes object has been created, we can
        #instantiate the color bar label
        self.label_obj = _Label(self)
        #Label the tick marks
        self.tick_labels = self._ui_tick_labels
    
    @property
    def lim(self):
        """
        Gets/sets the color bar limits.  Supply a 1x2 list of floats to 
        explicitly set the upper and lower limits.  If the string 'auto' is 
        input instead of a float, then the corresponding limit will be 
        automaticaly selected.
        """
        return(self._lim)
        
    @lim.setter
    def lim(self, lim):
        self._ui_lim = lim
        tick = self._ui_tick
        [lim, tick, n_tick] = self._set_lim_and_tick(lim, tick)
        return(lim, tick)

    @property
    def tick(self):
        """
        Get/sets the color bar tick mark spacing.  Supply a float to 
        explicitly set the tick marks spacing.  If `tick` is set to 'auto', 
        then the tick mark spacing will be automatically selected.
        """
        return(self._tick)
        
    @tick.setter
    def tick(self, tick):
        self._ui_tick = tick
        lim = self._ui_lim
        [lim, tick, n_tick] = self._set_lim_and_tick(lim, tick)
        return(lim, tick)
        
    @property
    def tick_mm(self):
        """
        Gets/sets the physical distance (in mm) between the tick marks.  Input 
        a float to specify a new spacing.
        """
        return(self._tick_mm)
        
    @tick_mm.setter
    def tick_mm(self, tick_mm):
        self._tick_mm = tick_mm
        self._set_size_and_position()
    
    @property
    def scale(self):
        """
        Gets/sets the scaling for the color bar.  Valid inputs include 'linear' 
        and 'log'.  Note: if you change the scaling when the axis limits 
        and ticks are set to 'auto' (the default), then the limits and ticks 
        will be recomputed.
        """
        return(self._ui_scale)
    
    @scale.setter
    def scale(self, scale):
        #It seems like I should not need to set all of these, but as of
        #matplotlib 1.5.1 they need to all be set.
        if scale == 'log':
            self._ui_scale = scale
            for data_obj in self.data_objs:
                data_obj.set_norm(_mpl.colors.LogNorm())
            self.mpl_bar.set_norm(_mpl.colors.LogNorm())
            self.mpl_bar.formatter = _mpl.ticker.LogFormatterMathtext()
        elif scale == 'linear':
            self._ui_scale = scale
            for data_obj in self.data_objs:
                data_obj.set_norm(_mpl.colors.Normalize())
            self.mpl_bar.set_norm(_mpl.colors.Normalize())
            self.mpl_bar.formatter = _mpl.ticker.ScalarFormatter()
        else:
            raise IOError('ERROR: unrecognized scaling')
        self._set_lim_and_tick(self._ui_lim[:], self._ui_tick)

    def _set_lim_and_tick(self, lim, tick):
        """Sets the limits and the tick spacing.  The lim and tick 
        setters perform the same operation, but they each recalculate the
        automatically selected limits and tick spacing in order to keep the 
        user interface simple.  This method computes the limits and tick 
        spacing once."""
        #Set the limits and ticks
        rgb_flag = False
        min_max = _np.zeros([len(self.data_objs),2])
        for s, data_obj in enumerate(self.data_objs):
            data = data_obj.get_array()
            if data.ndim > 2:
                rgb_flag = True
                break
            min_max[s,0] = data.min()
            min_max[s,1] = data.max()
        if rgb_flag:
            lim = self._ui_lim
            tick = self._ui_tick
            n_tick = (lim[1] - lim[0]) / tick
        else:
            mm = [_np.min(min_max[:,0]), _np.max(min_max[:,1])]
            [lim, tick, n_tick] = _utl.find_and_select_lim_and_tick(\
                self._ui_lim, self._ui_tick, mm,
                self.scale, 10.0, 0.0)
        self._lim = lim
        for data_obj in self.data_objs:
            data_obj.set_clim(lim)
        self._tick = tick
        self._num_tick = n_tick
        self.tick_list = self._ui_tick_list
        self.tick_labels = self._ui_tick_labels
        self._set_size_and_position()
        return(lim, tick, n_tick)
        
    def _set_size_and_position(self):
        """Set the color bar size and position, based on the number of ticks
        and the physical distance between tick marks."""
        ax_bboxes = []
        for da in self.data_ax:
            ax_bboxes.append(da.bbox)
        ax_bbox = _mpl.transforms.Bbox.union(ax_bboxes)         
        bar_width = self.sdim/4.0
        if self.orient == 'h':
            self.size = _np.array([self._num_tick * self.tick_mm, bar_width])
            #Place the color bar below the data axes, horizontally centered            
            if self._ui_pos is 'auto':
                bar_pos = _np.array([\
                    ax_bbox.x0 + ax_bbox.width/2.0  - self._num_tick * self.sdim / 2.0, \
                    ax_bbox.y0 - self.ax_2_bar_gap - bar_width])
                #We must immediately reset the user input position to 'auto'
                #since the position setter method assumes any input was 
                #supplied by the user.
                self.position = bar_pos
                self._ui_pos = 'auto'
            else:
                self.position = self._ui_pos
        elif self.orient == 'v':
            self.size = _np.array([bar_width, self._num_tick * self.tick_mm])
            #Place the color bar to the right of the data axes, vertically 
            #centered            
            if self._ui_pos == 'auto':
                bar_pos = _np.array([ax_bbox.x1 + self.ax_2_bar_gap, \
                    ax_bbox.y0 + ax_bbox.height/2.0 - self.size[1] / 2.0])
                #We must immediately reset the user input position to 'auto'
                #since the position setter method assumes any input was 
                #supplied by the user.
                self.position = bar_pos
                self._ui_pos = 'auto'
            else:
                self.position = self._ui_pos
        else:
            raise ValueError("""ERROR: Orientation should be either 'h' or 'v'""")
        if hasattr(self, 'label_obj'):
            if hasattr(self.label_obj, 'str_list'):
                self.label_obj.place_label()
        
    @property
    def label(self):
        """Sets/gets the color bar label.  Supply a 1x2 list of strings (in 
        LaTeX syntax) to specify the axis label text and axis units.  The 
        units will automatically be wrapped in paranthesises.  Supply a 1x1 
        list with a single string to create a label without any units."""
        return(self.label_obj.str_list)
    
    @label.setter   
    def label(self, str_list):
        if str_list is not None:
            str_list = _utl.adjust_depth(str_list, 1)
            self.label_obj.gen_label(str_list, self.font_size)
            self.label_obj.place_label()
    
    @property
    def tick_list(self):
        """
        Gets/sets tick mark positions.  Supply a list of values to 
        explicitly set the tick mark positions.  If `tick_list` is set to 
        'auto', then the tick marks will be automaticaly selected.
        """
        #As of matplotlib 1.5.1, you can only get the normalized ticks, which 
        #you then must convert.
        if self.orient == 'h':
            normalized_tick_list = self.mpl_ax.get_xticks()
        else:
            normalized_tick_list = self.mpl_ax.get_yticks()
        tick_list = self.data_objs[0].norm.inverse(normalized_tick_list)
        return(tick_list)
        
    @tick_list.setter
    def tick_list(self, tick_list):
        self._ui_tick_list = tick_list
        tick_list = _utl.gen_tick_list(tick_list, self.lim, self.tick, \
            self.scale, 10.0)
        self.mpl_bar.set_ticks(tick_list)
        if self.scale == 'log':
            #Minor log ticks do not seem to automatically appear in 
            #matplotlib 1.5.1.  
            #See https://github.com/matplotlib/matplotlib/issues/7141
            #Here is a work around.
            lim = self.lim
            tick = self.tick
            lim_diff = _np.log10(lim[1]) - _np.log10(lim[0])
            num_dec = lim_diff / tick
            minor_ticks = _np.array([])
            for n in _np.arange(num_dec):
                minor_ticks = _np.hstack([minor_ticks, \
                    (lim[0]*10.0**n)*_np.arange(2, 10, 1)])
            normalized_minor_ticks = self.data_objs[0].norm(minor_ticks)
            if self.orient == 'h':
                self.mpl_bar.ax.xaxis.set_ticks(\
                    normalized_minor_ticks, minor = True)
            else:
                self.mpl_bar.ax.yaxis.set_ticks(\
                    normalized_minor_ticks, minor = True)
        
    @property
    def tick_labels(self):
        """
        Gets/sets tick labels.  Assign a list of strings to set the labels.
        """
        return(self.mpl_bar.get_ticklabels())
    
    @tick_labels.setter
    def tick_labels(self, labels):
        self._ui_tick_labels = labels
        if labels != 'auto':
            set_tick_labels = []
            for label in labels:
                txt = _utl.raw_string(label)
                set_tick_labels.append('$\sf{' + txt + '}$')
            self.mpl_bar.set_ticklabels(set_tick_labels)

class _Label(object):
    def __init__(self, parent_bar):
        """
        """
        self.parent_bar = parent_bar
        self._pos = _np.array([0,0])
        self.anno = []
    
    @property
    def position(self):
        """
        Gets/sets position of color bar label, in mm units, relative to the 
        lower left corner of the color bar axes
        """
        return(self._pos)
        
    @position.setter
    def position(self, pos):
        #The position of the annotations were supplied to matplotlib in points
        #units, so we must convert from mm to points.
        pos_pt = pos * 72.0/25.4
        #The reference point is the position of the label, not the units.
        ref_pt = self.anno[0].xyann
        #Find the change in position and move the label and the units
        dx_pt = pos_pt - ref_pt
        for obj in self.anno:
            obj.xyann = obj.xyann + dx_pt
        self._pos = pos
    
    def gen_label(self, str_list, font_size = _mpl.rcParams['font.size']):
        """
        Generates a color bar label with or without units in parenthesis
        
        Parameters
        ----------
        str_list: list of str
            Label text and units in LaTeX syntax.
        font_size: float, optional
            font size (in points)
        """
        self.str_list = str_list
        #Initialize the storage list
        self.anno = []
        
        #Get rid of escape characters (ex: \n)
        for i in range(len(str_list)):
            str_list[i] = _utl.raw_string(str_list[i])
        
        #Create the label 
        #(Label position will be wrong to begin with. Once we know the size of 
        #the label, we will move it into the proper position.)
        x = _np.array([0.0,0.0])
        #Generate text and add object to the list
        #(I originally attempted to specify the font via the keyword 
        #"fontname =", but that does not work when using mathtext.  You must 
        #specify the font using the "mpl.rcParams['mathtext.XXX'] = " command.)
        self.anno.append(self.parent_bar.annotate('$' + str_list[0] + '$', \
            x, 'axes mm', verticalalignment = 'baseline', fontsize = font_size))
        #If units have been specified:
        if len(str_list) > 1:
            #Get size of label so we know where to put units
            var_bbox = self.parent_bar.get_obj_bbox(self.anno[0])
            #Define units spacing from variable text
            x[0] = var_bbox.x1 + 3.1 * font_size/18.0
            #Generate units and add object to the list
            #(I originally attempted to specify the font via the keyword 
            #"fontname =", but that does not work when using mathtext.  You 
            #must specify the font using the 
            #"mpl.rcParams['mathtext.XXX'] = " command.)   
            self.anno.append(self.parent_bar.annotate(\
                '$\mathsf{(' + str_list[1] + ')}$', x, 'axes mm', \
                verticalalignment = 'baseline', fontsize = font_size))
    
    def place_label(self):
        bboxes = []
        font_sizes = []
        for obj in self.anno:
            #Find the width and height of text
            bboxes.append(self.parent_bar.get_obj_bbox(obj))
            #Find the font size
            font_sizes.append(obj.get_fontsize())
        #Find the total width and height of the text
        bbox = _mpl.transforms.Bbox.union(bboxes)
        #Get the bounding boxes of the color bar 
        bar_bbox = self.parent_bar.bbox
        bar_tight_bbox = self.parent_bar.tight_bbox
        #Get the font size in mm units
        font_size = max(font_sizes)
        font_size_mm = font_size * 25.4/72.0
    
        x_0 = self.position
        #Define how far to move the label text to center it
        if self.parent_bar.orient.lower() == 'v':
            dx = _np.array([(bar_tight_bbox.width / 2.0 - bbox.width / 2.0) - x_0[0], \
                ((bar_tight_bbox.y1 - bar_bbox.y0) - x_0[1]) + font_size_mm * 0.7])
        else:
            #(I tried subtracting half the text bounding box height also, but it 
            #did not look right.)
            dx = _np.array([ ((bar_tight_bbox.x1 - bar_bbox.x0) - x_0[0]) \
                + font_size_mm * 0.5, -bar_bbox.height / 2.0 - x_0[1]]) 
        
        #Move the label
        self.position = x_0 + dx