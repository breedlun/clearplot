.. _examples:

.. raw:: html

    <style type="text/css">
    .figure {
        position: relative;
        float: left;
        margin: 10px;
        width: 180px;
        height: 200px;
    }

    .figure img {
        position: absolute;
        display: inline;
        left: 0;
        width: 170px;
        height: 170px;
        opacity:1.0;
        filter:alpha(opacity=100); /* For IE8 and earlier */
    }

    .figure:hover img {
        -webkit-filter: blur(1px);
        -moz-filter: blur(1px);
        -o-filter: blur(1px);
        -ms-filter: blur(1px);
        filter: blur(1px);
        opacity:1.0;
        filter:alpha(opacity=100); /* For IE8 and earlier */
    }

    .figure span {
        position: absolute;
        display: inline;
        left: 0;
        width: 170px;
        height: 170px;
        background: #BFD1D4;
        color: #000000;
        visibility: hidden;
        opacity: 0;
        z-index: 100;
    }

    .figure p {
        position: absolute;
        top: 33%;
        width: 170px;
        font-size: 110%;
    }

    .figure:hover span {
        visibility: visible;
        opacity: .4;
    }

    .caption {
        position: absolue;
        width: 180px;
        top: 170px;
        text-align: center !important;
    }
    </style>


Examples
========

These examples serve to showcase clearplot's capabilities, help new users get clearplot's syntax right, and verify that clearplot is working correctly.  Click on any image to see full size image and source code.

.. toctree::
	:hidden:
	
	./bare_bones/bare_bones.rst
	
	./basic/basic.rst
	
	./no_axis_arrows/no_axis_arrows.rst
	
	./two_curves-legend/two_curves-legend.rst
	
	./two_curves-labels-no_units/two_curves-labels-no_units.rst
	
	./two_y_axes/two_y_axes.rst
	
	./log_log_plot/log_log_plot.rst
	
	./arrows-custom_tick_labels/arrows-custom_tick_labels.rst
	
	./vertically_stacked/vertically_stacked.rst
	
	./LaTeX_typesetting/LaTeX_typesetting.rst
	
	./error_bars/error_bars.rst
	
	./bar_plot/bar_plot.rst
	
	./violin_plot-custom_tick_labels/violin_plot-custom_tick_labels.rst
	
	./plot_image_and_add_curve/plot_image_and_add_curve.rst
	
	./contour_plot-filled/contour_plot-filled.rst
	
	./contour_plot-image-log_scale/contour_plot-image-log_scale.rst
	
	./curve_and_image_sequence/curve_and_image_sequence.rst
	
	./video/video.rst


.. raw:: html

    <div class='figure align-center'>
    <a href=./bare_bones/bare_bones.html>
    <img src=../_images/bare_bones.png>
    <span class='figure-label'>
    <p>Bare Bones</p>
    </span>
    </a>
    </div>
    
.. raw:: html

    <div class='figure align-center'>
    <a href=./basic/basic.html>
    <img src=../_images/basic.png>
    <span class='figure-label'>
    <p>Basic</p>
    </span>
    </a>
    </div>

.. raw:: html

    <div class='figure align-center'>
    <a href=./no_axis_arrows/no_axis_arrows.html>
    <img src=../_images/no_axis_arrows.png>
    <span class='figure-label'>
    <p>No Axis Arrows</p>
    </span>
    </a>
    </div>
    
.. raw:: html

    <div class='figure align-center'>
    <a href=./two_curves-legend/two_curves-legend.html>
    <img src=../_images/two_curves-legend.png>
    <span class='figure-label'>
    <p>Two Curves - Legend</p>
    </span>
    </a>
    </div>
    
.. raw:: html

    <div class='figure align-center'>
    <a href=./two_curves-labels-no_units/two_curves-labels-no_units.html>
    <img src=../_images/two_curves-labels-no_units.png>
    <span class='figure-label'>
    <p>Two Curves - Labels - No Units</p>
    </span>
    </a>
    </div>
    
    
.. raw:: html

    <div class='figure align-center'>
    <a href=./two_y_axes/two_y_axes.html>
    <img src=../_images/two_y_axes.png>
    <span class='figure-label'>
    <p>Two Y Axes</p>
    </span>
    </a>
    </div>

.. raw:: html

    <div class='figure align-center'>
    <a href=./log_log_plot/log_log_plot.html>
    <img src=../_images/log_log_plot.png>
    <span class='figure-label'>
    <p>Log Log Plot</p>
    </span>
    </a>
    </div>
    
.. raw:: html

    <div class='figure align-center'>
    <a href=./arrows-custom_tick_labels/arrows-custom_tick_labels.html>
    <img src=../_images/arrows-custom_tick_labels.png>
    <span class='figure-label'>
    <p>Arrows - Custom Tick Labels</p>
    </span>
    </a>
    </div>
    
.. raw:: html

    <div class='figure align-center'>
    <a href=./vertically_stacked/vertically_stacked.html>
    <img src=../_images/vertically_stacked.png>
    <span class='figure-label'>
    <p>Vertically Stacked</p>
    </span>
    </a>
    </div>
    
.. raw:: html

    <div class='figure align-center'>
    <a href=./LaTeX_typesetting/LaTeX_typesetting.html>
    <img src=../_images/LaTeX_typesetting.png>
    <span class='figure-label'>
    <p>LaTeX Typesetting</p>
    </span>
    </a>
    </div>
    
.. raw:: html

    <div class='figure align-center'>
    <a href=./error_bars/error_bars.html>
    <img src=../_images/error_bars.png>
    <span class='figure-label'>
    <p>Error Bars</p>
    </span>
    </a>
    </div>
    
.. raw:: html

    <div class='figure align-center'>
    <a href=./bar_plot/bar_plot.html>
    <img src=../_images/bar_plot.png>
    <span class='figure-label'>
    <p>Bar Plot</p>
    </span>
    </a>
    </div>
    	
.. raw:: html

    <div class='figure align-center'>
    <a href=./violin_plot-custom_tick_labels/violin_plot-custom_tick_labels.html>
    <img src=../_images/violin_plot-custom_tick_labels.png>
    <span class='figure-label'>
    <p>Violin Plot - Custom Tick Labels</p>
    </span>
    </a>
    </div>

.. raw:: html

    <div class='figure align-center'>
    <a href=./plot_image_and_add_curve/plot_image_and_add_curve.html>
    <img src=../_images/plot_image_and_add_curve.png>
    <span class='figure-label'>
    <p>Plot Image and Add Curve</p>
    </span>
    </a>
    </div>
    
.. raw:: html

    <div class='figure align-center'>
    <a href=./contour_plot-filled/contour_plot-filled.html>
    <img src=../_images/contour_plot-filled.png>
    <span class='figure-label'>
    <p>Filled Contours</p>
    </span>
    </a>
    </div>
    
.. raw:: html

    <div class='figure align-center'>
    <a href=./contour_plot-filled/contour_plot-image-log_scale.html>
    <img src=../_images/contour_plot-image-log_scale.png>
    <span class='figure-label'>
    <p>Log Scaled Contours</p>
    </span>
    </a>
    </div>
    
.. raw:: html

    <div class='figure align-center'>
    <a href=./curve_and_image_sequence/curve_and_image_sequence.html>
    <img src=../_images/curve_and_image_sequence-b.png>
    <span class='figure-label'>
    <p>Curve and Image Sequence</p>
    </span>
    </a>
    </div>
    
.. raw:: html

    <div class='figure align-center'>
    <a href=./video/video.html>
    <img src=../_images/video.png>
    <span class='figure-label'>
    <p>Video</p>
    </span>
    </a>
    </div>

.. raw:: html

    <div style="clear: both"></div>
    
Note: the examples save the figure window as a png by specifying '.png' in the file name.  No extension is needed to save the figure in the default file format (pdf).