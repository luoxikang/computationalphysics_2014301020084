# -*- coding: utf-8 -*-
"""
Created on Sat Dec 03 20:52:38 2016

@author: Administrator
"""
import numpy as np
import matplotlib.pyplot as plt
from math import pi, cos, sin
from visual import *
import ch
ch.set_ch()

class Hyperion(object):
    def __init__(self, r=1.0, v=2*pi, the=0):

        self.vxl=[0]
        self.vyl=[v]
        self.xl=[r]
        self.yl=[0]
        self.tl=[0]
        self.thel=[the]        
        self.vthel=[0]
        self.init_scene()

    def init_scene(self):
        self.Pe = frame(pos=(self.xl[0], 0, 0))
        self.saturn = sphere(pos=(0,0,0),radius=0.2, color=(1, 0, 0))
#        self.mc = sphere(pos=(0,0,0), frame=self.Pe, radius=0.01, make_trail=True, visible=False)
        self.m1 = sphere(pos=(0.1, 0, 0), frame=self.Pe, radius=0.05, color=(1,1,0))
        self.m2 = sphere(pos=(-0.1, 0, 0), frame=self.Pe, radius=0.05,color=(0,1 ,1))
        self.shaft = cylinder(pos=(-0.1, 0, 0), axis=(0.2,0 ,0), lenth=0.2, radius=0.005,frame=self.Pe, color=(0,1,0))
        self.trail1 = curve(color=(1,1,0), radius=0.005)
        self.trail2 = curve(color = (0,1,1),radius=0.005)
        
    def caculate(self, dt = 0.0001, step=100000, demo=False):
        self.vx=self.vxl[0]
        self.vy=self.vyl[0]
        self.x=self.xl[0]
        self.y=self.yl[0]
        self.the = self.thel[0]
        self.vthe = self.vthel[0]
        self.t = 0
        for i in range(step):
            if demo == True:
                rate(300)
            self.r = (self.x**2+self.y**2)**0.5
            self.vx = self.vx - 4*pi**2*self.x/self.r**3*dt
            self.vy = self.vy - 4*pi**2*self.y/self.r**3*dt
            self.vthe += -12*pi**2*(self.x*sin(self.the)-self.y*cos(self.the))*(self.x*cos(self.the)+self.y*sin(self.the))/self.r**5*dt
            self.x = self.x + self.vx*dt
            self.y = self.y + self.vy*dt
            self.the += self.vthe*dt
            if demo == True:
                self.Pe.pos = (self.x, self.y, 0)
                self.m1.pos = (0.1*cos(self.the), 0.1*sin(self.the), 0)
                self.m2.pos = -self.m1.pos
                self.shaft.pos = self.m2.pos
                self.shaft.axis=(0.2*cos(self.the), 0.2*sin(self.the), 0)
                pos1 = self.Pe.frame_to_world(self.m1.pos)
                pos2 = self.Pe.frame_to_world(self.m2.pos)
                self.trail1.append(pos1)
                self.trail2.append(pos2)
#            if self.the > pi:
#                self.the = self.the - 2*pi
#            elif self.the < -pi:
#                self.the = self.the + 2*pi
            self.t = self.t + dt
            self.tl.append(self.t)
            self.thel.append(self.the)
            self.vthel.append(self.vthe)
     

#a = Hyperion()
#a.caculate(dt=0.001, demo=True)

a = Hyperion() 
a.caculate()
b = Hyperion(the=0.01)
b.caculate()

dthe = np.abs(np.array(a.thel)-np.array(b.thel))
fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

c = Hyperion(v=4.6)
d = Hyperion(v=4.6, the=0.01)
c.caculate()
d.caculate()

dthe1 = np.abs(np.array(c.thel)-np.array(d.thel))
C, y0 = np.polyfit(c.tl[:60000], np.log10(dthe1[:60000]), 1)
t=np.arange(0, 6, 0.1)
ax1.plot(a.tl, dthe)
ax2.plot(c.tl, np.log10(dthe1))
ax2.plot(t, C*t+y0)
ax2.text(8, 1.2, 'v=5.0')
ax1.set_xlabel('time/hyr')
ax1.set_ylabel(r'$\Delta\theta$(radians)')
ax2.set_xlabel('time/hyr')
ax2.set_ylabel(r'$\Delta\theta$(radians)')
ax1.set_title(r'Circular orbit $\Delta\theta$ versus time')
ax2.set_title(r'Elliptical orbit $\Delta\theta$ versus time')
ax1.set_yscale('log')
#ax2.set_yscale('log')     