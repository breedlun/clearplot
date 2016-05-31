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
#Do not run the in development tests
dir_list.remove('in_development')

for d in dir_list:
    path = os.path.abspath(os.path.join(cwd,d))
    if os.path.isdir(path):
        #Change to the test folder
        os.chdir(path)
        #Reload the default parameters in case any of the tests change 
        #the parameters.
        reload(clearplot.params)
        #Run the test script
        execfile(d + '.py')

os.chdir(cwd)
