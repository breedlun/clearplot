Installation
============

1.	Get a recent copy of clearplot.
2.  Append the clearplot directory to your ``PYTHONPATH``.
3.	Load a python interpreter.  Verify that you can run ``>>> import clearplot`` without any errors.
4.	If you are using the Spyder IDE on a Mac, you may need to change the matplotlib backend loaded by Spyder's scientific startup script.  In order to make the plotting window appear on top of all other windows, clearplot makes a call to ``fig.canvas.manager.window``. With the MacOSX backend ``fig.canvas.manager.window`` gives ``AttributeError: 'FigureManagerMac' object has no attribute 'window'``.  To avoid this you must go to Spyder Preferences->Console->External Modules, set the GUI Backend to Qt4Agg and restart Spyder.  Check that the backend is actually QtAgg by entering ``matplotlib.get_backend()`` at the console. See `this post <http://stackoverflow.com/questions/20025077/how-do-i-display-a-matplotlib-figure-window-on-top-of-all-other-windows-in-spyde>`__ and `this post <http://stackoverflow.com/questions/26050709/matplotlib-trouble-reducing-figure-size-with-tkagg-backend>`__ if you need further details.
5.	Change the font.  See the text document titled ``What_to_do_with_these_files.rtf`` in the directory ``clearplot/Font_Files/`` to use TeXGyreHeros-txfonts.  Otherwise, matplotlib will default back to Bitstream Vera Sans.