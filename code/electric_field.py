# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 18:06:55 2016

@author: Administrator
"""

import numpy as np
from mayavi import mlab 
import mpl_toolkits.mplot3d
import matplotlib.pyplot as plt

class Electric_field(object):
    
    def __init__(self):
        self.ar1=np.zeros((20,20))
        self.ar2=np.zeros((20,20))
       
        self.initfd()
        
        
    def initfd(self):
   
       self.ar1[6:14,6:14]=np.ones((8,8))
       self.ar2[6:14,6:14]=np.ones((8,8))
        
    def calculate(self, n=10):
        
        for k in range(n):        
            dv=0
            for i in np.arange(1,19):
                for j in np.arange(1,19):
                    if i in np.arange(6, 14) and j in np.arange(6,14):
                        continue
                    self.ar1[i,j]=(self.ar2[i+1,j]+self.ar2[i-1,j]+self.ar2[i,j+1]+self.ar2[i,j-1])/4
                    dv += abs(self.ar1[i,j]-self.ar2[i,j])
                    
                    if k > 4 and dv < 10e-5:
                        return self.ar1
            self.ar2 = self.ar1
                
    def calculate1(self, n=10):
        for k in range(n):        
            dv=0
            for i in np.arange(1,19):
                for j in np.arange(1,19):
                    if i in np.arange(6, 14) and j in np.arange(6,14):
                        continue
                    self.ar2 = self.ar1
                    self.ar1[i,j]=(self.ar1[i+1,j]+self.ar1[i-1,j]+self.ar1[i,j+1]+self.ar1[i,j-1])/4
                    dv += abs(self.ar1[i,j]-self.ar2[i,j])
                    
                    if k > 4 and dv < 10e-5:
                        return self.ar1
            
        

a = Electric_field()
e = Electric_field()

b=a.calculate1()
c=e.calculate()
d = b-c
x, y = np.ogrid[0:20:20j, 0:20:20j]
mlab.clf()
mlab.surf(x, y, d)
#mlab.outline()
