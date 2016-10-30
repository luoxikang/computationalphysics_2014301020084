# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 18:33:14 2016

@author: Administrator
"""
from math import sin, pi
import matplotlib.pyplot as plt
import ch
ch.set_ch()
WD=2.0/3
l=9.8
g=9.8
q=0.5


class Poincare_section(object):
    def __init__(self, the0=0.2, w0=0, FD=1.2, nt=0):
        self.the = the0
        self.w = w0
        self.FD = FD
        self.traj_the = [self.the]
        self.traj_w = [self.w]
        self.poi_the = [self.the]
        self.poi_w = [self.w]
        self.tl = [0]
        self.nt=nt
        
    def calculate(self, dt = 0.04, dur = 400):
        self.t=0
        for i in range(int(dur/dt)):
            self.w = self.w-(g*sin(self.the)/l + q*self.w - self.FD*sin(WD*self.t))*dt
            self.the = self.the + self.w*dt
            if self.the > pi:
                self.the = self.the - 2*pi
            elif self.the < -pi:
                self.the = self.the + 2*pi
            self.t = self.t+dt
            self.traj_the.append(self.the)
            self.traj_w.append(self.w)
            self.tl.append(self.t)
            n = self.t*WD/(2*pi)-self.nt/2
            if abs(n-round(n)) < 0.001:
                self.poi_the.append(self.the)
                self.poi_w.append(self.w)
                
a = Poincare_section()
a.calculate(dur=16000)
b = Poincare_section(nt=0.5)
c = Poincare_section(nt=0.25)

b.calculate(dur=16000)
c.calculate(dur=16000)

plt.plot(a.poi_the, a.poi_w, '.', label=u"周期开始") 
plt.plot(b.poi_the, b.poi_w, '.', label=u'$\frac{1}{4}$周期') 
plt.plot(c.poi_the, c.poi_w, '.', label=u'$\frac{1}{8}$周期') 
plt.legend()
plt.xlabel(r'$\theta/rad$')
plt.ylabel(r'$\omega/rad*s^-1$')
plt.title(u"演化时间16000s庞加莱截面")

        