# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 16:33:10 2016

@author: lss
"""
from cython cimport cdivision, boundscheck, wraparound
from libc.math cimport sin
from math import pi
import matplotlib.pyplot as plt
import numpy as np
l=9.8
g=9.8
q=0.5


cdef class NLpendulum(object):
    cdef:
        double the, w, FD, WD, t, T
        public list traj_the, traj_w, b_the, tl
         
    def __cinit__(self, the0=0.2, w0=0, FD=1.2, WD=2.0/3):
    
        self.the = the0
        self.w = w0
        self.traj_the = [self.the]
        self.traj_w = [self.w]
        self.b_the = []
        self.tl = [0]
        self.FD=FD
        self.WD = WD
        self.t=0
    
  
  
    cpdef calculate(self, int step_T=100, int dur_T = 500):
        cdef double dt 
        self.t=0
        self.T=2*pi/(self.WD)
        dt = self.T/step_T
        for i in range(dur_T*step_T): 
            self.w = self.w-(g*sin(self.the)/l + q*self.w - self.FD*sin(self.WD*self.t))*dt
            self.the = self.the + self.w*dt
    
            if self.the > pi:
                self.the = self.the - 2*pi
            elif self.the < -pi:
                self.the = self.the + 2*pi
            self.t = dt*i
            self.traj_the.append(self.the)
            self.traj_w.append(self.w)
            self.tl.append(self.t)
            if self.t/self.T >300 and self.t%self.T< 0.0001:
                self.b_the.append(self.the)
             
        
    cpdef reset(self, the0=0.2,  w0=0, FD=1.2, WD=2.0/3):
        self.the = the0
        self.w = w0
        self.FD = FD
        self.traj_the = [self.the]
        self.traj_w = [self.w]
        self.b_the = []
        self.tl = [0]
        self.WD=WD
    