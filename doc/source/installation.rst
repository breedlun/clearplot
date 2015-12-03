Installation
============

Easy Way
--------

1.  Install clearplot using ``pip install clearplot`` from the command line.  This will download clearplot from PyPI, install it on your ``PYTHONPATH``, and install the custom fonts in the proper directory.

Hard (Manual) Way
-----------------

1.	Get a recent copy of clearplot.

2.  Append the clearplot directory to your ``PYTHONPATH``.

3.	Load a python interpreter.  Verify that you can run ``import clearplot`` without any errors.

4.  Place the custom fonts where matplotlib can find them.

    a.  Find where Matplotlib stores its True Type fonts.  In a python interpreter, type the following two commands: ``import matplotlib``, ``matplotlib.matplotlib_fname()``.  On a mac, you should get something like ``.../python2.7/site-packages/matplotlib/mpl-data/matplotlibrc``.  The True Type fonts are stored in ``.../python2.7/site-packages/matplotlib/mpl-data/fonts/ttf/``.
    
    b.  Grab the fonts in the directories inside ``clearplot/Font_Files/`` and place them in: ``.../python2.7/site-packages/matplotlib/mpl-data/fonts/ttf/``.
    
    c.  Find where Matplotlib stores its cache files.  In a python interpreter, enter ``matplotlib.get_cachedir()``.  On a mac, you should get something like ``/Users/[username]/.matplotlib``.
    
    d.  Go to ``/Users/[username]/.matplotlib`` and delete ``fontList.cache``.  Next time matplotlib is imported the cache file will be rebuilt.
    
    e.  If you run into trouble, or want more information, see `this post <http://blog.olgabotvinnik.com/post/35807476900/how-to-set-helvetica-as-the-default-sans-serif-font-in>`__.

Optional Additional Steps
-------------------------

1.	If you are using the Spyder IDE on a Mac, you may need to change the matplotlib backend loaded by Spyder's scientific startup script.  In order to make the plotting window appear on top of all other windows, clearplot makes a call to ``fig.canvas.manager.window``. With the MacOSX backend ``fig.canvas.manager.window`` gives ``AttributeError: 'FigureManagerMac' object has no attribute 'window'``.  To avoid this you must go to Spyder Preferences->Console->External Modules, set the GUI Backend to Qt4Agg and restart Spyder.  Check that the backend is actually QtAgg by entering ``matplotlib.get_backend()`` at the console. See `this post <http://stackoverflow.com/questions/20025077/how-do-i-display-a-matplotlib-figure-window-on-top-of-all-other-windows-in-spyde>`__ and `this post <http://stackoverflow.com/questions/26050709/matplotlib-trouble-reducing-figure-size-with-tkagg-backend>`__ if you need further details.

2.	Install the custom fonts on your system so they can be accessed by other applications like Adobe Illustrator and Inkscape.
	
	a.  Find where Matplotlib stores its True Type fonts.  In a python interpreter, type the following two commands: ``import matplotlib``, ``matplotlib.matplotlib_fname()``.  On a mac you should get something like: ``.../python2.7/site-packages/matplotlib/mpl-data/matplotlibrc``.  The custom fonts, such as TeXGyreHeros-txfonts, should have been installed in ``.../python2.7/site-packages/matplotlib/mpl-data/fonts/ttf/``.
    
    b.  For Adobe Illustrator on a Mac, you can simply open the Font Book application (``/Applications/Utilities/Font Book``) and "drag and drop" the font files into the Font Book window.
    
    c.  For Inkscape on a Mac, you must copy the font files into the main font folder, not the user font folder.  The main font folder is located at ``/Library/Fonts``.
    
    d.  I do not know how to install fonts on Windows or Linux, but I am sure there are instructions online.
