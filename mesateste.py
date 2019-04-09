# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 09:11:09 2017

@author: felipenanini
"""

class Robo:

    def __init__(self, port = "\\\\.\\COM1", baudrate = 9600, bytesize = 8, 
                 parity = 'N', stopbits = 1, passoMotor=28100000, passoEncoder=2492):
        self.x = 0.0
        self.x0 = 0.0
        self.absref = True
        self.moved = False
    def connect(self):
        pass
    
    
    def move(self, x, a = False, r = False, sync = False):
        if r:
            self.x += x
        elif a:
            self.x = x + self.x0
        else:
            self.x = x
        print("move(x={}, a={}, r={}, sync={}".format(x, a, r, sync))
    
    def rmove(self, x, sync = False):
        """Inicializa a movimentacao incremental do robo no eixo indicado"""
        self.move(x, r=True, sync=sync)
        return
    def abs_position(self, pulses=False):
        xx = self.x + self.x0
        print("abs_position() = {}".format(xx))
        return dict(x=xx)
            
    def position(self):
        xx = self.x 
        print("position() = {}".format(xx))
        return dict(x=xx)
    
    def set_reference(self):
        print("set_reference()")
        self.x0 = self.x + self.x0
        self.x = self.x0
        
    def home(self, eixo, sinal):
        print("home({}, {})".format(eixo, sinal))

    def set_abs_reference(self):
        print("set_abs_reference()")
        self.x0 = 0.0
    
    def stop(self):
        print("stop()")
    
    def clear(self):
        print("clear()")
        
    def step_motor(self):
        print("step_motor()")
        self.step = False
        
    def step_encoder(self):
        print("step_encoder()")
        self.step = True
    
    def waitUntilDone(self, wait=0.01):
        print("waitUntilDone()")
        
    
    def disconnect(self):
        """Desconecta o programa do terminal"""
        print("disconnect()")

        return None
    def ping(self):
        """
        Dando sinal de vida...
        """
        return 123



    
