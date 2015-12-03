Version History
===============

version 1.0.3

1.  Modified the PyPI installation script to automatically install the custom fonts.
2.  Moved the color map arrays and the raw data used in the examples into csv files to finish resolving issues on github and PyPI.

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