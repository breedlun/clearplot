# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 20:38:43 2015

@author: Ben
"""
import os
import clearplot
#reload is not part of python 3's built-in library, so we must import it
from imp import reload

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
        #(With python 2, you could just do 'execfile()', but python 3 forces you to read
        #the file and execute the code yourself)
        with open(d + '.py') as f:
            #(The compile call isn't strictly needed, but it associates the filename with 
            #the code object making debugging a little easier.)
        	code = compile(f.read(), d + '.py', 'exec')
        	exec(code)

os.chdir(cwd)
