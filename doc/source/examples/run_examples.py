# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 20:38:43 2015

@author: Ben
"""
import os
import clearplot

#Get the names of all the examples
cwd = os.getcwd()
dir_list = os.listdir(cwd)
#I cannot figure out how to run the LaTeX example and then turn off LaTeX 
#typesetting without getting a ValueError that \displaystyle is not recognized.
#I will simply make sure that the LaTeX example is done last, so everything 
#else runs.
dir_list.remove('LaTeX_typesetting')
dir_list.append('LaTeX_typesetting')

for d in dir_list:
    path = os.path.abspath(os.path.join(cwd,d))
    if os.path.isdir(path):
        #Change to the example folder
        os.chdir(path)
        #Reload the default parameters in case any of the examples change 
        #the parameters.
        reload(clearplot.params)
        #Run the example script
        execfile(d + '.py')

os.chdir(cwd)
