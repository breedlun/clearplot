# -*- coding: utf-8 -*-
#Created on Sat Sep 20 11:19:52 2014
#@author: Benjamin Reedlunn

#Define clearplot version number
__version__ = '1.2.0'

import matplotlib as _mpl
import sys as _sys
import warnings as _warnings

#==============================================================================
# Check Upon Import
#============================================================================== 

#Define the minimimum version of matplotlib 
min_mpl_version = '1.4.0'
if 'sphinx' in _sys.modules:
    #Sphinx just documents the package, so it isn't necessary to have some 
    #of the newer features of matplotlib
    _warnings.warn("Warning: Clearplot detected that sphinx was loaded.  Sphinx just documents the package, so clearplot will allow older versions of matplotlib to be loaded.  Normally matplotlib " + min_mpl_version + " or greater is required.")
    min_mpl_version = '1.3.0'
 
def _parse_version_string(v):
    """Attempts to converts a version string to a tuple of integers."""
    v_list = v.split(".")
    try:
        #Usually the version only contains integers, so this should work
        v_list = tuple(map(int, (v_list)))
    except ValueError:
        #In development versions, they may create version '1.4.x', so we will
        #convert what we can to integers
        for i in range(len(v_list)):
            try:
                v_list[i] = int(v_list[i])
            except ValueError:
                print("""WARNING: Cannot parse 'matplotlib.__version__'. Please manually verify that your version of matplotlib is greater than """ + min_mpl_version)
    return v_list
#Verify the minimum version of matplotlib is installed
mpl_version = _parse_version_string(_mpl.__version__)
if mpl_version < _parse_version_string(min_mpl_version):
    raise ValueError('Matplotlib version must be ' + min_mpl_version + ' or greater')
if mpl_version == (1,4,2):
    _warnings.warn("Warning: Markers may not work properly due to a bug in matplotlib 1.4.2.", stacklevel = 2)
if mpl_version == (1,4,3):
    raise ValueError("Matplotlib 1.4.3 is incompatible with clearplot.  Matplotlib 1.4.3 has a bug that causes annotations, including axis labels, to be placed incorrectly.")
if mpl_version == (2,0,0):
    _warnings.warn("Warning: Due to a bug in matplotlib 2.0.0, text will be saved as font type 3 instead of font type 42.  This means that text in PDF or PS files will not be editable if the file is opened in a vector graphics program such as Adobe Illustrator.", stacklevel = 2)

#==============================================================================
# Define Parameters
#==============================================================================  

from clearplot import params

#==============================================================================
# Import for Convenience
#============================================================================== 

from clearplot import colors
from clearplot import figure
from clearplot import axes
from clearplot import color_bar
from clearplot import plot_functions