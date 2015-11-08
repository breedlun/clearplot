# -*- coding: utf-8 -*-
#Created on Sun Mar 22 15:46:24 2015
#author: Benjamin Reedlunn

import numpy as _np
import utilities as _utl
import matplotlib as _mpl
import clearplot as _cp

class Axis_Label(object):
    """
    Axis label class
    """
    def __init__(self, ax, orient):
        """
        Instantiates an axis label object
        
        Parameters
        ----------
        ax : axes object
            Axes the label pertains to.
        orient: float
            angle in radians specifying the orientation of the axis label 
            (should be 0 for a horizontal axis label or pi/2 for a vertical 
            axis label)
        """
        self.parent_ax = ax
        self.orient = orient
        self.anno = None
        self.str_list = None
        self._pos = _np.array([0,0])
        #Specifies whether label is to be placed with a arrow indicating the 
        #direction of increasing values
        self.arrow_bool = _cp.params.axis_arrow_bool
        #Store distance between tick marks (in mm)
        if orient == 0.0:
            self._tick_mm = ax.x_tick_mm
        else:
            self._tick_mm = ax.y_tick_mm
    
    @property
    def position(self):
        """
        Sets/gets the axis label position.  If the axis label has an arrow, 
        then the position is the arrow tip.  Otherwise the position is the 
        lower left most item in the axis label.  Input a 1x2 numpy array, in mm 
        units, to alter the axis label position. 
        """
        return(self._pos)
        
    @position.setter
    def position(self, pos):
        #The position of the annotations were supplied to matplotlib in points
        #units, so we must convert from mm to points.
        pos_pt = pos * 72.0/25.4
        #If the axis label has an arrow, then the arrow tip is the reference
        #point that `pos` applies to.  Otherwise the reference point is the
        #location of the lower left most item in the axis label.
        if self.arrow_bool:
            ref_pt = self.arrow.xy
            self.arrow.xy = pos_pt
        else:
            ref_pt = self.anno[0].xyann
        #Find the change in position and move the label and the units
        dx_pt = pos_pt - ref_pt
        for obj in self.anno:
            obj.xyann = obj.xyann + dx_pt
        self._pos = pos
        
#    @property
#    def arrow_bool(self):
#        return(self._arrow_bool)
#        
#    @arrow_bool.setter
#    def arrow_bool(self, arrow_bool):
#        if self._arrow_bool != arrow_bool:
#            self._arrow_bool = arrow_bool
#            self.place_label()
        
    def gen_arrow(self, x, cs, length = 'auto', \
            head_length = 'auto', head_aspect_ratio = 3.0, color = [0,0,0]):
        """
        Creates an arrow whose head has a curved back.  The arrow can be placed
        relative to several coordinate systems, yet it retains it's shape, even 
        when the data limits, axes, or figure window change size.
                
        Parameters
        ----------
        x: 1x2 numpy array
            Coordinates for tip of arrowhead
        cs: string or 1x2 list
            Specifies the coordinate system for the coordinates in `x`.  See
            the description of `cs_1` in the axes.annotate method for more 
            information.
        length: float, optional
            Length of the arrow from tip to tail in mm
        color: 1x3 list, optional
            RGB value for the arrow
            
        Returns
        -------
        arrow: annotation object
        """
        if length == 'auto':
            length = self._tick_mm
        if head_length == 'auto':
            head_length = 7.0 * self._tick_mm / 20.0
        arrow = self.parent_ax._add_arrow('=)>', x, cs, \
            self.orient, length, head_length, head_aspect_ratio, color)
        return(arrow)
    
    def gen_label(self, str_list, font_size = _mpl.rcParams['font.size']):
        """
        Generates an axis label with or without units in parenthesis
        
        Parameters
        ----------
        str_list: list of str
            Label text and units in LaTeX syntax.
        font_size: float, optional
            font size (in points)
        """
        #Save the input string
        self.str_list = str_list
        #Initialize the storage list
        #(The first item in the list should be the bottom left-most annotation)
        self.anno = []
        #Calculate font size in mm units
        font_size_mm = font_size * 25.4/72.0    
        
        #Get rid of escape characters (ex: \n)
        for i in range(len(str_list)):
            str_list[i] = _utl.raw_string(str_list[i])
            
#        var_text = _utl.raw_string(var_text)
#        if units is not None:
#            units = _utl.raw_string(units)
        
        #Create the label 
        #(Label position will be wrong to begin with. Once we know the size of 
        #the label, we will move it into the proper position.)
        x = _np.array([0.0, 0.0])
        if self.orient == 0:
            #Horizontal Label
            #Define axis label text spacing from arrowhead and units spacing from 
            #variable text
            txt_spacing = _np.array([4.0 * font_size/18.0, 3.1 * font_size/18.0])
            if self.arrow_bool:
                #Print arrow so that head lines up with the first tick mark
                self.arrow = self.gen_arrow(x, ['axes mm', 'axes mm'], \
                    length = self.parent_ax.sdim)
                #Specify the x coordinate offset to the left edge of the text.
                x[0] = txt_spacing[0]
            else:
                self.arrow = None
                x[0] = 0.0
            #Specify the y coordinate of the bottom edge of the text.  We need 
            #a y offset to get baseline aligned text to align with the 
            #arrowhead.  (We use baseline aligned text instead of center 
            #aligned so that the units match up with the text.)
            x[1] = - font_size_mm * 0.28
            #Generate text and add object to the list
            #(I originally attempted to specify the font via the keyword 
            #"fontname =", but that does not work when using mathtext.  You must 
            #specify the font using the "mpl.rcParams['mathtext.XXX'] = " command.)
            self.anno.append(self.parent_ax.annotate('$' + str_list[0] + '$', x, \
                'axes mm', verticalalignment = 'baseline', fontsize = font_size))
            #If units have been specified:
            if len(str_list) > 1:
                #Get size of label so we know where to put units
                label_bbox = self.parent_ax.get_obj_bbox(self.anno[0])
                #Generate units and add object to the list
                #(I originally attempted to specify the font via the keyword 
                #"fontname =", but that does not work when using mathtext.  You 
                #must specify the font using the 
                #"mpl.rcParams['mathtext.XXX'] = " command.)
                x[0] = label_bbox.x1 + txt_spacing[1]     
                self.anno.append(self.parent_ax.annotate(\
                    '$\mathsf{(' + str_list[1] + ')}$', x, 'axes mm', \
                    verticalalignment = 'baseline', fontsize = font_size))
        else:
            #Vertical Label
            #Define axis label text spacing from arrowhead and units spacing from 
            #variable text
            txt_spacing = _np.array([3.3 * font_size/18.0, 2.2 * font_size/18.0])
            if self.arrow_bool:
                #Print arrow at first tick mark
                self.arrow = self.gen_arrow(x, ['axes mm', 'axes mm'], \
                    length = self.parent_ax.sdim)
                #Specify the y coordinate offset to the bottom edge of the text.
                x[1] = txt_spacing[0]
            else:
                self.arrow = None
                x[1] = 0.0
            #If units have been specified:
            if len(str_list) > 1:
                #Create units and add object to the list
                #(I originally attempted to specify the font via the keyword 
                #"fontname =", but that does not work when using mathtext.  You 
                #must specify the font using the "mpl.rcParams['mathtext.XXX'] = " 
                #command.)
                self.anno.append(self.parent_ax.annotate(\
                    '$\mathsf{(' + str_list[1] + ')}$', x, 'axes mm', \
                    fontsize = font_size, verticalalignment = 'bottom', \
                    horizontalalignment = 'center'))
                #Get size of units so we know where to put the label
                units_bbox = self.parent_ax.get_obj_bbox(self.anno[0])
                #Specify the y coordinate offset to the bottom edge of the text.
                x[1] = units_bbox.y1 + txt_spacing[1]
            #Generate text and add object to the list
            #(I originally attempted to specify the font via the keyword 
            #"fontname =", but that does not work when using mathtext.  You must 
            #specify the font using the "mpl.rcParams['mathtext.XXX'] = " command.)
            self.anno.append(self.parent_ax.annotate('$' + str_list[0] + '$', x, 
                'axes mm', fontsize = font_size, verticalalignment = 'bottom', \
                horizontalalignment = 'center'))
#            #Visualize the baseline
#            self.parent_ax.add_line(_np.array([[x[0]-5.0, x[1]], [x[0] + 5.0, x[1]]]))
    
    def place_label(self):
        """
        Places the axis label
        """
        ax = self.parent_ax
        bboxes = []
        font_sizes = []
        for obj in self.anno:
            #Find the width and height of text, relative to the lower left 
            #corner of the figure window
            bboxes.append(ax.parent_fig.get_obj_bbox(obj))
            #Find the font size
            font_sizes.append(obj.get_fontsize())
        #Find the total width and height of the text (without any arrows)
        bbox = _mpl.transforms.Bbox.union(bboxes)
        #Translate the bounding box to be relative to the lower left corner of
        #the axes
        bbox = bbox.translated(-ax.position[0], -ax.position[1])
        #Get the font size in mm units
        font_size = max(font_sizes)
        font_size_mm = font_size * 25.4/72.0
        
        #Get the bounding box of the data axes, relative to the lower left 
        #corner of the figure window
        #(Use get_tight_bbox and get_bbox to get the dimensions with and 
        #without tick mark labels.)
        ax_tgt_bbox = ax.tight_bbox
        #Translate the bounding box to be relative to the lower left corner of
        #the axes
        ax_tgt_bbox = ax_tgt_bbox.translated(-ax.position[0], -ax.position[1])
        #Get data axis size
        ax_size = ax.size
        #Get the position of the label
        x_0 = self.position
        
#        #Visualize the baseline
#        self.parent_ax.add_line(_np.array([[x_0[0]-5.0, x_0[1]], [x_0[0] + 5.0, x_0[1]]]))
    
#            #Verify that you have captured the bounding boxes
#            from matplotlib.patches import Rectangle
#            fig_size = self.parent_fig.size
#            rect = Rectangle([bboxes[-1].x0/fig_size[0], bboxes[-1].y0/fig_size[1]], \
#                bboxes[-1].width/fig_size[0], bboxes[-1].height/fig_size[1], \
#                linewidth = 0.75, color = [0,0,0], transform = self.parent_fig.mpl_fig.transFigure, \
#                fill = False)
#            self.mpl_ax.patches.append(rect)
#            label.append(rect)
#            if len(bboxes) > 1:
#                rect = Rectangle([bboxes[-2].x0/fig_size[0], bboxes[-2].y0/fig_size[1]], \
#                    bboxes[-2].width/fig_size[0], bboxes[-2].height/fig_size[1], \
#                    linewidth = 0.75, color = [0,0,0], transform = self.parent_fig.mpl_fig.transFigure, \
#                    fill = False)
#                self.mpl_ax.patches.append(rect)
#                label.append(rect)
#            rect = Rectangle([bbox.x0/fig_size[0], bbox.y0/fig_size[1]], \
#                bbox.width/fig_size[0], bbox.height/fig_size[1], \
#                linewidth = 0.75, color = [0,0,0], transform = self.parent_fig.mpl_fig.transFigure, \
#                fill = False)
#            self.mpl_ax.patches.append(rect)
#            label.append(rect)

        x_t1 = _np.zeros(2)
        if self.orient == 0:
            #Horizontal Label
            if ax.mpl_ax.xaxis.get_label_position() == 'bottom':
                #First x-axis (on bottom)
                x_t1[1] = ax_tgt_bbox.y0
            else:
                #Second x-axis (on top)
                x_t1[1] = ax_tgt_bbox.y1
            #Find the first tick mark in mm
            mm_per_data_units = ax_size[0]/_np.diff(ax.mpl_ax.get_xlim())[0]
            x_t1[0] = mm_per_data_units * \
                (ax.mpl_ax.get_xticks()[0] - ax.mpl_ax.get_xlim()[0])
        else:
            #Vertical Label
            if ax.mpl_ax.yaxis.get_label_position() == 'left':
                #First y-axis (on left side)
                x_t1[0] = ax_tgt_bbox.x0
            else:
                #Second y-axis (on right side)
                x_t1[0] = ax_tgt_bbox.x1
            #Find the first tick mark in mm
            mm_per_data_units = ax_size[1]/_np.diff(ax.mpl_ax.get_ylim())[0]
            x_t1[1] = mm_per_data_units * \
                (ax.mpl_ax.get_yticks()[0] - ax.mpl_ax.get_ylim()[0])
    
#        #Visualize the first tick
#        self.parent_ax.add_line(_np.array([[x_t1[0], x_t1[1]], [x_t1[0] + 5.0, x_t1[1]]]))
    
        if self.arrow_bool:
            #Find the number of tick marks (not including the first one)
            if self.orient == 0:
                N_tick = len(ax.mpl_ax.get_xticks()) - 1.0
            else:                
                N_tick = len(ax.mpl_ax.get_yticks()) - 1.0
            
            #Decide how many tick marks to move the label
            if N_tick % 2 != 0: #if odd
                if N_tick > 1:
                    ds_tick = _np.ceil(N_tick / 2.0)
                if N_tick <= 1:
                    ds_tick = _np.floor(N_tick / 2.0)
            else:
                ds_tick = N_tick / 2.0        
            #Define displacement for axis label
            if self.orient == 0:
                if ax.mpl_ax.xaxis.get_label_position() == 'bottom':
                    #Horizontal label for first x-axis (on bottom)
                    height_above_ax_bndry = bbox.y1 - x_t1[1]
                    horiz_dist_from_1st_tick = x_0[0] - x_t1[0]
                    dx = _np.array([-horiz_dist_from_1st_tick + ds_tick * self._tick_mm, \
                        - height_above_ax_bndry - 2.5/8.0 * font_size_mm])
                else:
                    #Horizontal label for second x-axis (on top)
                    height_below_ax_bndry = x_t1[1] - bbox.y0
                    horiz_dist_from_1st_tick = x_0[0] - x_t1[0]
                    dx = _np.array([-horiz_dist_from_1st_tick + ds_tick * self._tick_mm, \
                        + height_below_ax_bndry + 2.5/8.0 * font_size_mm])
            elif ax.mpl_ax.yaxis.get_label_position() == 'left':
                #Vertical label for first y-axis (on left side)
                width_right_of_ax_bndry = bbox.x1 - x_t1[0]
                vert_dist_from_1st_tick = x_0[1] - x_t1[1]
                dx = _np.array([- width_right_of_ax_bndry - 19.0/32.0 * font_size_mm, \
                     -vert_dist_from_1st_tick + ds_tick * self._tick_mm])
            else:
                #Vertical label for second y-axis (on right side)
                width_left_of_ax_bndry = x_t1[0] - bbox.x0
                vert_dist_from_1st_tick = x_0[1] - x_t1[1]
                dx = _np.array([width_left_of_ax_bndry + 19.0/32.0 * font_size_mm, \
                    -vert_dist_from_1st_tick + ds_tick * self._tick_mm])
        else:
            #Define displacement for axis label
            if self.orient == 0:
                #Horizontal Label
                xticks = ax.mpl_ax.get_xticks()
                height_above_ax_bndry = bbox.y1 - x_t1[1]
                horiz_dist_from_1st_tick = x_0[0] - x_t1[0]
                dx = _np.array([-horiz_dist_from_1st_tick + \
                    (xticks[-1] - xticks[0]) * mm_per_data_units / 2.0 - bbox.width/2.0, \
                    - height_above_ax_bndry -  3.0/8.0 * font_size_mm])
            elif ax.mpl_ax.yaxis.get_label_position() == 'left':
                #Vertical label for first y-axis (on left side)
                yticks = ax.mpl_ax.get_yticks()
                width_right_of_ax_bndry = bbox.x1 - x_t1[0]
                vert_dist_from_1st_tick = x_0[1] - x_t1[1]
                dx = _np.array([-width_right_of_ax_bndry - 19.0/32.0 * font_size_mm, \
                    - vert_dist_from_1st_tick + \
                    (yticks[-1] - yticks[0]) * mm_per_data_units / 2.0 - bbox.height/2.0])
            else:
                #Vertical label for second y-axis (on right side)
                yticks = ax.mpl_ax.get_yticks()            
                width_left_of_ax_bndry = x_t1[0] - bbox.x0
                vert_dist_from_1st_tick = x_0[1] - x_t1[1]
                dx = _np.array([width_left_of_ax_bndry + 19.0/32.0 * font_size_mm, \
                    - vert_dist_from_1st_tick + \
                    (yticks[-1] - yticks[0]) * mm_per_data_units / 2.0 - bbox.height/2.0])   

        #Move the axis label
        self.position = x_0 + dx