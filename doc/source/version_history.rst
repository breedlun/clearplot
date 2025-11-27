Version History
===============

version 1.3.1
1. Switched from setup.py to pyproject.toml to make distribution files compatible with pypi's current (Nov. 2025) standards.
2. Replaced the font installation step with the matplotlib version 3.3+ ability to register fonts at runtime that are not in the user, system, or matplotlib font directories.

version 1.3.0

1. Revised legend placement to enable a greater variety of legend locations outside the plot axes.  The new input syntax, unfortunately, is not backwards compatible with the old syntax for placing a legend outside the axes.
2. Added the ability to fill the vertical or horizontal region defined by two curves.
3. Revised automatic selection of axis limits when the limits for the orthogonal axis have already been set.
4. Revised curve clipping routine to properly handle a curve that exits and reenters the plotting region with only one or two points outside the plotting region.
5. Fixed a bug that prohibited user specified tick mark spacings with log scaled axes.
6. Fixed several bugs related to new symlog capability.
7. Fixed a bug that prohibited user specified tick mark spacings with log scaled axes.
8. Revised curve clipping routine to properly handle a curve that exits and re-enters the plotting region with only one or two points outside the plotting region.
9. Revised curve clipping routine to avoid adding data points at intersections with axis limits if the linestyle is 'none'.
10. Made a number of minor revisions to remain compatible with the latest versions of python, numpy, and matplotlib.

version 1.2.2

1. Added the ability to specify symlog scaled axes that span both negative and positive values.
2. Modified axes.plot_intensity_map() to use pcolormesh instead of add_image since pcolormesh can handle nonlinearly scaled x and y axes.
3. Fixed a bug in the developmental plot_surface() function.

version 1.2.1

1. Updated to be compatible with matplotlib 3.3.0.
2. Fixed a bug where axis arrows would get scaled when the distance between tick marks was scaled.
3. Changed the default marker edge width to be 2 points when a non-filled marker such as 'x' is specified.
4. Made the dark color lists not quite so dark.
5. Changed the default optional argument from 'auto' to the more pythonic None.

version 1.2.0

1. Updated to be compatible with Python 3.
2. Updated to be compatible with matplotlib 2.0.0
3. Modified the color bar class so that multiple images can use the same color bar.
4. Added the ability to plot an intensity map (heat map) as an image.
5. Added the ability to place lines and rectangles that span the axes horizontally or vertically.
6. Added the ability to specify the gap between the color bar and the axes.
7. Fixed a bug where user input axes positions would sometimes work incorrectly if they were specified after axes instantiation.
8. Fixed bug where user specified labels would be lost in pf.plot_markers() and pf.plot_bars().
9. Fixed the bug so that all sets of markers, instead of just the first set, are output by ax.plot_markers().

version 1.1.0

1. Added the ability to have log scaled color bars.
2. Reorganized the color bar code to minimize code duplication between the initialization method and other methods.
3. Fixed a bug that prevented the color bar from returning the list of tick mark positions.  
4. Fixed a bug that caused the color bar label to be placed incorrectly if the color bar size or position were changed.
5. Altered the way users specify labels to artists.  Labels are now specified upon artist creation rather than when the legend is added to the plot.  This way the label becomes associated with the artist object, which makes complex legends with multiple data types much easier.
6. Fixed a bug that caused a duplicate legend to be placed on top of the original legend.
7. Converted the dashed line that marks 0 into a spline instead of a curve.  This associates the dashed line more strongly with the axes.  For example, hiding the axes now hides the dashed lines too.
8. Changed the default marker edge width to zero for curves.  Now both markers and curves have zero marker edge width.
9. Fixed a bug that allowed markers to sometimes appear outside of the plotting area.
10. Fixed a bug with auto-adjusting shared axes.  If x/y axis is shared then clearplot attempts to adjust the pair of y/x axes to make them have the same number of tick marks.  If it fails, then it will adjust the physical spacing between the tick marks.  This should be more robust now.
11. Fixed a bug with picking label text and specifying the leader line angle.

version 1.0.7

1. Changed the default marker edge width to zero.  
2. Made figure window only appear on top of all other windows if interactive mode is on.
3. Added a method to the figure class to close the figure window.
4. Fixed a bug that caused fig.auto_adjust_layout() to ignore legends.  This bug often caused big legends or legends placed outside of the axes to get clipped.
5. Changed the latter part of the standard color list to have more distinctive colors.  Also automated the process of creating dark, darker, and pastel color lists from the standard colors list.
6. Make the tick label e^n non-italic for natural logarithm scaled axes.
7. Fixed a bug where axes would be added to the current figure, even if the user specified a different figure.

version 1.0.6

1. Enabled arbitrary logarithmic bases for log scaled axes.
2. Fixed an incompatibility with circled labels and matplotlib versions prior to 1.5.0.
3. Fixed a bug with setting the physical distance between tick marks before creating axis labels.
4. Fixed a bug with changing the physical distance between tick marks on log axes.
5. Fixed a bug where linked axes did not inherit the physical distance between tick marks.
6. Fixed a bug with determining the unique curves for a legend when the plot has curves with and without markers.
7. Fixed a bug with autoselecting limits with shared axes.

version 1.0.5

1. Switch the matplotlib backend from Qt4Agg to TkAgg, since TkAgg is the only interactive backend that is supposed to work "out of the box" with matplotlib, as of matplotlib version 1.5.0.  

version 1.0.4

1. Updated setup.py to install the custom fonts more robustly and to install the color map csv files.
2. Switched to the warnings module instead of simply printing warnings.

version 1.0.3

1. Modified setup.py to automatically install the custom fonts.
2. Moved the color map arrays and the raw data used in the examples into csv files to finish resolving issues on github and PyPI.

version 1.0.1 and 1.0.2

1. Hard coded the color map definitions instead of loading them from a pickled file to resolve issues on github and PyPI.  Also moved color lists and color maps into a new module called colors.  

version 1.0

1. Renamed BRplot to clearplot and made it publicly available for the first time.

BRplot version 3.0

1. Reorganized BRplot from a single python module into a package.
2. Transitioned from documenting BRplot with only docstrings to using Sphinx-doc to generate html documentation.
3. Restructured package to give it an object oriented interface.  The functional interface still exists for generating standard plots, but the object oriented interface is helpful for creating custom, specialized, or complicated plots.  The primary changes are the figure object and axes object.  When the figure/axes objects is created, it also instantiates a matplotlib figure/axes object inside of it, which is easily accessed by typing fig.mpl_fig / ax.mpl_ax. 
4. Added the ability to link one x/y axis to another x/y axis in the same figure window so that the axes have the same limits and tick mark spacing.  This allows one to easily stack sets of axes vertically/horizontally in a figure window, and keep the x/y axes synchronized.
5. Improved the automatic limit and tick mark selection for plots with multiple x axes or multiple y axes.
6. Added the ability to create violin plots, which provide an easy way to compare several statistical distributions. 
7. Switched from the TkAgg backend to the Qt4Agg backend.  The Qt4Agg backend seems to let you change the figure window size at will, while TkAgg acts quite strangely.  (For further details, see `this post <http://stackoverflow.com/questions/26050709/matplotlib-trouble-reducing-figure-size-with-tkagg-backend>`__ and `this post <https://github.com/matplotlib/matplotlib/issues/3584>`__.)
8. Curve legends and marker legends automatically eliminate any duplicate labels.

BRplot version 2.0

1.  The function contour() was added to make contour plots.
2.  Added the ability to place error bars on data points.
3.  The function bar_plot() was added to create bar plots.
4.  The function box_plot() was added to create box and whisker plots.
5.  Added the ability to place one or more plots in a preexisting figure window.
6.  Added an example showing how to use BRplot in a video.
7.  Altered the legend keyword arguments to make it easier to place legends.  Also, users can now pass any matplotlib legend keyword through to the legend method.
8.  Added the ability to specify a list of LaTeX strings for tick mark labels.
9.  Made pdf the default file type rather than the only file type for saving figures.  Now users can input a file name with a file extension that matplotlib recognizes, and the file will be saved as the file type corresponding to the file extension.
10. Fixed a bug that caused the placement of axis labels to be off by about 10% of the width and height of the label.  In BRplot, axis labels are first placed, then their bounding boxes are measured using the current renderer, and finally they are moved to the correct location.  Unfortunately, BRplot was inadvertently using the wrong renderer when it measured the text bounding box.  Several placement settings were designed around this incorrect renderer, so most of the time things looked just fine.  However, the placement settings were unable to compensate for long text strings, which is what revealed this bug.  BRplot should now use the correct renderer, and place axis labels correctly.  For further information, see `this post <http://stackoverflow.com/questions/22667224/matplotlib-get-text-bounding-box-independent-of-backend/22689498#22689498>`__.
11. It is now possible to turn off the axis arrows.
12. Improved the auto settings for im_plot() and im_show().
13. Improved the organization of the examples and tests.
14. Internal housekeeping: grouped similar variables into dictionaries.
15. Tracked down some confusing behavior when embedding an image in a vector graphics file, such as a pdf.  See `this post <https://github.com/matplotlib/matplotlib/issues/2972>`_ for further details.  BRplot now tries to select the proper interpolation method based on the size of the image in the figure window, but the user can override.

BRplot version 1.0

1.	Made the figure window appear on top of all other windows instead of behind everything.  This turned out to be quite tricky.  See `this post <http://stackoverflow.com/questions/20025077/how-do-i-display-a-matplotlib-figure-window-on-top-of-all-other-windows-in-spyde>`__ for further details
2.	Took the default values for the keyword arguments out of the function definition line.  Now the keyword arguments are parsed inside the function.  This makes the function definition line much cleaner.
3.	The function im_plot() can now display a color bar.
4.	The function im_show() was added to display a sequence of images.
5.	Added the capability to label curves with leader lines. Curves can be labeled interactively, or by specifying the position of the text and the root of the leader line.
6.	The function add_labels() was added to place multiple labels on a single curve.
7.	Updated the documentation.
8.	Made functions internal to BRplot private.  This way, code introspection will first display the functions that users are meant to employ.
9.	If the axes limits could be tighter, but the data will extend very slightly past the limits, the auto limit algorithm will now select the tighter limits.
10.	Changed the input syntax for marker styles, label styles, and line styles so that the user can input either a dictionary or individual style attributes.
11.	Added the capability to place arrow heads on the curves.  Curves can be labeled interactively, or by inputting the position of the arrow head(s).
12.	Changed the default to italic characters for variables and upright characters for units.
13.	Changed the default font to TeXGyreHerosTXfonts.  This font is a combination of TeXGyreHeros (reduced in size by 10%) for the Latin letters and the math font from the LaTeX txfonts package for the greek letters.
14.	Added the proper LaTeX preamble to replicate TeXGyreHerosTXfonts when usetex = True.
15.	Converted the examples to an IPython notebook.  This makes it easier to see the impact of the various options.
16.	Improved y-axis label placement for LaTeX strings whose bounding box extends far below the text baseline.
17.	Added some custom colormaps 

BRplot Version 0.2

1.	Improved PDF bounding box so that it tightly wraps around the limits of the figure content. (The mpl.rcParams['savefig.bbox']='tight' previously did not work well because BRplot created a set of invisible figure axes to place annotations and axis labels in.  The bounding box became the edges of the figure axes, even though they were invisible.  Removing the figure axes also means that PDFs opened in Adobe Illustrator have fewer clipping masks to delete.)
2.	Added the ability to input a list of tick marks.
3.	If you have clip_on = True in matplotlib, then each curve has it's own clipping mask, which is really annoying when you just want to select a curve in Adobe Illustrator. In addition, the data outside the clipping mask is visible once you release the clipping mask. Instead, I switched clip_on = False, and I do the clipping prior to plotting the data.

BRplot Version 0.1

1.	Initial testing
2.	Added a list of example problems.