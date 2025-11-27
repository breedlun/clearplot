Installation
============

Using pip
---------

1.  Install clearplot using ``pip install -v clearplot`` from the command line.  

    a.  This will download clearplot from PyPI, install it on your ``PYTHONPATH``, and install the custom fonts in the proper directory.  The ``-v`` tells pip to be verbose, so you can see what pip is doing.
    
    b.  If pip has trouble connecting to the PyPI server, you can download clearplot from `PyPI's website <https://pypi.python.org/pypi/clearplot>`__ and run ``pip install -v [path]``, where ``[path]`` is the path to the downloaded tarball.   

Using github
------------

1.	Get a recent copy of clearplot using ``git clone https://github.com/breedlun/clearplot``.

2.  Append the clearplot directory to your ``PYTHONPATH``.

3.	Load a python interpreter.  Verify that you can run ``import clearplot`` without any errors.


Optional Additional Steps
-------------------------
 
1.	Install the custom fonts on your system so they can be accessed by other applications like Adobe Illustrator and Inkscape.
	
	a.  Find where clearplot stores its True Type fonts.  In a python interpreter, type the following two commands: ``import clearplot``, ``clearplot.__file__``.  On a mac you should get something like: ``.../site-packages/clearplot/clearplot/__init__.py``.  The custom fonts, such as TeXGyreHerosTXfonts, should have been installed in ``.../site-packages/clearplot/clearplot/true_type_fonts/``.
    
    b.  For Mac users:
    
    	i.	Open the Font Book application (``/Applications/Utilities/Font Book``) 
    	
    	ii. Select the "All Fonts" group from the left tray. 
    	
    	iii. "Drag and drop" the font files into the Font Book window while holding down the option key to copy the font files instead of moving them.
    
    c.  I do not know how to install fonts on Windows or Linux, but I am sure there are instructions online.
