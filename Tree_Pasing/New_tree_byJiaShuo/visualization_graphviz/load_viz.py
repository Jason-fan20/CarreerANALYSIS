# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 19:52:38 2020

@author: ASUS
"""

with open("test-table2.gv", "r",encoding='utf-8') as f:
    dot1 = f.read()
    
import graphviz
dot=graphviz.Source(dot1)
dot.view()