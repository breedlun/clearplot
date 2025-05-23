# -*- coding: utf-8 -*-
#Created on Wed Sep 24 21:26:51 2014
#@author: Benjamin Reedlunn

import clearplot as _cp
from clearplot import figure as _figure
import matplotlib as _mpl
import numpy as _np
from clearplot import utilities as _utl

def _setup_plot(x_label, y_label, **kwargs):
    """
    Read standard kwargs from plot functions and apply them
    """
    #Set default values for arguments not passed into the axes plot methods
    x_lim = kwargs.pop('x_lim', [None, None])
    y_lim = kwargs.pop('y_lim', [None, None])
    x_tick = kwargs.pop('x_tick', None)
    y_tick = kwargs.pop('y_tick', None)
    x_scale = kwargs.pop('x_scale', 'linear')
    y_scale = kwargs.pop('y_scale', 'linear')
    scale_plot = kwargs.pop('scale_plot', 1)
    font_size = kwargs.pop('font_size', _mpl.rcParams['font.size'])
    fig = kwargs.pop('fig', None)
    ax_pos = kwargs.pop('ax_pos', None)
    
    if fig == None:
        fig = _figure.Figure()
    ax = fig.add_axes(position = ax_pos, scale_plot = scale_plot, \
        font_size = font_size)
    ax.x_scale = x_scale
    ax.y_scale = y_scale
    ax._ui_x_lim = x_lim
    ax._ui_x_tick = x_tick
    ax._ui_y_lim = y_lim
    ax._ui_y_tick = y_tick
    ax.x_label = x_label
    ax.y_label = y_label
#    #Make sure the axis labels are in the correct format
#    x_label = _utl.adjust_depth(x_label, 1)
#    y_label = _utl.adjust_depth(y_label, 1)
#    x_label = (x_label + [None, None])[0:2]
#    y_label = (y_label + [None, None])[0:2]
#    #Create the axis labels
#    if isinstance(x_label[0], str):
#        ax.label_x(x_label[0], x_label[1])
#    if isinstance(y_label[0], str):
#        ax.label_y(y_label[0], y_label[1])
    return(fig, ax, kwargs)

def plot(filename, x, y, labels = [None], \
    x_label = None, y_label = None, **kwargs):
    """
    Plot the x and y data as 2D curves.
    
    Parameters
    ----------
    filename : string
        File name for the plot output file.  A file extension supported by 
        matplotlib, such as '.png', can be appended to the file name to 
        override the default file type.  To skip creating an output file, 
        input '' for `filename`.
    x : list of numpy arrays
        x coordinates of the data to be plotted.  Each list element should be 
        a 1-D numpy array.
    y : list of numpy arrays
        y coordinates of the data to be plotted.  Same structure as the `x` 
        input.
    labels : list, optional
        Specifies LaTeX strings to label the curves.  The list should be 1xQ, 
        where Q is the number of curves.
    x_label : list of strings, optional
        x-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units.  
    y_label : list of strings, optional
        y-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units. 
    x_lim : 1x2 list, optional
        x-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    y_lim : list, optional
        y-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    x_tick : float or int, optional
        Tick mark spacing for the x-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    y_tick : list, optional
        Tick mark spacing for the y-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    x_scale : [ 'linear' | 'log' ], optional
        x-axis scaling.  The default is 'linear'.
    y_scale : [ 'linear' | 'log' ], optional
        y-axis scaling.  The default is 'linear'.
    legend : bool, optional
        Specifies whether to display a legend for the curves.
    legend_loc : 1x2 list or string, optional
        Legend location.  For the proper syntax, see the axes.add_legend() 
        documentation for the legend 'loc' keyword argument.
    legend_kwargs : dict, optional
        Keyword arguments to customize the legend appearance.  This is passed 
        directly into the matplotlib legend function.  See the matplotlib 
        documentation further details.
    scale_plot : float, optional
        Changes the size of the entire plot, but leaves the font sizes the 
        same.
    font_size : float, optional
        Font size (in points) of the text in the plot.
    fig : figure object, optional
        Figure window to place the plot in.  The default behavior is to place 
        the plot in a new, dedicated, figure window.
    ax_pos : 1x2 list of floats, optional
        Position (in mm) of the lower left corner of the data axes, relative 
        to the lower left corner of the figure window.  (For reference, the 
        default distance between tick marks is 20 mm.)
        
    Other Parameters
    ----------------
    See parameters in Axes.plot()
    
    Returns
    -------
    fig : figure object
        Figure object containing the plot.
    ax : axes object
        Axes object containing the data.
    curves: list
        Curve objects
        
    See Also
    --------
    plot_functions.plot_markers()
    """
    legend = kwargs.pop('legend', None)
    legend_loc = kwargs.pop('legend_loc', 'best')
    legend_kwargs = kwargs.pop('legend_kwargs', dict())

    [fig, ax, kwargs] = _setup_plot(x_label, y_label, **kwargs)
    
    ax.plot(x, y, labels = labels, **kwargs)
    
    #Generate legend
    if legend == None:
        if len(x) > 1 and labels != [None]:
            legend = True
        else:
            legend = False 
    if legend:
        ax.add_legend(loc = legend_loc, **legend_kwargs)

#    # Catch unexpected keyword arguments
#    if kwargs:
#        raise TypeError("%r are invalid keyword arguments" % (kwargs.keys()))

    #Update canvas
    fig.auto_adjust_layout()

    #Only save data if a filename has been given
    if filename != '':
        fig.save(filename)
        
    return(fig, ax, ax.curves)
    
def plot_markers(filename, x, y, labels = [None], \
    x_label = None, y_label = None, **kwargs):
    """
    Plot the x and y data as markers (a scatterplot).
    
    Parameters
    ----------
    filename : string
        File name for the plot output file.  A file extension supported by 
        matplotlib, such as '.png', can be appended to the file name to 
        override the default file type.  To skip creating an output file, 
        input '' for `filename`.
    x : list of numpy arrays
        x coordinates of the data to be plotted.  Each list element should be 
        a 1-D numpy array.
    y : list of numpy arrays
        y coordinates of the data to be plotted.  Same structure as the `x` 
        input
    labels : list, optional
        Specifies LaTeX strings to label the marker.  The list should be 1xQ, 
        where Q is the number of curves.
    x_label : list of strings, optional
        x-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units.  
    y_label : list of strings, optional
        y-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units. 
    x_lim : 1x2 list, optional
        x-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    y_lim : list, optional
        y-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    x_tick : float or int, optional
        Tick mark spacing for the x-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    y_tick : list, optional
        Tick mark spacing for the y-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    x_scale : [ 'linear' | 'log' ], optional
        x-axis scaling.  The default is 'linear'.
    y_scale : [ 'linear' | 'log' ], optional
        y-axis scaling.  The default is 'linear'.
    legend : bool, optional
        Specifies whether to display a legend for the curves.
    legend_loc : 1x2 list or string, optional
        Legend location.  For the proper syntax, see the axes.add_legend() 
        documentation for the legend 'loc' keyword argument.
    legend_kwargs : dict, optional
        Keyword arguments to customize the legend appearance.  This is passed 
        directly into the matplotlib legend function.  See the matplotlib 
        documentation further details.
    scale_plot : float, optional
        Changes the size of the entire plot, but leaves the font sizes the 
        same.
    font_size : float, optional
        Font size (in points) of the text in the plot.
    fig : figure object, optional
        Figure window to place the plot in.  The default behavior is to place 
        the plot in a new, dedicated, figure window.
    ax_pos : 1x2 list of floats, optional
        Position (in mm) of the lower left corner of the data axes, relative 
        to the lower left corner of the figure window.  (For reference, the 
        default distance between tick marks is 20 mm.)
        
    Other Parameters
    ----------------
    See parameters in Axes.plot_markers()
    
    Returns
    -------
    fig : figure object
        Figure object containing the plot.
    ax : axes object
        Axes object containing the data.
    markers: list
        Marker objects
        
    See Also
    --------
    plot_functions.plot()
    """
    legend = kwargs.pop('legend', None)
    legend_loc = kwargs.pop('legend_loc', 'best')
    legend_kwargs = kwargs.pop('legend_kwargs', dict())

    [fig, ax, kwargs] = _setup_plot(x_label, y_label, **kwargs)
    
    ax.plot_markers(x, y, labels = labels, **kwargs)
    
    #Generate legend
    if legend == None:
        if len(x) > 1 and labels != [None]:
            legend = True
        else:
            legend = False 
    if legend:
        ax.add_legend(loc = legend_loc, **legend_kwargs)

#    # Catch unexpected keyword arguments
#    if kwargs:
#        raise TypeError("%r are invalid keyword arguments" % (kwargs.keys()))

    #Update canvas
    fig.auto_adjust_layout()

    #Only save data if a filename has been given
    if filename != '':
        fig.save(filename)
        
    return(fig, ax, ax.markers)

def plot_bars(filename, x, y, labels = [None], \
    x_label = None, y_label = None, **kwargs):
    """
    Plot the x and y data as a series of vertical bars
    
    Parameters
    ----------
    filename: string
        File name for the plot output file.  A file extension supported by 
        matplotlib, such as '.jpg', can be appended to the file name to 
        override the default file type.  To skip creating an output file, 
        input '' for `filename`.
    x : 1xN list of numpy arrays
        x coordinates of bars
    y : 1xN list of numpy arrays
        Height of bars
    labels : list, optional
        Specifies LaTeX strings to label the curves.  The list should be 1xQ, 
        where Q is the number of curves.
    x_label : list of strings, optional
        x-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units.  
    y_label : list of strings, optional
        y-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units. 
    x_lim : 1x2 list, optional
        x-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    y_lim : list, optional
        y-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    x_tick : float or int, optional
        Tick mark spacing for the x-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    y_tick : list, optional
        Tick mark spacing for the y-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    x_scale : [ 'linear' | 'log' ], optional
        x-axis scaling.  The default is 'linear'.
    y_scale : [ 'linear' | 'log' ], optional
        y-axis scaling.  The default is 'linear'.
    legend : bool, optional
        Specifies whether to display a legend for the bars.
    legend_loc : 1x2 list or string, optional
        Legend location.  For the proper syntax, see the axes.add_legend() 
        documentation for the legend 'loc' keyword argument.
    legend_kwargs : dict, optional
        Keyword arguments to customize the legend appearance.  This is passed 
        directly into the matplotlib legend function.  See the matplotlib 
        documentation further details.
    scale_plot : float, optional
        Changes the size of the entire plot, but leaves the font sizes the 
        same.
    font_size : float, optional
        Font size (in points) of the text in the plot.
    fig : figure object, optional
        Figure window to place the plot in.  The default behavior is to place 
        the plot in a new, dedicated, figure window.
    ax_pos : 1x2 list of floats, optional
        Position (in mm) of the lower left corner of the data axes, relative 
        to the lower left corner of the figure window.  (For reference, the 
        default distance between tick marks is 20 mm.)
        
    Other Parameters
    ----------------    
    See parameters in Axes.plot_bars()
    
    Returns
    -------
    fig : figure object
        Figure object containing the plot.
    ax : axes object
        Axes object containing the data.
    bars: list
        Bar objects
    """
    legend = kwargs.pop('legend', None)
    legend_loc = kwargs.pop('legend_loc', 'best')
    legend_kwargs = kwargs.pop('legend_kwargs', dict())

    [fig, ax, kwargs] = _setup_plot(x_label, y_label, **kwargs)
    
    ax.plot_bars(x, y, labels = labels, **kwargs)
    
    #Generate legend
    if legend == None:
        if len(x) > 1 and labels != [None]:
            legend = True
        else:
            legend = False 
    if legend:
        ax.add_legend(loc = legend_loc, **legend_kwargs)

    #Update canvas
    fig.auto_adjust_layout()

    #Only save data if a filename has been given
    if filename != '':
        fig.save(filename)
        
    return(fig, ax, ax.bars)

def plot_box_and_whiskers(filename, x, y, \
    x_label = None, y_label = None, **kwargs):
    """
    Make a box and whisker plot from the x and y data
    
    Parameters
    ----------
    filename: string
        File name for the plot output file.  A file extension supported by 
        matplotlib, such as '.jpg', can be appended to the file name to 
        override the default file type.  To skip creating an output file, 
        input '' for `filename`.
    x : 1xN list of numpy arrays
        x coordinates of boxes
    y : 1xN list of numpy arrays
        Distributions of data
    x_label : list of strings, optional
        x-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units.  
    y_label : list of strings, optional
        y-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units. 
    x_lim : 1x2 list, optional
        x-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    y_lim : list, optional
        y-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    x_tick : float or int, optional
        Tick mark spacing for the x-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    y_tick : list, optional
        Tick mark spacing for the y-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    x_scale : [ 'linear' | 'log' ], optional
        x-axis scaling.  The default is 'linear'.
    y_scale : [ 'linear' | 'log' ], optional
        y-axis scaling.  The default is 'linear'.
    scale_plot : float, optional
        Changes the size of the entire plot, but leaves the font sizes the 
        same.
    font_size : float, optional
        Font size (in points) of the text in the plot.
    fig : figure object, optional
        Figure window to place the plot in.  The default behavior is to place 
        the plot in a new, dedicated, figure window.
    ax_pos : 1x2 list of floats, optional
        Position (in mm) of the lower left corner of the data axes, relative 
        to the lower left corner of the figure window.  (For reference, the 
        default distance between tick marks is 20 mm.)

    Other Parameters
    ----------------    
    See parameters in Axes.plot_box_and_whiskers()    
    
    Returns
    -------
    fig : figure object
        Figure object containing the plot.
    ax : axes object
        Axes object containing the data.
    boxes : list
        Box objects
    """

    [fig, ax, kwargs] = _setup_plot(x_label, y_label, **kwargs)
    
    ax.plot_box_and_whiskers(x, y, **kwargs)
    
    #Update canvas
    fig.auto_adjust_layout()

    #Only save data if a filename has been given
    if filename != '':
        fig.save(filename)
        
    return(fig, ax, ax.boxes)

def plot_violins(filename, x, y, x_label = None, y_label = None, **kwargs):
    """
    Make a violin plot from the x and y data
    
    Parameters
    ----------
    x : 1xN list of numpy arrays
        x coordinates of violins
    y : 1xN list of numpy arrays
        Distributions of data
    x_label : list of strings, optional
        x-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units.  
    y_label : list of strings, optional
        y-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units. 
    x_lim : 1x2 list, optional
        x-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    y_lim : list, optional
        y-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    x_tick : float or int, optional
        Tick mark spacing for the x-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    y_tick : list, optional
        Tick mark spacing for the y-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    x_scale : [ 'linear' | 'log' ], optional
        x-axis scaling.  The default is 'linear'.
    y_scale : [ 'linear' | 'log' ], optional
        y-axis scaling.  The default is 'linear'.
    scale_plot : float, optional
        Changes the size of the entire plot, but leaves the font sizes the 
        same.
    font_size : float, optional
        Font size (in points) of the text in the plot.
    fig : figure object, optional
        Figure window to place the plot in.  The default behavior is to place 
        the plot in a new, dedicated, figure window.
    ax_pos : 1x2 list of floats, optional
        Position (in mm) of the lower left corner of the data axes, relative 
        to the lower left corner of the figure window.  (For reference, the 
        default distance between tick marks is 20 mm.)

    Other Parameters
    ----------------    
    See parameters in Axes.plot_violins()
    
    Returns
    -------
    fig : figure object
        Figure object containing the plot.
    ax : axes object
        Axes object containing the data.
    violins : list
        Violin objects
    """
    [fig, ax, kwargs] = _setup_plot(x_label, y_label, **kwargs)
    
    ax.plot_violins(x, y, **kwargs)

    #Update canvas
    fig.auto_adjust_layout()

    #Only save data if a filename has been given
    if filename != '':
        fig.save(filename)
        
    return(fig, ax, ax.violins)

def plot_intensity_map(filename, x, y, z, x_label = None, y_label = None, **kwargs):
    """
    Plots a intensity map (heat map) as an image.
    
    Parameters
    ----------
    filename: string
        File name for the plot output file.  A file extension supported by 
        matplotlib, such as '.jpg', can be appended to the file name to 
        override the default file type.  To skip creating an output file, 
        input '' for `filename`.
    x : 1x2 or MxN numpy array
        Matrix x position.
    y : 1x2 or MxN numpy array
        Matrix y position.
    z : MxN numpy array
        Matrix to be plotted
    x_label : list of strings, optional
        x-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units.  
    y_label : list of strings, optional
        y-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units. 
    x_lim : 1x2 list, optional
        x-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    y_lim : list, optional
        y-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    x_tick : float or int, optional
        Tick mark spacing for the x-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    y_tick : list, optional
        Tick mark spacing for the y-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    c_bar : boolean, optional
        Specifies whether or not to place a color bar in the figure window.
    c_map : matplotlib colormap object, optional
        If "im" array is MxN, then the array values are mapped to a certain 
        color (or gray value) using the supplied colormap.
    c_lim : 1x2 list, optional
        Colormap limits.  The first element should be the lower limit, while 
        the second element should be the upper limit.  Alternatively, either 
        element may None to have the algorithm automatically select the limits.
    c_tick : float, optional
        Tick mark spacing for the color bar.  Alternatively, input None to 
        have the algorithm automatically select the tick mark spacing.
    c_orient : the string 'h' or 'v', optional
        Orientation of the color bar.  The default is a vertical orientation.
    c_label : list, optional
        Color bar label.  The first list element is the color bar variable 
        being plotted, while the second element is the color bar units.  Both 
        strings should be in LaTeX syntax. The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units.
    c_scale : [ 'linear' | 'log' ], optional
        Color bar scaling.  The default is 'linear'.
    scale_plot : float, optional
        Changes the size of the entire plot, but leaves the font sizes the 
        same.
    font_size : float, optional
        Font size (in points) of the text in the plot.
    fig : figure object, optional
        Figure window to place the plot in.  The default behavior is to place 
        the plot in a new, dedicated, figure window.
    ax_pos : 1x2 list of floats, optional
        Position (in mm) of the lower left corner of the data axes, relative 
        to the lower left corner of the figure window.  (For reference, the 
        default distance between tick marks is 20 mm.)

    Other Parameters
    ----------------    
    See parameters in Axes.plot_matrix()    
    
    Returns
    -------
    fig : figure object
        Figure object containing the plot.
    ax : axes object
        Axes object containing the data.
    im : image object
        Matrix plotted as an image
    """
    
    #Set default values
    c_bar = kwargs.pop('c_bar', True)
    c_orient = kwargs.pop('c_orient', 'v')
    c_label = kwargs.pop('c_label', None)
    c_tick = kwargs.pop('c_tick', None)
    c_lim = kwargs.pop('c_lim', [None, None])
    c_scale = kwargs.pop('c_scale', 'linear')
    
    [fig, ax, kwargs] = _setup_plot(x_label, y_label, **kwargs)
    
    im = ax.plot_intensity_map(x, y, z, c_scale = c_scale, c_lim = c_lim, **kwargs)
    
    if c_bar:
        #Place color bar
        c_bar = fig.add_color_bar(im, label = c_label, tick = c_tick, \
            lim = c_lim, orient = c_orient, scale = c_scale)

    #Update figure
    fig.auto_adjust_layout()
    
    #Only save data if a filename has been given
    if filename != '':
        fig.save(filename)
        
    return(fig, ax, im)

def plot_contours(filename, x, y, z, x_label = None, y_label = None, **kwargs):
    """
    Create a contour plot from the x, y, and z data.
    
    Parameters
    ----------
    filename: string
        File name for the plot output file.  A file extension supported by 
        matplotlib, such as '.jpg', can be appended to the file name to 
        override the default file type.  To skip creating an output file, 
        input '' for `filename`.
    x: 2-D numpy array
        x coordinates of the data to be plotted.
    y: 2-D numpy array
        y coordinates of the data to be plotted.  `y` must have the same shape 
        as `x`.
    z: 2-D numpy array
        z coordinates of the data to be plotted.  `z` must have the same shape 
        as `x`.
    x_label : list of strings, optional
        x-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units.  
    y_label : list of strings, optional
        y-axis label.  The first list element is the axis variable being 
        plotted, while the second element is the axis units.  Both strings 
        should be in LaTeX syntax.  The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units. 
    x_lim : 1x2 list, optional
        x-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    y_lim : list, optional
        y-axis limits.  The first list element is the lower limit, while the 
        second element is the upper limit.  Alternatively, either element may 
        be None to have the algorithm automatically select the limits.
    x_tick : float or int, optional
        Tick mark spacing for the x-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    y_tick : list, optional
        Tick mark spacing for the y-axis.  Alternatively, input None to have 
        the algorithm automatically select the tick mark spacing.
    c_bar : boolean, optional
        Specifies whether or not to place a color bar in the figure window.
    c_map : matplotlib colormap object, optional
        If "im" array is MxN, then the array values are mapped to a certain 
        color (or gray value) using the supplied colormap.
    c_lim : 1x2 list, optional
        Colormap limits.  The first element should be the lower limit, while 
        the second element should be the upper limit.  Alternatively, either 
        element may be None to have the algorithm automatically select the 
        limits.
    c_tick : float, optional
        Tick mark spacing for the color bar.  Alternatively, input None to 
        have the algorithm automatically select the tick mark spacing.
    c_orient : the string 'h' or 'v', optional
        Orientation of the color bar.  The default is a vertical orientation.
    c_label : list, optional
        Color bar label.  The first list element is the color bar variable 
        being plotted, while the second element is the color bar units.  Both 
        strings should be in LaTeX syntax. The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units.
    c_scale : [ 'linear' | 'log' ], optional
        Color bar scaling.  The default is 'linear'.
    scale_plot : float, optional
        Changes the size of the entire plot, but leaves the font sizes the 
        same.
    font_size : float, optional
        Font size (in points) of the text in the plot.
    fig : figure object, optional
        Figure window to place the plot in.  The default behavior is to place 
        the plot in a new, dedicated, figure window.
    ax_pos : 1x2 list of floats, optional
        Position (in mm) of the lower left corner of the data axes, relative 
        to the lower left corner of the figure window.  (For reference, the 
        default distance between tick marks is 20 mm.)

    Other Parameters
    ----------------    
    See parameters in Axes.plot_contours()    
    
    Returns
    -------
    fig : figure object
        Figure object containing the plot.
    ax : axes object
        Axes object containing the data.
    bg : contour background
        Background of contour plot
    cl : contour lines
        Contour lines
    """
    
    #Set default values
    plot_type = kwargs.get('plot_type', 'filled')
    c_bar = kwargs.pop('c_bar', True)
    c_orient = kwargs.pop('c_orient', 'v')
    c_label = kwargs.pop('c_label', None)
    c_tick = kwargs.pop('c_tick', None)
    c_scale = kwargs.pop('c_scale', 'linear')
    
    [fig, ax, kwargs] = _setup_plot(x_label, y_label, **kwargs)
    
    [bg, cl] = ax.plot_contours(x, y, z, c_scale = c_scale, **kwargs)
    
    if c_bar:
        if plot_type == 'lines':
            c_obj = cl
        else:
            c_obj = bg
        #Place color bar
        c_bar = fig.add_color_bar(c_obj, label = c_label, tick = c_tick, \
            orient = c_orient, scale = c_scale)

    #Update figure
    fig.auto_adjust_layout()
    
    #Only save data if a filename has been given
    if filename != '':
        fig.save(filename)
        
    return(fig, ax, bg, cl)

def show_im(filename, im_seq, **kwargs):
    """
    Displays an image or a sequence of images.  
    
    Parameters
    ----------
    filename : string
        File name for the plot output file.  A file extension supported by 
        matplotlib, such as '.jpg', can be appended to the file name to 
        override the default file type.  To skip creating an output file, 
        input '' for `filename`.
    im_seq : list of lists containing MxN or MxNx3 arrays
        A list of images sequences.  The list should be 1xA, where A is the 
        number of image sequences.  Each image sequence is a 1xC list, where C 
        is the number of images in the sequence.  (Images within a sequence are 
        displayed side by side, while sequences have a small space between 
        them.) Each element in the image sequence list should be a MxN or 
        MxNx3 array.  If image shapes are MxN, the array values are 
        interpreted as intensities that are mapped using the specified color 
        map.  If the shapes are MxNx3, then the array values are treated as 
        RGB values.
    scale_im : float, optional
        Scales the images, holding the aspect ratio fixed.  If left 
        unspecified the algorithm will attempt to pick the proper value.  If 
        the image sequence is smaller than the screen resolution, then images 
        will be displayed at full scale.  Otherwise, the images will be scaled 
        down to fit within the screen resolution.
    scale_gap : float, optional
        Scales the size of the gap between continuous image sequences
    im_origin : string, optional
        Origin for the image indices.  If 'upper left' is input, then the 
        [0,0] index is the upper left of the image, with positive y being
        downwards.  If 'lower left' is input, then the [0,0] index is the 
        lower left of the image, with positive y being upwards.
    im_interp : string, optional
        Image interpolation method.  See matplotlib documentation for 
        acceptable values.
    c_bar : boolean, optional
        Specifies whether or not to place a color bar in the figure window.
    c_map : matplotlib colormap object, optional
        If "im" array is MxN, then the array values are mapped to a certain 
        color (or gray value) using the supplied colormap.
    c_lim : 1x2 list, optional
        Colormap limits.  The first element should be the lower limit, while 
        the second element should be the upper limit.  Alternatively, either 
        element may be None to have the algorithm automatically select the 
        limits.
    c_tick : float, optional
        Tick mark spacing for the color bar.  Alternatively, input None to 
        have the algorithm automatically select the tick mark spacing.
    c_orient : the string 'h' or 'v', optional
        Orientation of the color bar.  The default is a vertical orientation.
    c_label : list, optional
        Color bar label.  The first list element is the color bar variable 
        being plotted, while the second element is the color bar units.  Both 
        strings should be in LaTeX syntax. The units get automatically wrapped
        in parentheses.  Input a 1x1 list to supply a variable without any 
        units. 
    b_labels : bool, optional
        Specifies whether or not to label images with circled numbers 
        (balloons)
    scale_plot : float, optional
        Changes the size of the entire plot, but leaves the font sizes the 
        same.
    font_size : float, optional
        Font size (in points) of the text in the plot.
    fig : figure object, optional
        Figure window to place the plot in.  The default behavior is to place 
        the plot in a new, dedicated, figure window.
    ax_pos : 1x2 list of floats, optional
        Position (in mm) of the lower left corner of the data axes, relative 
        to the lower left corner of the figure window.  (For reference, the 
        default distance between tick marks is 20 mm.)
    
    Returns
    -------
    fig : figure object
        Figure object containing the plot.
    ax : axes object
        Axes object containing the data. 
    im_obj : image object
        Image object containing the image data
        
    See Also
    --------
    Axes.add_image() : Places an image on a set of x-y axes
    """
    
    #Set default values
    scale_im = kwargs.pop('scale_im', None)
    scale_gap = kwargs.pop('scale_gap', 1)
    scale_plot = kwargs.pop('scale_plot', 1)
    c_bar = kwargs.pop('c_bar', False)
    c_map = kwargs.pop('c_map', _cp.colors.c_maps['rainbow'])
    c_lim = kwargs.pop('c_lim', [None, None])
    c_tick = kwargs.pop('c_tick', None)
    c_orient = kwargs.pop('c_orient', 'v')
    c_label = kwargs.pop('c_label', ['c\_label'])
    b_labels = kwargs.pop('b_labels', False)
    im_interp = kwargs.pop('im_interp', None)
    im_origin = kwargs.pop('im_origin', 'upper')
    font_size = kwargs.pop('fsize', _mpl.rcParams['font.size'])
    fig = kwargs.pop('fig', None)
    ax_pos = kwargs.pop('ax_pos', None)
    if kwargs:
        # Catch unexpected keyword arguments
        raise TypeError("%r are invalid keyword arguments" % (kwargs.keys()))
    
    #Put the image sequences in the proper nested list format
    im_seqs = _utl.adjust_list_depth(im_seq, 2)
    
    #Define a scaling dimension for the plot.  This dimension is used in a 
    #number of places to scale the distances between different objects.  Under 
    #default settings, the scaling dimension corresponds to the number of 
    #millimeters between tick marks.  
    sdim = 20.0 * scale_plot
    #Define the gap between image sequences (in mm)
    gap = sdim / 4.0 * scale_gap
    #Find the sizes of the images and each continuous row of images
    im_sizes = []
    im_seq_sizes = _np.zeros([len(im_seqs), 2])
    for i, im_seq in enumerate(im_seqs):
        im_sizes.append(_np.zeros([len(im_seq), 2]))
        for j, im in enumerate(im_seq):
            #Store the size of each image 
            #(I am only using the first two outputs from shape in case the 
            #image is in RGB format.  The [::-1] causes the ouput from shape 
            #switch the number of rows and columns so that data is in 
            #(width, height) form.
            im_sizes[i][j,:] = im.shape[0:2][::-1]
        #Store the size of each continuous row of images
        im_seq_sizes[i,:] = [_np.sum(im_sizes[i][:,0]), _np.max(im_sizes[i][:,1])]
    
    if scale_im == None:
        #If image resolution (+ margins and padding) is smaller than the 
        #computer screen resolution, then just display image as is.  Otherwise, 
        #scale it down.
        #Get screen dimensions.
        try:
            from PySide import QtGui
        except:
            raise IOError("ERROR: auto scaling of images is currently only supported with PySide.  Please explicitly specify image scaling.")
        screen_rect = QtGui.qApp.desktop().screenGeometry()    
        scale_im_width = (screen_rect.width() \
            - ((len(im_seqs)-1) * gap + ax_pos[0]*2) * _cp.params.dpmm) \
            / _np.sum(im_seq_sizes[:,0])
        scale_im_height = (screen_rect.height() - ax_pos[1]*2 * _cp.params.dpmm) \
            / _np.max(im_seq_sizes[:,1])
        #Figure out which dimension constrains things
        if scale_im_width < scale_im_height:
            scale_im = scale_im_width
        else:
            scale_im = scale_im_height
        #Chose whether to scale the image
        if scale_im > 1:
            scale_im = 1
        else:
            print('Images scaled by %.3f to fit on screen' %(scale_im))
    #Define image axes width and height (in inches)
    ax_size = _np.array([_np.sum(im_seq_sizes[:,0]), \
        _np.max(im_seq_sizes[:,1])]) * scale_im / _cp.params.dpmm
    ax_size[0] = ax_size[0] + (len(im_seqs)-1) * gap
    #Calculate the gap between image sequences in image pixels
    pix_gap = gap * _cp.params.dpmm / scale_im
    #Make image axes coordinates coorespond to image pixels
    ax_lim = []
    ax_lim.append([0, _np.sum(im_seq_sizes[:,0]) + (len(im_seqs)-1) * pix_gap])
    ax_lim.append([0, _np.max(im_seq_sizes[:,1])])    
    
    #Generate image axes
    #Create figure window
    if fig is None:
        fig = _figure.Figure()
    #Generate the image axes      
    im_ax = fig.add_invisible_axes(size = ax_size, position = ax_pos)
    #Set the limits
    im_ax.x_lim = ax_lim[0]
    im_ax.y_lim = ax_lim[1]

    #Define the position of the lower left corner of the first image wrt the 
    #image axes
    x0 = 0   
    y0 = 0
    #Initialize the balloon label counter
    k = 0
    #Define the gap between the balloon labels and the images 
    #(in normalized axes coordinates)
    label_gap_nac = sdim * 0.35 / ax_size[1]
    #As of matplotlib 1.5.0, you can specify the padding for circles.  Earlier 
    #versions cannot.
    if _cp.mpl_version < (1,5,0):
        l_bbox = dict(boxstyle='circle', fc = 'none') 
    else:   
        l_bbox = dict(boxstyle='circle', fc = 'none', pad = 0.2) 
    #Define a list to store the image objects
    im_obj = []
    for i, im_seq in enumerate(im_seqs):
        for j, im in enumerate(im_seq):
            #Define the position of the upper right corner of the image wrt the
            #image axes
            x1 = x0 + im_sizes[i][j,0]
            y1 = y0 + im_sizes[i][j,1]
            #Place image
            im_obj.append(im_ax.add_image(im, x = [x0, x1], y = [y0, y1], \
                c_map = c_map, origin = im_origin, c_lim = c_lim, \
                im_interp = im_interp))
            if b_labels:
                #Increment the balloon number by one
                k = k + 1
                #Create the balloon label
                #(Place the x coordinate wrt data coordinates, place the y 
                #coordinate wrt normalized image axes coordinates)
                im_ax.annotate('%r' %(k), [(x0 + x1)/2.0, 1 + label_gap_nac], \
                    ['data', 'axes fraction'], \
                    size = font_size * scale_plot, \
                    va = 'center', ha = 'center', \
                    fontname = 'sans-serif', bbox=l_bbox)
            x0 = x1
        #Put a gap between each image sequence
        x0 = x0 + pix_gap
        
    if c_bar:
        #Place color bar
        c_bar = fig.add_color_bar(im_obj[0], \
            label = c_label, lim = c_lim, tick = c_tick, orient = c_orient)

    #Update canvas
    fig.auto_adjust_layout() 
    
    #Only save data if a filename has been given
    if filename != '':
        fig.save(filename)
#        #Save any rasterized images at full resolution
#        if scale_im <= 1.0:
#            save_dpmm = _cp.params.dpmm / scale_im
#        else:
#            save_dpmm = _cp.params.dpmm
#        fig.save(filename, dpmm = save_dpmm)
        
    return(fig, im_ax, im_obj)        

def plot_surface(filename, x, y, z, x_label='x', y_label='y', z_label='z', \
    x_lim = [None,None], y_lim = [None,None], z_lim = [None,None],\
    x_tick = None, y_tick = None, z_tick = None, \
    light_alt_angle = 0.0, light_azm_angle = 90.0, \
    view_alt_angle = 20.0, view_azm_angle = 30.0, title = 'None', \
    c_map = _cp.colors.c_maps['plain_red']):
    """
    Plots a 3D surface.  In development...
    """    
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Line3D
    import matplotlib.colors as mplc
    
    fig = _figure.Figure(size = [160,160])
    
    #Collect data, limits, tick mark spacing, and axis labels into 
    #structured lists. This makes it easier to loop thru these structures.
    #(The reason I have x_lim[:] instead of x_lim is python passes lists by 
    #reference.  The [:] causes python to pass a copy.)
    xyz = [x, y, z]    
    ax_lim = [x_lim[:], y_lim[:], z_lim[:]]
    ax_tick = [x_tick, y_tick, z_tick]
    ax_label = [x_label, y_label, z_label]    

    #If the user did not specify axis limits or tick mark spacing, find an 
    #acceptable set of values for each axis.  Also find the number of ticks for
    #each axis
    N_tick = [0] * 3
    for a, (x, lim, tick) in enumerate(zip(xyz, ax_lim, ax_tick)):
        [ax_lim[a], ax_tick[a], N_tick[a]] = \
            _utl.find_and_select_lim_and_tick(lim, tick, lim, 'linear', 10.0, 0.0)
        
    axes3d = fig.mpl_fig.gca(projection = '3d')
    #Turn off autoscale so that the plot command does not alter the limits of 
    #the plot later
    axes3d.set_autoscale_on(False)
    #Label axes    
    axes3d.set_xlabel(ax_label[0])
    axes3d.set_ylabel(ax_label[1])
    axes3d.set_zlabel(ax_label[2])
    #Set axis limits (this is done after plotting the data because I found it 
    #does not work properly if you do it prior to plotting the data)
    tick_list = _np.arange(ax_lim[0][0], ax_lim[0][1]+ax_tick[0], ax_tick[0])
    axes3d.set_xlim(ax_lim[0])    
    axes3d.set_xticks(tick_list)
    tick_list = _np.arange(ax_lim[1][0], ax_lim[1][1]+ax_tick[1], ax_tick[1])    
    axes3d.set_ylim(ax_lim[1])     
    axes3d.set_yticks(tick_list)
    tick_list = _np.arange(ax_lim[2][0], ax_lim[2][1]+ax_tick[2], ax_tick[2])     
    axes3d.set_zlim(ax_lim[2])      
    axes3d.set_zticks(tick_list)
    #Draw dashed lines across plot if x axis spans zero 
    if _np.sign(ax_lim[0][0] + ax_tick[0]/10.0**12) != \
        _np.sign(ax_lim[0][1] - ax_tick[0]/10.0**12):
        l = Line3D([0.0,0.0], ax_lim[1], [0.0,0.0], \
            linestyle = '--', linewidth = 1, color = [0,0,0])                                    
        axes3d.add_line(l)
        l = Line3D([0.0,0.0], [0.0,0.0], ax_lim[2],\
            linestyle = '--', linewidth = 1, color = [0,0,0])                                    
        axes3d.add_line(l)
    #Draw dashed lines across plot if y axis spans zero 
    if _np.sign(ax_lim[1][0] + ax_tick[1]/10.0**12) != \
        _np.sign(ax_lim[1][1] - ax_tick[1]/10.0**12):
        l = Line3D(ax_lim[0], [0.0,0.0], [0.0,0.0], \
            linestyle = '--', linewidth = 1, color = [0,0,0])                                    
        axes3d.add_line(l)
        l = Line3D([0.0,0.0], [0.0,0.0], ax_lim[2],\
            linestyle = '--', linewidth = 1, color = [0,0,0])                                    
        axes3d.add_line(l)  
    
    #Specify the viewing angle 
    #(elev = angle above z plane, azim = angle about the z-axis)
    axes3d.view_init(elev=view_alt_angle, azim=view_azm_angle)
    # create light source object.
    #(I could not find any documentation on  on using a lightsource with a surface,
    #but the following forum post described what to do:
    #http://matplotlib.1069221.n5.nabble.com/Is-it-possible-to-have-different-color-for-inner-and-outer-face-of-a-3D-plot-td38979.html)
    #(altdeg = angle above z plane, azdeg = angle about the z-axis)
    ls = mplc.LightSource(azdeg=light_azm_angle, altdeg=light_alt_angle)
    illuminated_surf = ls.shade(xyz[2], cmap = c_map)
    surf = axes3d.plot_surface(xyz[0], xyz[1], xyz[2], \
        rstride=1, cstride=1, linewidth=0, antialiased=False, \
        facecolors = illuminated_surf)
        
    #Add Title
    if title != 'None':
        axes3d.set_title(title)
        
    if filename != '':
        fig.save(filename)

    return(fig, axes3d, surf)   
    
def plot_3d_scatter(filename, x, y, z, x_label='x', y_label='y', z_label='z', \
    x_lim = [None,None], y_lim = [None,None], z_lim = [None,None],\
    x_tick = None, y_tick = None, z_tick = None, \
    light_alt_angle = 0.0, light_azm_angle = 90.0, \
    view_alt_angle = 20.0, view_azm_angle = -25.0, title = 'None'):
    """
    Plots a 3D scatter plot.  In development...
    """    
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Line3D
    import matplotlib.colors as mplc
    
    fig = _figure.Figure()
    
    #Collect data, limits, tick mark spacing, and axis labels into 
    #structured lists. This makes it easier to loop thru these structures.
    #(The reason I have x_lim[:] instead of x_lim is python passes lists by 
    #reference.  The [:] causes python to pass a copy.)
    xyz = [x, y, z]    
    ax_lim = [x_lim[:], y_lim[:], z_lim[:]]
    ax_tick = [x_tick, y_tick, z_tick]
    ax_tick_list = [[],[],[]]
    ax_label = [x_label, y_label, z_label]    

    #If the user did not specify axis limits or tick mark spacing, find an 
    #acceptable set of values for each axis.  Also find the number of ticks for
    #each axis
    N_tick = [0] * 3
    for a, (x, lim, tick) in enumerate(zip(xyz, ax_lim, ax_tick)):
        [ax_lim[a], ax_tick[a], N_tick[a]] = \
            _utl.find_and_select_lim_and_tick(lim, tick, x, 'linear', 10, 0.02)
        
    axes3d = fig.mpl_fig.gca(projection = '3d')
    #Turn off autoscale so that the plot command does not alter the limits of 
    #the plot later
    axes3d.set_autoscale_on(False)
    #Label axes    
    axes3d.set_xlabel(ax_label[0])
    axes3d.set_ylabel(ax_label[1])
    axes3d.set_zlabel(ax_label[2])
    #Set axis limits (this is done after plotting the data because I found it 
    #does not work properly if you do it prior to plotting the data)
    tick_list = _np.arange(ax_lim[0][0], ax_lim[0][1]+ax_tick[0], ax_tick[0])
    axes3d.set_xlim(ax_lim[0])    
    axes3d.set_xticks(tick_list)
    tick_list = _np.arange(ax_lim[1][0], ax_lim[1][1]+ax_tick[1], ax_tick[1])    
    axes3d.set_ylim(ax_lim[1])     
    axes3d.set_yticks(tick_list)
    tick_list = _np.arange(ax_lim[2][0], ax_lim[2][1]+ax_tick[2], ax_tick[2])     
    axes3d.set_zlim(ax_lim[2])      
    axes3d.set_zticks(tick_list)
    #Draw dashed lines across plot if x axis spans zero 
    if _np.sign(ax_lim[0][0] + ax_tick[0]/10.0**12) != \
        _np.sign(ax_lim[0][1] - ax_tick[0]/10.0**12):
        l = Line3D([0.0,0.0], ax_lim[1], [0.0,0.0], \
            linestyle = '--', linewidth = 1, color = [0,0,0])                                    
        axes3d.add_line(l)
        l = Line3D([0.0,0.0], [0.0,0.0], ax_lim[2],\
            linestyle = '--', linewidth = 1, color = [0,0,0])                                    
        axes3d.add_line(l)
    #Draw dashed lines across plot if y axis spans zero 
    if _np.sign(ax_lim[1][0] + ax_tick[1]/10.0**12) != \
        _np.sign(ax_lim[1][1] - ax_tick[1]/10.0**12):
        l = Line3D(ax_lim[0], [0.0,0.0], [0.0,0.0], \
            linestyle = '--', linewidth = 1, color = [0,0,0])                                    
        axes3d.add_line(l)
        l = Line3D([0.0,0.0], [0.0,0.0], ax_lim[2],\
            linestyle = '--', linewidth = 1, color = [0,0,0])                                    
        axes3d.add_line(l)  
    
    #Specify the viewing angle 
    #(elev = angle above z plane, azim = angle about the z-axis)
    axes3d.view_init(elev=view_alt_angle, azim=view_azm_angle)
    scatter = axes3d.scatter(xyz[0], xyz[1], xyz[2])
        
    #Add Title
    if title != 'None':
        axes3d.set_title(title)
        
    if filename != '':
        fig.save(filename)

    return(fig, axes3d, scatter)