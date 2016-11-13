# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 08:51:39 2016

@author: lss
"""

import os 
import time
import numpy as np


class Character_IMG(object):
    
    def __init__(self, s):
        self.size = s
        self.row = "."*self.size
        self.columns = [self.row]*self.size
        self.matrix = [list(row) for row in self.columns]
        self.xlist = []
        self.ylist = []
        
    def plot(self, x, y):
        if max(x) <= self.size and min(x)>= 0 and max(y) <= self.size and min(y)>=0:
            ufunc_int = np.vectorize(int)
            self.xlist = ufunc_int(x)
            self.ylist = ufunc_int(y)
            for xi,yi in zip(self.xlist, self.ylist):
                self.matrix[yi][xi] = "0"
            self.columns = ["".join(every_row) for every_row in self.matrix]
        else:
            print "Your coordinate is out of the range"
        self.show()    
        
    def show(self):
        img = "\n          ".join(self.columns)
        print "          "+img
        
    def movex(self, step):
        for i in range(len(self.columns)):
            self.columns[i] = " "*step + self.columns[i]
        self.show()
        
    def movey(self, step):
        print "\n"*step
        self.show()
        
    def rotate(self):
        self.matrix = map(list, zip(*self.matrix))
        self.columns = ["".join(every_row) for every_row in self.matrix]
        self.show()
        
    def reset(self):
        self.row = "."*self.size
        self.columns = [self.row]*self.size
        self.matrix = [list(row) for row in self.columns]
        
        
if __name__ == "__main__":
    def demo():
        img = Character_IMG(80)
        t = np.arange(0, 2*np.pi, 0.01)
        x = 8*(2*np.sin(t)-np.sin(2*t)) + 35
        y = -8*(2*np.cos(t)-np.cos(2*t)) + 35
        img.plot(x,y)
        time.sleep(1)
        for i in range(20):
           img.movex(1)
           time.sleep(0.1)
           c = os.system('clear')
        img.movey(10)
        img.rotate()
        img.reset() 
        img.show()
        
    demo()
    
    
    
    
    
    
    
    
    