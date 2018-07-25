# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 09:11:09 2017

@author: felipenanini
"""

class Mesa:
    def __init__(self):
        self.x = 0.0
        self.x0 = 0.0
        self.absref = True
        self.moved = False
    
    def connect(self, *rest):
        print("Conectou com a placa imaginaria")
         
    def moveCW(self, x):
        self.x = x 
        print("moveX " + str(x) + " -> x = " + str(self.x))
        
    def rmoveCW(self, x):
        self.x += x
        print("rmoveX " + str(x) + " -> x = " + str(self.x))
           
    def home(self):
        self.x = 0.0
        self.x0 = 0.0
        print("homeX")
        
    def position(self):
        p = dict(x=self.x)
        print(p)
        return p
        
    def abs_position(self):
        p = dict(x=self.x + self.x0)
        print(p)
        return p
    
    def set_reference(self):
        p = self.abs_position()
        self.x0 = p['x']
        self.x = 0.0

        
    def set_abs_reference(self):
        p = self.abs_position()
        self.x += self.x0
        self.x0 = 0

    def stop(self):
        print("PARADA IMEDIATA")
    def clear(self):
        print("CLEAR")
        
