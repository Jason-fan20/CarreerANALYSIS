# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:09:10 2020

@author: ASUS
"""

with open("test.txt", "r",encoding="utf-8") as f:
    row_list = f.read()
#    print(row_list)
    row_list=row_list.replace('\n',' ')
    print(eval(row_list))
    for thing in row_list:
        print(thing)