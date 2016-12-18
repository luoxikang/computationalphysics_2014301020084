# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 20:13:15 2016

@author: Administrator
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy
from math import sin, pi
class Wave(object):
    
    def __init__(self, lenth = 1, dx = 0.01, c=300):
        self.ylp = np.zeros(lenth/dx)
        self.ylc = self.ylp.copy()
        self.yln = self.ylp.copy()
        self.dx = dx
        self.dt = dx/c
        self.xl = np.arange(0, lenth, dx)
        self.xnum = lenth/dx
        
        self.c0 = c
        
    def init_condi(self):
        self.ylp = np.exp(-1000*(self.xl-0.3)**2)
        self.ylc = self.ylp.copy()
        self.yarl = [self.ylc]
        
    def calculate(self, n=1000):
        self.tl = []
        self.dpol = []
        for j in range(n):
            i=1
            
            while i < self.xnum-1:
                if i < self.xnum/2:
                    self.c = self.c0
                else:
                    self.c = self.c0/2
                    
                self.r = self.c*self.dt/self.dx    
                self.yln[i]=2*(1-self.r**2)*self.ylc[i]-self.ylp[i]+self.r**2*(self.ylc[i+1]+self.ylc[i-1])
         
                i+=1
            
#            self.ylc[0] = 0.5*sin(2*pi*j*self.dt/0.001)
#            self.yln[0] = 0.5*sin(2*pi*j*self.dt/0.001)
            self.yarl.append(self.yln.copy())
            self.tl.append(j*self.dt)
            self.dpol.append(self.yln[4])
            self.ylp = self.ylc.copy()
            self.ylc = self.yln.copy()
            
    

a = Wave()
a.init_condi()  
a.calculate()

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.set_xlim(0, 1)
ax1.set_ylim(-1, 1)
ax1.set_xlabel("x/m")
ax1.set_ylabel("y/m")
ax2.set_xlim(0, a.tl[-1])
ax2.set_ylim(-1, 1)
ax2.set_xlabel("t/s")
ax2.set_ylabel("signal")
wave, = ax1.plot([], [],lw=2)
signal, = ax2.plot([], [])
it=0
def update(t):
    global it

    wave.set_data(a.xl, a.yarl[it])
    

    signal.set_data(a.tl[:it], a.dpol[:it])
    it+=1

    return mplfig_to_npimage(fig)

animation =mpy.VideoClip(update, duration=5)
animation.write_gif("wave.gif", fps=20)

ft = np.fft.rfft(a.dpol[:512])/512

ftp = np.abs(ft)

freq = np.linspace(0, 1.0/(2*a.dt), 257)

fig, ax = plt.subplots(1)
ax.set_xlim(0, 3000)
ax.plot(freq,ftp)
ax.set_xlabel("frequency(Hz)")
ax.set_ylabel("Power")
ax.set_title("Power spectra")