# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 18:10:11 2016

@author: Administrator
"""
import numpy as np
from matplotlib import pyplot as plt
from math import cos, sin, pi
g0=9.8
R = 6.3e6

class Cannon_shell(object):
    '''This is the cannon shell without air resistance'''
    def __init__(self, v, tha, h=0):
        self.v = v
        self.tha = tha
        self.vx = self.v*cos(self.tha)
        self.vy = self.v*sin(self.tha)
        self.x = 0
        self.y = h
        self.xl = [0]
        self.yl = [h]
    
    def iterate(self, dt):
         self.vy = self.vy - g0*dt
         self.x = self.x + self.vx*dt
         self.y = self.y + self.vy*dt
        
    def calculate(self):
        while (1):
            self.iterate(0.1)
            if self.y < 0:
                r = -self.yl[-1]/self.y
                xz = (self.xl[-1] + r*self.x)/(r + 1)
                self.xl.append(xz)
                self.yl.append(0)
                break
            self.xl.append(self.x)
            self.yl.append(self.y)
        return xz
    def draw(self):
        plt.plot(self.xl, self.yl)
        
    def reset(self, v, tha, h=0):
        self.v = v
        self.tha = tha
        self.vx = self.v*cos(self.tha)
        self.vy = self.v*sin(self.tha)
        self.x = 0
        self.y = h
        self.xl = [0]
        self.yl = [h]
        

class Cannon_aire(Cannon_shell):
    ''' This is the cannon shell with air resistance and ignoring the air density'''
    def __init__(self, v, tha, b2=4e-5, h=0):
        super(Cannon_aire, self).__init__(v, tha, h)
        self.b2 = b2 # b2 = B2/m
    def iterate(self, dt):
        self.vx = self.vx - self.b2*self.v*self.vx*dt
        self.vy = self.vy - g0*dt - self.b2*self.v*self.vy*dt
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt
        self.v = (self.vx**2 + self.vy**2)**0.5
        
    def reset(self, v, tha, b2=4e-5,h=0):
        super(Cannon_aire,self).reset(v, tha, h)
        self.b2 = b2
        
        
class Cannon_aire_alt(Cannon_aire):
    '''This is the cannon shell with air resistance.The air density and gravity g varies with the altitude.In fact, the change of g can be ignored...'''
    def iterate1(self, dt):
        ro = (1 - 6.5e-3*self.y/300)**2.5
        self.b2 = self.b2*ro
        self.vx = self.vx - self.b2*self.v*self.vx*dt
        self.vy = self.vy - g0*dt - self.b2*self.v*self.vy*dt
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt
        self.v = (self.vx**2 + self.vy**2)**0.5
        
    def iterate2(self, dt):
        g  = g0*(R/(self.y+R))**2
        ro = (1 - 6.5e-3*self.y/300)**2.5
        self.b2 = self.b2*ro
        self.vx = self.vx - self.b2*self.v*self.vx*dt
        self.vy = self.vy - g*dt - self.b2*self.v*self.vy*dt
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt
        self.v = (self.vx**2 + self.vy**2)**0.5
        
    def calculate(self, ch_g=False):
        if ch_g == False:
            iterate = self.iterate1
        else:
            iterate = self.iterate2
            
        while (1):
            iterate(0.1)
            if self.y < 0:
                r = -self.yl[-1]/self.y
                xz = (self.xl[-1] + r*self.x)/(r + 1)
                self.xl.append(xz)
                self.yl.append(0)
                break
            self.xl.append(self.x)
            self.yl.append(self.y)
        return xz
    

a = Cannon_shell(700, pi/6)
b = Cannon_aire(700, pi/6, 4e-5)
c = Cannon_aire_alt(700, pi/6, 4e-5)
d = Cannon_aire_alt(700, pi/6, 4e-5)
a.calculate()
b.calculate()
c.calculate()
d.calculate(ch_g = True)

plt.plot(a.xl, a.yl, label = "No air resistance",lw=1.5)
plt.plot(b.xl, b.yl, label = "With airresistance",lw=1.5)
plt.plot(c.xl, c.yl, label = "Consider density", lw=1.5)
plt.plot(d.xl, d.yl, label = "With g changed", lw=1.5)
plt.legend(loc=1,bbox_to_anchor=(1.12,1)) 
plt.xlabel("x/m")
plt.ylabel("y/m")

cannonl = [a, b, c, d]
def compare():
    fig = plt.figure(figsize=(15,8))
    for i in range(4):
         fig.add_subplot(220+i+1)
         
    for tha in (pi/3, pi/6, pi/4, pi/5):
        thaa = tha/pi*180
        for i in range(4):
            cannonl[i].reset(700,tha)
            cannonl[i].calculate()
            fig.axes[i].plot(cannonl[i].xl, cannonl[i].yl,label="$%d^\circ$" %thaa)
            fig.axes[i].set_ylim(0, 20000)
            fig.axes[i].set_xlim(0, 50000)
            fig.axes[i].set_xlabel('x/km')
            fig.axes[i].set_ylabel('y/km')
    fig.axes[0].set_title("Without air resistance")    
    fig.axes[1].set_title("With air resistance ignore density") 
    fig.axes[2].set_title("Consider density")
    fig.axes[3].set_title("Consider change of g")
    for ax in fig.axes:
        ax.legend()
    fig.tight_layout()
    
def cp_thax():
    def find_tha(m):
        xll = []
        thal = np.arange(0, pi/2, 0.01)
        for tha in thal:
            m.reset(700, tha)
            xl = m.calculate()
            xll.append(xl)
        xlmax = max(xll)
        d = dict(zip(xll, thal))
        return (thal, xll, d[xlmax])
    fig, ax = plt.subplots()
    for ca in cannonl[:3]:
        z = find_tha(ca)
        ax.plot(z[0], z[1])
        ax.set_xlabel(r"$\theta/rad$")
        ax.set_ylabel("$x_{max}$")
        th = z[2]/pi*180
        print "Angle that make x max is %.2f" %th
    
    l1,l2,l3 = ax.lines
    plt.legend((l1,l2,l3), ("No air resist", "air resist","consider density"), loc=1, bbox_to_anchor=(1.1,1.1))

#compare()
cp_thax()


