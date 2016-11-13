# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 18:33:14 2016

@author: Administrator
"""
from math import sin, pi
from visual import *
from traits.api import HasTraits, Float, Button, Bool
from traitsui.api import View, Item
import ch

ch.set_ch()
l=9.8
g=9.8
q=0.5


class NLpendulum(HasTraits):
    
    iFD=Float(1.2)
    iWD=Float(2.0/3)
    
    start_button = Button("Start animation")
    ready = Bool(False)
    view = View(
    Item("iFD", label= u'驱动力'),Item("iWD", label = u"周期"),Item("start_button", label=u'开始')
    ,title=u"控制面板",kind = "livemodal")
        
    def __init__(self, the0=0.2, w0=0, *args, **kwargs):
        super(NLpendulum, self).__init__(*args, **kwargs)
        self.the = the0
        self.w = w0
        self.traj_the = [self.the]
        self.traj_w = [self.w]
        self.b_the = []
        self.tl = [0]
        self.init_scene()


        
    def init_scene(self):        
        self.Pe=frame(pos=(0,0,0))
        self.base=box(pos=(0,0,0), size=(2, 0.1,2))
        self.Shaft = box(axis = (4, 0, 0), pos=(2, 0, 0), size=(4, 0.02, 0.02) ,color=(0,1,0), frame=self.Pe)
        self.Mass = sphere(pos=(4+0.1, 0, 0), radius=0.1,frame=self.Pe,color=(1,0,0))
        self.Pe.axis = vector(sin(self.the), -cos(self.the), 0)
     
        
    def calculate(self, step_T=100, dur_T = 500, demo=False):
        if demo == True:
            self.FD=self.iFD
            self.WD = self.iWD
        self.t=0
        self.T=2*pi/(self.WD)
        dt = self.T/step_T
        for i in range(dur_T*step_T):
         
            if demo == True:
                rate(2/dt)
     
            self.w = self.w-(g*sin(self.the)/l + q*self.w - self.FD*sin(self.WD*self.t))*dt
            self.the = self.the + self.w*dt
    
            if self.the > pi:
                self.the = self.the - 2*pi
            elif self.the < -pi:
                self.the = self.the + 2*pi
            if demo == True:
                self.Pe.axis = vector(sin(self.the), -cos(self.the), 0)

         
            self.t = dt*i
            self.traj_the.append(self.the)
            self.traj_w.append(self.w)
            self.tl.append(self.t)
            if self.t/self.T >300 and self.t%self.T< 10e-10:
                self.b_the.append(self.the)
            
        
    def _start_button_fired(self):
        
        self.reset(FD=self.iFD, WD=self.iWD) 
        self.calculate(demo=True)
   
        
    def reset(self, the0=0.2, w0=0, FD=1.2, WD=2.0/3):
        self.the = the0
        self.w = w0
        self.FD = FD
        self.traj_the = [self.the]
        self.traj_w = [self.w]
        self.b_the = []
        self.tl = [0]
        self.WD=WD
                
                
a= NLpendulum()
a.configure_traits()




        