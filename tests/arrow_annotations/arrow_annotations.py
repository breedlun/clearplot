#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 28 07:28:03 2025

@author: ben
"""

import clearplot.figure as cp_fig

fig = cp_fig.Figure()
ax = fig.add_axes()

#Normal arrow 
#(Need to look into why this does not create the tail behind the arrowhead,
#and need to make sure the solution does not produce tails for cases that
#should only have a arrowhead without a tail.)
ax.add_arrow('-)>', [0.5, 0.25], 'data', 0, 20)

#Monolithic arrow with a fat tail
ax.add_arrow('=)>', [0.5, 0.5], 'data', 0, 20, line_width = 3)


