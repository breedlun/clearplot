.. Clearplot documentation master file, created by
   sphinx-quickstart on Tue Mar 31 20:10:19 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Clearplot
=========
Clearplot creates publication quality plots using matplotlib.  At the moment, the emphasis is on 2D plotting of simple curves and images, like the example below.

.. image:: Necking_Example.png

Although the documentation has detailed descriptions of the clearplot syntax, probably the best way to get started is to look at the `examples <./examples/index.html>`_.

Contents
========

.. toctree::
	:maxdepth: 4
	
    ./installation
    ./examples/index
    api/clearplot
    ./genindex
    ./version_history
    
Primary Features
----------------
- Features an object oriented interface for complicated plots and a procedural interface for simple plots.  Both interfaces are well documented in hyperlinked html.
- Supports linking and stacking multiple sets of axes in a figure.  Also supports up to two x and/or y-axes in a single plot.
- Automatically selects axis limits and tick mark spacings to pleasing values, but user may override.
- Axes labels are automatically offset from axes according to the width and height of the text.
- Curves can be labeled with text and a leader line.  Labels can be placed interactively, or by inputting the position of the text and the root of the leader line.
- Arrow heads can be placed on curves to indicate directionality.  Arrow heads can be placed interactively, or by inputting the arrow head position(s).
- Individual axes may be on a linear scale or a log scale.
- Support for bar plots, box and whisker plots, and violin plots.
- Support for several types of contour plots.
- Horizontal and/or vertical error bars can be placed on data points.
- Supports plotting field data as a sequence of images.
- Plots saved as pdfs are designed to be opened and easily edited in Adobe Illustrator or Inkscape.
- Uses a pleasing, easy to read font, TeXGyreHeros-txfonts, which was constructed to match the sans-serif Latin letters and the Greek letters in the txfonts (and newtx) package for LaTeX.  This means one can easily use a font for plots that matches the font in LaTeX generated equations.

Bug Fixes and Modifications
---------------------------

Please let me (breedlu@sandia.gov) know when you find any bugs, so I can squash them.  Feel free to modify the code yourself, but please rename clearplot to something else if you changed more than a simple setting.  I would rather not have multiple versions of clearplot floating around. If you have a neat feature to add, let me know and I might incorporate it into the code. 