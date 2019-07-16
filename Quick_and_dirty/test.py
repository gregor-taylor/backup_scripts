# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:10:50 2017

@author: 0901754t
"""

class Class1():
    def __init__(self):
        print('Im init')
    def print_me(self,string):
        print(string)
        
class Class2():
    def __init__(self):
    	print('Class 2 init')

    def print_me_from_other_class(self, string):
    	Class1.print_me(self,string)
        
    

test = Class2()
test.print_me_from_other_class('TEST')
#test.inherit('TEST')


