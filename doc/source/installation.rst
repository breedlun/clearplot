Installation
============

Easy Way
--------

1.  Install clearplot using ``pip install -v clearplot`` from the command line.  

    a.  This will download clearplot from PyPI, install it on your ``PYTHONPATH``, and install the custom fonts in the proper directory.  The ``-v`` tells pip to be verbose, so you can see what pip is doing.
    
    b.  If pip has trouble connecting to the PyPI server, you can download clearplot from `PyPI's website <https://pypi.python.org/pypi/clearplot>`__ and run ``pip install -v [path]``, where ``[path]`` is the path to the downloaded tarball.   

Hard (Manual) Way
-----------------

1.	Get a recent copy of clearplot using ``git clone https://github.com/breedlun/clearplot``.

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

1.	If you are using the Spyder IDE on a Mac, you may need to change the matplotlib backend loaded by Spyder's scientific startup script.  The MacOSX backend and the TkAgg backend both have issues (see `this post <http://stackoverflow.com/questions/20025077/how-do-i-display-a-matplotlib-figure-window-on-top-of-all-other-windows-in-spyde>`__ and `this post <https://github.com/spyder-ide/spyder/issues/1651>`__ for more information).  If you are running into these problems, you must:

    a. Go to Spyder Preferences->Console->External Modules and set the GUI Backend to Qt4Agg.
    
    b. Go to Spyder Preferences->Console->Advanced Settings and select "Use the following startup script" to select the ``scientific_startup.py`` script. 
    
    c. Restart Spyder.  

2.	Install the custom fonts on your system so they can be accessed by other applications like Adobe Illustrator and Inkscape.
	
	a.  Find where Matplotlib stores its True Type fonts.  In a python interpreter, type the following two commands: ``import matplotlib``, ``matplotlib.matplotlib_fname()``.  On a mac you should get something like: ``.../python2.7/site-packages/matplotlib/mpl-data/matplotlibrc``.  The custom fonts, such as TeXGyreHeros-txfonts, should have been installed in ``.../python2.7/site-packages/matplotlib/mpl-data/fonts/ttf/``.
    
    b.  For Adobe Illustrator on a Mac, you can simply open the Font Book application (``/Applications/Utilities/Font Book``) and "drag and drop" the font files into the Font Book window.
    
    c.  For Inkscape on a Mac, you must copy the font files into the main font folder, not the user font folder.  The main font folder is located at ``/Library/Fonts``.
    
    d.  I do not know how to install fonts on Windows or Linux, but I am sure there are instructions online.
