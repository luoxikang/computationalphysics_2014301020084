# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:34:15 2016

@author: Administrator
"""

import numpy as np
from matplotlib import pyplot as plt
from math import cos, sin, pi, sqrt, tan
from  cannon_shell import Cannon_shell
from scipy import stats

g=9.8     
        
class Cannon_shot(object):
    
    def __init__(self, vw=0, b2=4e-5, h=0, target=()):
            self.b2 = b2
            self.x = 0
            self.h = h
            self.y = h
            self.xl = [0]
            self.yl = [h]
            self.vw=vw
            self.tx, self.ty = target
            
    def iterate(self, dt):
        ro = (1 - 6.5e-3*self.y/300)**2.5
        self.b2 = self.b2*ro
        rx = self.vx-self.vw
        self.vx =self. vx - self.b2*(rx**2+self.vy**2)**0.5*rx*dt
        self.vy = self.vy - g*dt - self.b2*(rx**2+self.vy**2)**0.5*self.vy*dt
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt
        
    def find(self, the, dt):
        self.the=the
        vi=(self.tx/cos(the))*sqrt(g/(2*(self.tx*tan(the)-self.ty+self.h)))
        v=vi
        self.reset(self.vw, h=self.h, target=(self.tx, self.ty))
        while v < 1500:
           self.vx = v*cos(the)
           self.vy = v*sin(the)
           while(1):
              self.iterate(dt)
              if self.y < self.ty and self.y-self.yl[-1]<0:
                  self.x, self.y=self.xl[-1], self.yl[-1]
                  self.iterate(0.0001)
                  if self.y < self.ty:
                      xz = (self.ty-self.yl[-1])*(self.x-self.xl[-1])/(self.y-self.yl[-1]) + self.xl[-1]
                      if abs(xz-self.tx) < 5:
                          self.xl.append(xz)
                          self.yl.append(self.ty)
                          print "found, v is %.3f, hit on (%d, %d)" %(v, xz, self.ty)
                          self.v=v
                          return [v, xz, self.ty]
                      else:
                          self.reset(self.vw, h=self.h, target=(self.tx,self.ty))
                          break
              self.xl.append(self.x)
              self.yl.append(self.y)
           v = v+0.05 
           print v
           
    def calculate(self ,v, the, vw, dt):
        self.reset(vw, h=self.h, target=(self.tx,self.ty))
        self.vx=v*cos(the)
        self.vy=v*sin(the)
        while (1):
            self.iterate(dt)
            if self.y < self.ty and self.y-self.yl[-1]<0:
                self.x, self.y=self.xl[-1], self.yl[-1]
                self.iterate(0.0001)
                if self.y < self.ty:
                     xz = (self.ty-self.yl[-1])*(self.x-self.xl[-1])/(self.y-self.yl[-1]) + self.xl[-1]
                     self.xl.append(xz)
                     self.yl.append(self.ty)
                     return xz-self.tx
                     break
            self.xl.append(self.x)
            self.yl.append(self.y)
        
    def reset(self, vw=0, b2=4e-5, h=0, target=()):
        self.b2 = b2
        self.x = 0
        self.y = h
        self.xl = [0]
        self.yl = [h]
        self.vw=vw
        self.tx, self.ty = target
        
    def get_err_uniform(self):
        v_err = np.random.uniform(self.v*0.95, self.v*1.05, 20)
        the_err = np.random.uniform(self.the-2*pi/180, self.the+2*pi/180, 20)
        vw_err = np.random.uniform(self.vw*1.1, self.vw*0.9, 20)
        
        self.c_err = zip(v_err, the_err, vw_err)
        r_err  = []
        fig, ax=plt.subplots()
        ax.set_title("Error obey uniform distribution")
        ax.set_xlabel("x/m")
        ax.set_ylabel('y/m')
        for v, the, vw in self.c_err:
            err=self.calculate(v, the, vw, 0.01)
            ax.plot(self.xl, self.yl)
            r_err.append(err)
        
        aver_err=sqrt(np.mean(np.array(r_err)**2))
        return aver_err
        
    def get_err_norm(self):
        v_err = stats.norm(loc=self.v, scale=self.v*0.05/3).rvs(size=20)
        the_err = stats.norm(loc=self.the, scale=2*pi/540).rvs(size=20)
        vw_err = stats.norm(loc=self.vw, scale=abs(self.vw*0.1/3)).rvs(size=20)
        
        self.c_err = zip(v_err, the_err, vw_err)
        r_err  = []
        fig, ax=plt.subplots()
        ax.set_title("Error obey normal distribution")
        ax.set_xlabel("x/m")
        ax.set_ylabel('y/m')
        for v, the, vw in self.c_err:
            err=self.calculate(v, the, vw, 0.01) 
            ax.plot(self.xl, self.yl)
            r_err.append(err)
        
        aver_err=sqrt(np.mean(np.array(r_err)**2))
        return aver_err
        


#a=Cannon_shell(500, pi/3)
#b=Cannon_shot(vw=-100, h=0, target=(100000, 0))
#a.calculate(0.1)
#b.calculate(500, pi/3, -100, 0.01)
#plt.plot(a.xl, a.yl,label='no resistance')
#plt.plot(b.xl, b.yl,label='resistance')
#plt.xlabel('x/m')
#plt.ylabel('y/m')
#plt.legend()

a=Cannon_shot(vw=-100, h=1000, target=(100000, 4000))
c=a.find(pi/4, 0.01)

print 'average error from normal distribution: %.1fm' %a.get_err_norm()
print 'average error from uniform distribution: %.1fm' %a.get_err_uniform()



