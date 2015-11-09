# -*- coding: utf-8 -*-
#Created on Fri Oct 10 19:39:21 2014
#@author: Benjamin Reedlunn

import matplotlib as _mpl
import numpy as _np

##==============================================================================
## Circle Box
##============================================================================== 
#
#class _Circle_Box_Style(_mpl.patches.BoxStyle._Base):
#    """
#    A circle box style to be used with annotations
#    """
#    def __init__(self, pad=0.1):
#        self.pad = pad
#        super(_Circle_Box_Style, self).__init__()
#
#    def transmute(self, x0, y0, width, height, mutation_size):
#        # padding
#        pad = mutation_size * self.pad
#        # center
#        cx, cy = x0+.5*width, y0+.5*height 
#        # width and height with padding added.
#        width, height = width + 2.*pad, height + 2.*pad,
#        # get radius
#        radius = (width**2 + height**2)**.5 * .5
#        print "radius = " + str(radius)
#        # Generate path of the circle
#        cir_path = _mpl.path.Path.unit_circle()
#        vertices = radius*cir_path.vertices + (cx, cy)
#        path = _mpl.path.Path(vertices, cir_path.codes)
#
#        return path
#        
#_mpl.patches.BoxStyle._style_list['circle'] = _Circle_Box_Style

#==============================================================================
# Slick Arrow
#============================================================================== 

_dflt_head_length = round(72.0/25.4 * 7.0, 4)
_dflt_head_width = round(72.0/25.4 * 7.0 * 0.4, 4)
_dflt_length = 72.0/25.4 * 20

class _Slick_Arrow(_mpl.patches.ArrowStyle._Base):
    """
    Base class for a John Shaw approved arrow style to be used with annotations
    """
    def __init__(self, beginarrow = None, endarrow = None, 
        head_length = _dflt_head_length, head_width = _dflt_head_width, \
        monolithic = False, length = 0):
        """
        The arrows are drawn if *beginarrow* and/or *endarrow* are
        true. *head_length* and *head_width* determines the size
        of the arrow, in points (1/72"), relative to the *mutation scale*.  
        """
        self.beginarrow = beginarrow
        self.endarrow = endarrow
        self.head_length = head_length
        self.head_width = head_width
        self.fillbegin = True
        self.fillend = True
        self.monolithic = monolithic
        self.length = length
        super(_Slick_Arrow, self).__init__()

    def _gen_arrow_path(self, x_a, x_b, head_width, head_length, length, \
        monolithic = False):
        """
        Returns the path for the arrowhead or a monolithic, straight, arrow.
        
        Parameters
        ----------
        x_a: 1x2 array or list
            Coordinates of a point aligned with back of arrow
        x_b: 1x2 array or list
            Coordinates of the tip of the arrowhead
        head_width: float
            Arrowhead width, in points (1/72")
        head_length: float
            Arrowhead length, in points (1/72")
        length: float
            Arrow length from tip to tail, in points *1/72")
        monolithic: bool, optional
            Specifies whether to make the arrow a combination of a line and
            a patch, or to make it a sinle monolithic patch
        
        Returns
        -------
        path: path object
        """
        #Define the radius of the back of the arrow (in points) 
        head_R = head_width / 2.0
        
        if monolithic:
            #Define the number of points along the curve of the back of the arrow            
            n = 12
            #Define the total number of points needed to construct the patch
            m = n + 4
            #Specify the line width of the arrow tail (in points)
            line_width = 0.75
            
            #Construct the arrow in clockwise fashion
            #Tip
            X_tip = _np.array([[0],[0]])            
            #Bottom half of arrowhead back
            #Find the angle of the intersection point, where the line hits the 
            #back of the arrowhead
            theta_0 = _np.arcsin(line_width/(2.0*head_R))               
            theta_bot = _np.linspace(-_np.pi/2.0 + _np.pi/15.0, -theta_0, n/2)
            X_bot =  head_R * _np.array([_np.cos(theta_bot), _np.sin(theta_bot)])
            X_bot[0,:] = X_bot[0,:] - head_length
            #Straight line
            X_line = _np.array([[-length, -line_width/2.0], [-length, line_width/2.0]]).T
            #Top half of arrowhead back
            theta_top = _np.linspace(theta_0, _np.pi/2.0 - _np.pi/15.0, n/2)
            X_top =  head_R * _np.array([_np.cos(theta_top), _np.sin(theta_top)])
            X_top[0,:] = X_top[0,:] - head_length            
            #Put them together, and add extra point at the tip to close the path
            X = _np.concatenate([X_tip, X_bot, X_line, X_top, X_tip, X_tip], axis = 1)
        else:
            #Define the number of points along the curve of the back of the arrow 
            n = 11
            #Define the total number of points needed to construct the patch
            m = n + 2
            
            #Construct the arrow in clockwise fashion
            #Tip
            X_tip = _np.array([[0],[0]])
            #Arrowhead back
            theta = _np.linspace(-_np.pi/2.0 + _np.pi/15.0, _np.pi/2.0 - _np.pi/15.0, n)
            X_back = head_R * _np.array([_np.cos(theta), _np.sin(theta)])
            X_back[0,:] = X_back[0,:] - head_length
            #Put them together, and add extra point at the tip to close the path
            X = _np.concatenate([X_tip, X_back, X_tip, X_tip], axis = 1)
        
        #Get the arrowhead orientation
        orient = _np.arctan2(x_b[1] - x_a[1], x_b[0] - x_a[0])
        #Define a rotation matrix and rotate into the desired orientation 
        Q = _np.array([[_np.cos(orient), -_np.sin(orient)], [_np.sin(orient), _np.cos(orient)]])    
        X = _np.dot(Q, X)
        #Shift to the desired location
        path_vertices = _np.array(x_b)[:,None] + X
        #Define the reference point that defines the location of the patch (MOVETO)
        #Define the other points that define the shape of the patch (LINETO)
        #Define the point to close the polygon with (CLOSEPOLY)
        path_codes = [_mpl.path.Path.MOVETO] + \
                     [_mpl.path.Path.LINETO] * (m - 1) + \
                     [_mpl.path.Path.CLOSEPOLY]
        #Generate the path object             
        path = _mpl.path.Path(path_vertices.T, path_codes)

        return(path)

    def transmute(self, path, mutation_size, line_width):
        """
        Generates the proper arrow head path and scales it.
        
        Parameters
        ----------
        path: path object
            The path along which the arrow will be drawn
        muatation_size: float
            The amount the arrow head will be scaled
        line_width: float
            May be used to adjust the the path so that it does not pass beyond 
            the given points.
            
        Returns
        -------
        path_list: list
            A list of Path instances
        fillable list: list
            A list of booleans, each indicating whether the corresponding Path
            instance in `path_list` can be filled or not.
        """
        #Scale the arrow
        head_length = self.head_length * mutation_size
        head_width = self.head_width * mutation_size
        length = self.length * mutation_size

        #Construct the output lists
        path_list = [path]
        fillable_list = [False]
        
        #Arrow at the beginning of the line
        if self.beginarrow:
            #The incoming path is typically an 'arc3' path, so we grab the 
            #first two vertices to help align the arrow head
            x0 = path.vertices[0]
            x1 = path.vertices[1]
            ah_path = self._gen_arrow_path(x1, x0, head_width, \
                head_length, length, monolithic = self.monolithic)
            path_list.append(ah_path)
            fillable_list.append(True)

        #Arrow at the end of the line
        if self.endarrow:
            #The incoming path is typically an 'arc3' path, so we grab the 
            #last two vertices to help align the arrow head
            x2 = path.vertices[-2]
            x3 = path.vertices[-1]
            ah_path = self._gen_arrow_path(x2, x3, head_width, \
                head_length, length, monolithic = self.monolithic)
            path_list.append(ah_path)
            fillable_list.append(True)                                 

        return(path_list, fillable_list)


class Slick_Arrow_A(_Slick_Arrow):
    """
    An arrow with a head at its beginning point.
    """

    def __init__(self, head_length = _dflt_head_length, \
        head_width = _dflt_head_width, length = _dflt_length):
        """
        Instantiates an arrow with a head at its beginning point.
        
        Parameters
        ----------
        head_length : float, optional
            length of the arrow head, in points (1/72")
        head_width : float, optional
            width of the arrow head, in points (1/72")
        length : float, optional
            length of the arrow from tip to tail, in points (1/72")
        """

        super(Slick_Arrow_A, self).__init__(
              beginarrow=True, endarrow=False,
              head_length=head_length, head_width=head_width, length = length)

_mpl.patches.ArrowStyle._style_list["<(-"] = Slick_Arrow_A

class Slick_Arrow_B(_Slick_Arrow):
    """
    An arrow with a head at its end point.
    """

    def __init__(self, head_length = _dflt_head_length, \
        head_width = _dflt_head_width, length = _dflt_length):
        """
        Instantiates an arrow with a head at its end point.
        
        Parameters
        ----------
        head_length : float, optional
            length of the arrow head, in points (1/72")
        head_width : float, optional
            width of the arrow head, in points (1/72")
        length : float, optional
            length of the arrow from tip to tail, in points (1/72")
        """

        super(Slick_Arrow_B, self).__init__(
            beginarrow=False, endarrow=True,
            head_length=head_length, head_width=head_width, length = length)

_mpl.patches.ArrowStyle._style_list["-)>"] = Slick_Arrow_B

class Slick_Arrow_AB(_Slick_Arrow):
    """
    An arrow with heads at its beginning and end points.
    """

    def __init__(self, head_length = _dflt_head_length, \
        head_width = _dflt_head_width, length = _dflt_length):
        """
        Instantiates an arrow with heads at its beginning and end points.  
        
        Parameters
        ----------
        head_length : float, optional
            length of the arrow head, in points (1/72")
        head_width : float, optional
            width of the arrow head, in points (1/72")
        length : float, optional
            length of the arrow from tip to tail, in points (1/72")
        """

        super(Slick_Arrow_AB, self).__init__(
            beginarrow=True, endarrow=True,
            head_length=head_length, head_width=head_width, length = length)

_mpl.patches.ArrowStyle._style_list["<(-)>"] = Slick_Arrow_AB

class Axis_Arrow(_Slick_Arrow):
    """
    A monolithic arrow with a head at its end point.
    """

    def __init__(self, head_length = _dflt_head_length, \
        head_width = _dflt_head_width, length = _dflt_length):
        """
        Parameters
        ----------
        head_length : float, optional
            length of the arrow head, in points (1/72")
        head_width : float, optional
          width of the arrow head, in points (1/72")
        length : float, optional
            length of the arrow from tip to tail, in points (1/72")
        """

        super(Axis_Arrow, self).__init__( \
            beginarrow=False, endarrow=True, \
            head_length=head_length, head_width=head_width, \
            monolithic = True, length = length)

_mpl.patches.ArrowStyle._style_list["=)>"] = Axis_Arrow