# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 20:38:43 2015

@author: Ben
"""
import os

cwd = os.getcwd()
dir_list = os.listdir(cwd)
#I cannot figure out how to run the LaTeX example and then turn off LaTeX 
#typesetting without getting a ValueError that \displaystyle is not recognized.
#To avoid any issues, we simply make sure that the LaTeX example is done last.
dir_list.remove('LaTeX_typesetting')
dir_list.append('LaTeX_typesetting')

for d in dir_list:
    path = os.path.abspath(os.path.join(cwd,d))
    if os.path.isdir(path):
        os.chdir(path)
        execfile(d + '.py')

os.chdir(cwd)
