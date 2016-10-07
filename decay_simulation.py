# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 22:11:35 2016

@author: Administrator
"""

import matplotlib.pyplot as plt
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy
from scipy import integrate
import numpy as np

class Decay_nulceu(object):
    
    def __init__(self, Nai, Nbi, dt, dur):
        self.Na = Nai
        self.Nb = Nbi
        self.dt = dt
        self.Nal = [Nai]
        self.Nbl = [Nbi]
        self.t = [0]
        self.dur = dur
        self.nstep = int(self.dur//dt)
        self.fig, self.ax = plt.subplots()
        self.ax.set_ylabel("Number of every type of nucleus")
        self.ax.set_xlabel("time $s$")
        self.ax.set_xlim(0,self.dur)
        self.ax.set_ylim(min((Nbi, Nai)), max((Nbi,Nai)))
        self.lineA, = self.ax.plot([],[], label="Number of A nucleus", lw=1.5)
        self.lineB, = self.ax.plot([],[], label="Number of B nucleus", lw=1.5)
        self.ax.legend()
        self.ax.set_title("Decay simulation")
        
    def calculate(self):
        for i in range(0, self.nstep):
            dNa = self.Nb-self.Na
            dNb = self.Na-self.Nb
            
            self.Na += dNa*self.dt
            self.Nb += dNb*self.dt
            
            self.Nal.append(self.Na)
            self.Nbl.append(self.Nb)
            self.t.append((i+1)*self.dt)

    def calculate1(self):
        def equ(init, t):
            Na, Nb = init
            return [Nb-Na ,Na-Nb]
            
        self.t = np.arange(0, self.dur, self.dt)
        result = integrate.odeint(equ, (self.Na, self.Nb), self.t)
        self.Nal = result[:,0]
        self.Nbl = result[:,1]
        
    def show(self):
       self.lineA.set_data(self.t, self.Nal)
       self.lineB.set_data(self.t, self.Nbl)
       self.fig.canvas.draw()
       plt.show()
 
    def update(self, it):
        f = 1//self.dt
        t = int(it*f)
        self.lineA.set_data(self.t[:t], self.Nal[:t])
        self.lineB.set_data(self.t[:t], self.Nbl[:t])
        return mplfig_to_npimage(self.fig)
          
    def make_gif(self):
        animation =mpy.VideoClip(self.update, duration=self.dur)
        animation.write_gif("Decay_simulation.gif", fps=1//self.dt)
        
if __name__ == "__main__":
    a = Decay_nulceu(100, 0, 0.1, 10)
    a.calculate1()
    a.make_gif()

        