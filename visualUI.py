# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 21:49:53 2016

@author: Administrator
"""

from visual import *
from math import pi , sin , cos
import threading
import numpy as np
from traits.api import *
from traitsui.api import *


class VisualUI(HasTraits):
    

    iR = Float(1.)
    iLS = Float(4.)
    ig = 9.8
    itha = Range(0,pi/2, pi/12)
    ithadot = Float(0)
    iphi = Float(0)
    iphidot = Float(0)
    iw = Float(3)
    
    R, LS, g, tha, thadot, phi, phidot, w = iR,iLS, ig, itha.get_default_value()[1],ithadot,iphi, iphidot, iw
    
    ready = Bool(False)
    start_button = Button("Go")
    
    view = View(
    Item("iR"),Item("iLS"),Item("ithadot"),Item("iphi"), Item("iphidot"),Item("iw"),Item("itha"),Item("start_button")
    ,title=u"控制面板",kind = "livemodal")   
    
    def __init__(self, *args, **kwargs):
        super(VisualUI, self).__init__(*args, **kwargs)
        self.init_scene()
        self.lock = threading.Lock()
        
    def init_scene(self):
        
        self.k=frame(pos=(0,0,0))
        self.Pe = frame(pos=(self.R,0,0),frame=self.k)
        self.Shaft = cylinder(axis = (self.LS, 0, 0), length = self.LS, radius=0.02,frame=self.Pe, color=(0,1,0))
        self.Mass = sphere(pos=(self.LS+0.1, 0, 0), radius=0.1,frame=self.Pe,color=(1,0,0))
        self.Pe.axis = vector(sin(self.tha)*cos(self.phi), -cos(self.tha), sin(self.tha)*sin(self.phi))
        self.alpha = np.linspace(0, 2*pi, 100)
        self.poss = np.array([self.R*np.sin(self.alpha), self.alpha*0 ,self.R*np.cos(self.alpha)])
        self.track = curve(pos=self.poss.T, radius = 0.02)
        self.trail = curve(radius = 0.015,color=(1,1,0))
        
        self.dt = 0.001
     
        
    def animation(self):
        self.R, self.LS, self.g, self.tha, self.thadot, self.phi, self.hidot, self.w = self.iR, self.iLS, self.ig, self.itha, self.ithadot, self.iphi, self.iphidot, self.iw
        
        while self.ready:
            rate(1/self.dt)
            self.lock.acquire()
            aphi = (2*(self.w-self.phidot)*cos(self.tha)*self.thadot - self.w*self.w*self.R*sin(self.phi)/self.LS)/sin(self.tha)
            
            atha = 0.5*(self.phidot-self.w)**2*sin(2*self.tha) + self.w*self.w*self.R*cos(self.tha)*cos(self.phi)/self.LS - self.g*sin(self.tha)/self.LS
            
            self.thadot = self.thadot + atha*self.dt
            self.phidot = self.phidot + aphi*self.dt
            
            self.tha = self.tha + self.thadot*self.dt
            self.phi = self.phi + self.phidot*self.dt
            
            self.k.rotate(axis=(0,1,0), angle = self.w*self.dt)
            self.Pe.axis = vector(sin(self.tha)*cos(self.phi), -cos(self.tha), sin(self.tha)*sin(self.phi))
            
            pos1 = self.Pe.frame_to_world(self.Mass.pos)
            pos2 = self.k.frame_to_world(pos1)
            self.trail.append(pos2)
            self.lock.release()
            
    def start_animation(self):

        self.thread = threading.Thread(None, self.animation)
        self.thread.start()
        
    def end_animation(self):
        self.ready = False
        self.thread.join()
        
    def _start_button_fired(self):
        self.ready = True
        self.start_animation()
        
    @on_trait_change("iR,iLS, ig, itha,ithadot,iphi, iphidot, iw")
    def pause(self):
        self.lock.acquire()
        self.ready = False
        self.trail.pos = np.array([])
        self.lock.release()
      
        
#class visualUIHandler(Handler):
#     def closed(self, info, is_ok):
#        info.object.end_animation()
     
demo = VisualUI()
demo.configure_traits()