# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 20:38:43 2015

@author: Ben
"""
import os
import clearplot
#reload is not part of python 3's built-in library, so we must import it
from importlib import reload

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
        print("Plotting " + d)
        #Run the test script
        #(With python 2, you could just do 'execfile()', but python 3 forces you to read
        #the file and execute the code yourself)
        with open(d + '.py') as f:
            #(The compile call isn't strictly needed, but it associates the filename with 
            #the code object making debugging a little easier.)
        	code = compile(f.read(), d + '.py', 'exec')
        	exec(code)

os.chdir(cwd)
