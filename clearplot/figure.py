# -*- coding: utf-8 -*-
#Created on Sat Sep 20 11:23:30 2014
#@author: breedlu

import matplotlib as _mpl
import matplotlib.pyplot as _plt
import numpy as _np
from matplotlib.lines import Line2D as _mpl_Line2D
from matplotlib.patches import Polygon as _mpl_Polygon
import matplotlib.text as _mpl_text
import clearplot as _cp
import axes as _axes
import color_bar as _color_bar
import utilities as _utl

class Figure(object):
    """
    Figure class 
    
    """
    
    def __init__(self, size = 'auto', dpmm = _cp.params.dpmm):
        """
        Instantiates a figure object        
        
        Parameters
        ----------
        fig_size: list or tuple, optional
            Width and height of figure in mm
        dpmm: float, optional
            Dots per mm
        """
        self._ui_size = size
        if size is 'auto':
            size_inch = _np.array(_mpl.rcParams['figure.figsize'])
        else:
            size_inch = _np.array(size) / 25.4
        self.mpl_fig = _plt.figure(figsize = size_inch, dpi = dpmm * 25.4)
        #Force the figure to be on top of all other windows
        self.put_window_on_top()
        #Set the figure renderer to None
        self._renderer = None
        #Set the number of mm to pad the tight bbox
        self.tight_bbox_pad = _mpl.rcParams['savefig.pad_inches'] * 25.4
        #Initialize the axes container
        self.axes = []
        #Initialize the color_bar container
        self.color_bars = []
    
    def add_axes(self, **kwargs):
        """
        Adds a set of generic axes to the figure
        
        Parameters
        ----------
        Keyword arguments get passed to axes.Axes()
                
        Returns
        -------
        ax : axes object
        """
        ax = _axes.Axes(self, **kwargs)
        return(ax)
        
    def add_invisible_axes(self, **kwargs):
        """
        Adds a set of invisible axes to the figure.
        
        Parameters
        ----------        
        Keyword arguments get passed to axes.Invisible_Axes()
        
        Returns
        -------
        ax : invisible axes object
        """
        ax = _axes.Invisible_Axes(self, **kwargs)
        return(ax)
        
#    def add_axes_grid(self, n_row = 1, n_col = 1, position = 'auto', **kwargs):
#        ax_list = []
#        for i in range(n_row):
#            if i == 0:
#                position = 'auto'
#            else:
#                ax_upper_left = ax_list[0].position
#                ax_upper_left[1] = ax_upper_left[1] + ax_list[0].size[1]
#                trans = _utl.Offset_From(ax_list[i-1], [0,1], 'mm')
#                position = [0, 20]
#            ax_list.append(_axes.Axes(self, position, transform = trans, **kwargs))
#                
#        self.axes.extend(ax_list)
#        return(ax_list)
      
    @property  
    def tight_bbox(self):
        """
        Get/set the tight bounding box for the figure, in mm.
        """
        #It seems to matter if you have a draw command before getting the 
        #tight bbox
        self.draw()
        #NOTE: this is a blatant copy from print_figure() in matplotlib's
        #backend_bases.py, but I made a few changes:
        #1) The padding was changed to mm units.
        #2) The bbox width and height are checked to make sure they are not
        # infinity.
        bbox_inches = self.mpl_fig.get_tightbbox(self.renderer) 
        bbox_artists = self.mpl_fig.get_default_bbox_extra_artists()
        bbox_filtered = []
        for a in bbox_artists:
            bbox = a.get_window_extent(self.renderer)
            if a.get_clip_on():
                clip_box = a.get_clip_box()
                if clip_box is not None:
                    bbox = _mpl.transforms.Bbox.intersection(bbox, clip_box)
                clip_path = a.get_clip_path()
                if clip_path is not None and bbox is not None:
                    clip_path = clip_path.get_fully_transformed_path()
                    bbox = _mpl.transforms.Bbox.intersection(bbox,
                                             clip_path.get_extents())
            if bbox is not None and (bbox.width != 0 or bbox.height != 0) and \
                _np.abs(bbox.width) != _np.inf and \
                _np.abs(bbox.height) != _np.inf:
                bbox_filtered.append(bbox)

        if bbox_filtered:
            _bbox = _mpl.transforms.Bbox.union(bbox_filtered)
            trans = _mpl.transforms.Affine2D().scale(1.0 / self.mpl_fig.dpi)
            bbox_extra = _mpl.transforms.TransformedBbox(_bbox, trans)
            bbox_inches = _mpl.transforms.Bbox.union([bbox_inches, bbox_extra])

        bbox_inches = bbox_inches.padded(self.tight_bbox_pad/25.4)      
        #This is the end of the copy from matplotlib's print_figure()
        
        #Convert the bbox from inches to mm        
        trans = _mpl.transforms.Affine2D()
        trans.scale(25.4, 25.4)
        bbox = bbox_inches.transformed(trans)
        return(bbox)
                
    @property
    def mm_to_pix_trans(self):
        """
        Gets a transformation object that converts mm to pixels, relative to 
        the bottom left hand corner of the figure.
        """
        fig_size_pix = self.mpl_fig.bbox.size
        fig_size = self.size
        trans = _mpl.transforms.Affine2D()
        trans.scale(fig_size_pix[0] / fig_size[0], fig_size_pix[1] / fig_size[1])
        return(trans)
        
    @property
    def fig_to_mm_trans(self):
        """
        Gets a transformation object that converts normalized figure 
        coordinates to mm, relative to the bottom left hand corner of the 
        figure.
        """
        fig_size = self.size
        trans = _mpl.transforms.Affine2D()
        trans.scale(fig_size[0], fig_size[1])
        return(trans)
        
    def put_window_on_top(self):
        """
        Places the figure window on top of all other windows if interactive
        mode is on.
        """
        if hasattr(self.mpl_fig.canvas.manager, 'window') and _plt.isinteractive():
            #Force the figure to be on top of all other windows
            if hasattr(self.mpl_fig.canvas.manager.window, 'attributes'):
                #(The command below doees not work with the MacOSX or Qt4Agg backend.  
                #I have only verified it works with the TkAgg backend.)
                self.mpl_fig.canvas.manager.window.attributes('-topmost', 1)
                #Disable this right afterwards so that other windows can be on top of the 
                #figure window
                self.mpl_fig.canvas.manager.window.attributes('-topmost', 0)
            elif hasattr(self.mpl_fig.canvas.manager.window, 'raise_'):
                #(The command below doees not work with the MacOSX or TkAgg backend.  
                #I have only verified it works with the Qt4Agg backend.)                
                self.mpl_fig.canvas.manager.window.raise_()
    
    @property
    def renderer(self):
        """
        Gets the current renderer
    
        Returns
        -------
        renderer: renderer object
        """
        if self._renderer is None:
            if hasattr(self.mpl_fig.canvas, "get_renderer"):
                #Some backends, such as TkAgg, have the get_renderer method, 
                #which makes this easy.
                self._renderer = self.mpl_fig.canvas.get_renderer()
            elif hasattr(self.mpl_fig.canvas, "print_pdf"):
                #Other backends do not have the get_renderer method, so we have a work 
                #around to find the renderer.  Print the figure to a temporary file 
                #object, and then grab the renderer that was used.
                #(I stole this trick from the matplotlib backend_bases.py 
                #print_figure() method.)
                import io
                self.mpl_fig.canvas.print_pdf(io.BytesIO())
                self._renderer = self.mpl_fig._cachedRenderer
            else:
                self._renderer = self.mpl_fig.canvas.renderer
        return(self._renderer)
        #Old method that gives the incorrect renderer   
        #renderer = _mpl.backend_bases.RendererBase()
        #For further information, see this post:
        #http://stackoverflow.com/questions/22667224/matplotlib-get-text-bounding-box-independent-of-backend/22689498#22689498
        
    def add_text(self, x, txt, **kwargs):
        """
        Adds text to the figure window
        
        Parameters
        ----------
        x: 1x2 numpy array
            Coordinates of the text in mm
        txt: string
            Text to add to the figure
        kwargs:
            Keyword arguments to matplotlib's text function
            
        Returns
        -------
        txt_obj: text object
        
        See Also
        --------
        ax.add_text : adds text to axes
        ax.annotate : adds an annotation to the axes
        """
        #Convert into normalized figure coordinates
        fig_size = self.size
        x_nfc = _np.array(x) / fig_size
        #Add text to the figure
        txt_obj = self.mpl_fig.text(x_nfc[0], x_nfc[1], txt, **kwargs)
        return(txt_obj)
    
    def add_line(self, x, **kwargs):
        """
        Adds a 2D line to the figure
        
        Parameters
        ----------
        x: 2x2 numpy array
            Coordinates of the line in mm.  First row contains the first point,
            and the second row contains the second point.
        kwargs:
            Keyword arguments to matplotlib's Line2D class
            
        Returns
        -------
        line_obj: matplotlib line object
        
        See Also
        --------
        ax.add_line : adds line to axes
        ax.annotate : adds an annotation to the axes
        """
        #Convert the coordinates into normalized figure coordinates
        fig_size = self.size
        x_nfc = _np.array(x)
        x_nfc[:,0] = x_nfc[:,0] / fig_size[0]
        x_nfc[:,1] = x_nfc[:,1] / fig_size[1]
        #Create the line object
        line_obj = _mpl_Line2D(x_nfc[:,0], x_nfc[:,1], transform = self.mpl_fig.transFigure, **kwargs)
        #Add the line to the figure
        self.mpl_fig.lines.append(line_obj)
        return(line_obj)
        
    def add_polygon(self, x, **kwargs):
        """
        Adds a polygon to the figure
        
        Parameters
        ----------
        x: Nx2 numpy array
            Coordinates of the polygon in mm.  First row contains the first 
            point, the second row contains the second point, etc.
        kwargs:
            Keyword arguments to matplotlib's Polygon class
            
        Returns
        -------
        patch_obj: matplotlib patch object
        """
        #Convert the coordinates into normalized figure coordinates
        fig_size = self.size
        x_nfc = _np.array(x)
        x_nfc[:,0] = x_nfc[:,0] / fig_size[0]
        x_nfc[:,1] = x_nfc[:,1] / fig_size[1]
        #Create the polygon object
        patch_obj = _mpl_Polygon(x_nfc, transform = self.mpl_fig.transFigure, **kwargs)
        #Add the polygon to the figure
        self.mpl_fig.patches.append(patch_obj)
        return(patch_obj)
        
    def add_color_bar(self, ax, im_obj, **kwargs):
        """
        Places a color bar in the specified figure   
        
        Parameters
        ----------
        ax : axes object
            Axes object that contains `im_obj`.
        im_obj : image object
            Image object that the color bar pertains to.
        label : list
            

        Other Parameters
        ----------------
        See parameters in Color_Bar()
        """
        bar = _color_bar.Color_Bar(self, ax, im_obj, **kwargs)
        label = kwargs.pop('label', None)
        if label is not None:
            #Make sure the label is in the correct format
            label = _utl.adjust_depth(label, 1)
            #Apply the label
            bar.label = label
        
        return(bar)
    
    def get_obj_bbox(self, obj):
        """
        Finds the coordinates of the bounding box surrounding an object, in mm, 
        relative to the lower left corner of the figure window
        
        Parameters
        ----------
        obj: graphics primitive object 
            object you wish to get the bounding box for
        
        Returns
        -------
        bbox: bounding box object
        """
        #Since many objects are defined relative to other objects, it is 
        #important to draw the object.  Otherwise, a call to 
        #obj.get_window_extent can give incorrect values.
        obj.draw(self.renderer)
        #Get dimensions of object in pixel units
        bbox_pix = obj.get_window_extent(self.renderer)
        #Convert to mm units
        bbox = bbox_pix.transformed(self.mm_to_pix_trans.inverted())
        #For some reason, the bounding box for LaTeX text is too tight in the 
        #vertical direction.  All other text bounding boxes have some padding, 
        #so LaTeX bounding boxes need to be adjusted.
        if _mpl.rcParams['text.usetex']:
            if obj.findobj(match=_mpl_text.Text) and obj.get_text() != '':
                #Set the amount of adjustment (in mm)
                y_adj = 0.7
                #Shift the text position up or down, as needed
                #(This assumes that position is defined in mm)
                [x, y] = obj.get_position()
                if obj.get_va() == 'bottom':
                    y = y + y_adj
                elif obj.get_va() == 'top':
                    y = y - y_adj
                obj.set_position([x,y])
                #Get the new bounding box
                bbox_pix = obj.get_window_extent(self._renderer)
                #Convert to mm units
                bbox = bbox_pix.transformed(self.mm_to_pix_trans.inverted())
                #Adjust the new bounding box
                bbox = bbox.from_extents(bbox.x0, bbox.y0 - y_adj, \
                    bbox.x1, bbox.y1 + y_adj)
                    
#        #Verify that you have captured the bounding box
#        from matplotlib.patches import Rectangle
#        fig_size = self.size
#        rect = Rectangle([bbox.x0/fig_size[0], bbox.y0/fig_size[1]], \
#            bbox.width/fig_size[0], bbox.height/fig_size[1], \
#            linewidth = 0.75, color = [0,0,0], fill = False, \
#            transform = self.mpl_fig.transFigure)
#        self.mpl_fig.patches.append(rect)
#        self.draw()

        return(bbox)     
    
    @property    
    def size(self):
        """
        Get/set the figure size in mm.  When changing the figure size, the 
        figure content is left the same size.
        """
        size = self.mpl_fig.get_size_inches() * 25.4
        return(size)
    
    #This method was created because matplotlib's fig.set_size_inches() 
    #automatically scales the content of the figure window.  Usually, we wish 
    #to change the figure window size while the figure content remains the 
    #same size.
    @size.setter
    def size(self, size):
        #Get the size of the figure before changing it
        #(The _np.copy() command is needed to keep the size data from updating
        #when we change the figure size.)
        old_fig_size = _np.copy(self.size)

        #Change the size of the figure
        size_inch = _np.array(size) / 25.4
        self.mpl_fig.set_size_inches(size_inch, forward = True)
        #We must do a draw() command because drawing can cause the figure 
        #window size to change slightly, so requests for the figure size
        #would be wrong.
        self.draw()
                
        #Scale the figure content back down to its original size
        
        #Get the current size of the figure window
        new_fig_size = self.size
        sf = new_fig_size / old_fig_size
        
        #Cycle through the figure content and scale them back down to their
        #original sizes
        for ax in self.mpl_fig.axes:
            pos = ax.get_position()
            ax.set_position([pos.x0 / sf[0], pos.y0 / sf[1], pos.width / sf[0], pos.height / sf[1]])     
         
        for text in self.mpl_fig.texts:
            pos = _np.array(text.get_position())
            text.set_position(pos / sf)
            
        for line in self.mpl_fig.lines:
            x = line.get_xdata()
            y = line.get_ydata()
            line.set_xdata(x / sf[0])
            line.set_ydata(y / sf[1])
        
        for patch in self.mpl_fig.patches:
            xy = patch.get_xy()
            patch.set_xy(xy / sf)
                
    def auto_adjust_layout(self, pad = _cp.params.auto_layout_pad):
        """
        If the figure size and axes positions have not been explicitly 
        specified, this method will resize the figure window and move the 
        content to center all the content inside the window.  If the content 
        positions within the window have been explicitly specified, then the 
        figure size will be adjusted, but the content positions relative to the
        lower left corner of the window will remain the same.
        
        Parameters
        ----------
        pad : float
            Padding on edges of figure, in mm.
        """
        #Only adjust figure if the size has not been specified
        if self._ui_size is 'auto':
            fig_bbox = self.tight_bbox
            #Collect the user input axes positions
            ui_ax_pos_auto = []
            for ax in self.axes:
                ui_ax_pos_auto.append(ax._ui_pos is 'auto')
            #Treat the colorbars as if they were axes
            for bar in self.color_bars:
                ui_ax_pos_auto.append(bar._ui_pos is 'auto')
            if False not in ui_ax_pos_auto:
                #If the axes positions have not been specified then move the 
                #axes all by the same amount, and resize the figure window.
                dx = - _np.array([fig_bbox.x0 - pad, fig_bbox.y0 - pad])
                for ax in self.axes:
                    ax.position = ax.position + dx
                for bar in self.color_bars:
                    bar.position = bar.position + dx
                self.size = [fig_bbox.width + 2*pad, fig_bbox.height + 2*pad]
            else:
                #If any of the axes positions have been specified, then just
                #resize the figure window.  This may end up with content far
                #off center, or even outside of the figure window area.
                self.size = [fig_bbox.x0 + fig_bbox.width + 2*pad, \
                    fig_bbox.y0 + fig_bbox.height + 2*pad]
    
    def draw(self):
        """
        Convenience method that draws all the content in the figure 
        window.
        """
        self.mpl_fig.canvas.draw()
    
    def update(self):
        """
        Convenience method that draws any object that has been added to the
        the figure window.
        """
        try:
            self.mpl_fig.canvas.update()
        except:
            self.mpl_fig.canvas.draw()    

    #This method is just a wrapper around the matplotlib fig.savefig() method
    #It allows the user to work in mm instead of inches, and implements many
    #of the defaults clearplot typically uses.
    def save(self, file_name, dpmm = _cp.params.dpmm, face_color = 'w', \
        edge_color = 'w', transparent = True, bbox = None, pad = 0, \
        frame_on = False):
        """
        Save the current figure.

        Parameters
        ----------
        file_name : string
            A string containing a path to a filename.
            If `format` is ``None`` and `filename` is a string, the output
            format is deduced from the extension of the filename. If
            the filename has no extension, the value of the rc parameter
            ``savefig.format`` is used.
        dpmm : [ None | float > 0 ]
            The resolution in dots per mm.
        face_color : [string | RGB color]
            The color of the figure background
        edge_color : [string | RGB color]
            The color of the figure border
        transparent : bool
            If *True*, the axes patches will all be transparent; the
            figure patch will also be transparent unless facecolor
            and/or edgecolor are specified via kwargs.
            This is useful, for example, for displaying
            a plot on top of a colored background on a web page.  The
            transparency of these patches will be restored to their
            original values upon exit of this function.
        bbox : bounding box object
            Bounding box of the region to be saved, in mm.  If 'tight', then 
            matplotlib will try to figure out the tightest bounding box that
            contains the figure content.  If ``None``, then the figure window 
            will be saved as is.
        pad : float
            Amount of padding around the figure when `bbox` is 'tight'.
        frame_on : bool
            If *True*, the figure patch will be colored, if *False*, the
            figure background will be transparent.  If not provided, the
            rcParam 'savefig.frameon' will be used.
        """
        if bbox is None or bbox == 'tight':
            bbox_inch = bbox
        else:
            bbox_inch = _np.array(bbox) / 25.4
        
        self.mpl_fig.savefig(file_name, dpi = dpmm * 25.4, \
            face_color = face_color, edge_color = edge_color, \
            transparent = transparent, bbox_inches = bbox_inch, \
            pad_inch = pad * 25.4, frame_on = frame_on)
            
    def close(self):
        """
        Closes the figure window
        """
        _plt.close(self.mpl_fig)
        