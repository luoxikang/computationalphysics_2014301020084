# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 16:41:55 2016

@author: Administrator
"""
from visual import *
import matplotlib.pyplot as plt
import numpy as np


class Stadium_billiard(object):
    def __init__(self, a=0.5, y=1):
        self.pxl=[]
        self.pvl=[]
        self.xl=[]
        self.yl=[]
        self.t = []
        self.a=a
        self.y=y
    
    def ani(self, demo=False, dur=1000):
        l=self.a*10
        cr2 = shapes.arc(pos=(0, l), radius=10, angle1=0, np=50 , angle2=pi)
        cr1 = shapes.arc(pos=(0, -l), radius=10, angle1=0, np=50, angle2=-pi)
        l1 = shapes.line(start=(10, l), end=(10,-l), np=20, thickness=0.1)
        l2 = shapes.line(start=(-10, l), end=(-10, -l), np=20,thickness=0.1)
        extrusion(shape=cr1+cr2+l1+l2)
        ball = sphere(pos=(0, self.y, 0), radius=0.2, make_trail=True, color=(0, 1, 0))
        ball.trail_object.radius = 0.05
        ball.v = vector(0.4, 0.4, 0.4)
    
        dt=0.2
        t=0.0

        
        cir1c = vector(0, l, 0)
        cir2c = vector(0, -l, 0)
        while t< dur:
            if demo == True:
                rate(1000)
            t = t + dt
            ball.pos = ball.pos + ball.v*dt
            self.xl.append(ball.pos.x)
            self.yl.append(ball.pos.y)
            self.t.append(t)
            if abs(ball.pos.y) < 0.05:
                self.pxl.append(ball.pos.x)
                self.pvl.append(ball.v.x)
    
            if l > ball.pos.y > -l:
                nvector = ball.pos - vector(0, ball.pos.y, 0)
                if not (nvector.mag < 10):
                    ang = diff_angle(nvector, -ball.v)
                    ball.v = -ball.v.rotate(2*ang, cross(-ball.v, nvector))
            elif ball.pos.y > l:
                nvector = ball.pos-cir1c
                if not (nvector.mag < 10):
                    ang = diff_angle(nvector, -ball.v)
                    ball.v = -ball.v.rotate(2*ang, cross(-ball.v, nvector))
            else:
                nvector = ball.pos-cir2c
                if not (nvector.mag < 10):
                    ang = diff_angle(nvector, -ball.v)
                    ball.v = -ball.v.rotate(2*ang, cross(-ball.v, nvector))
                
     
    



a = Stadium_billiard(a=0.5)
a.ani(demo=True, dur=10000)
plt.plot(a.pxl, a.pvl, '.')
plt.title(r"Stadium Billiard:$\alpha=0.1$")
plt.xlabel('x')
plt.ylabel('vx')
plt.xlim(-10, 10)

#a = Stadium_billiard(a=0.1)
#b = Stadium_billiard(a=0.1, y=1.00001)
#a.ani()
#b.ani()
#
#dis = np.abs(np.array(a.yl)-np.array(b.yl))
#
#fig = plt.figure(figsize=(10,5))
#ax1 = fig.add_subplot(121)
#ax2= fig.add_subplot(122)
#
#ax1.plot(a.xl, a.yl, color='r', label='ball a')
#ax1.plot(b.xl, b.yl, label='ball b')
#ax1.set_xlabel('x')
#ax1.set_ylabel('y')
#ax1.set_title('Two trajectories')
#ax1.legend()
#
#ax2.plot(a.t, dis)
#ax2.set_yscale('log')
#ax2.set_xlabel('time')
#ax2.set_ylabel('separation')
#ax2.set_title(r"$\alpha=0.1$, divergence of two trajectories")
#plt.tight_layout()