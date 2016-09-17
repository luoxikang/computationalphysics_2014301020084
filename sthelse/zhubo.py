# -*- coding: utf-8 -*-
"""
Created on Fri Oct 02 16:55:02 2015

@author: Administrator
"""

import numpy as np
from numpy import cos,pi
import matplotlib.pyplot as plt
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy
import ch
ch.set_ch()
y1 = np.r_[-20:-5:200j]
y2 = np.r_[5:20:200j]

fig,(ax1,ax2) = plt.subplots(2,1)

A=1.
w=pi 
v=1. 
t=0.
x1 = A*cos(w*(t-y1/v))
x2 = A*cos(w*(t+y2/v))

line1, = ax1.plot(y1, x1,lw=2)
line2, = ax1.plot(y2, x2,lw=2)
ax1.set_ylim(-2, 2)
ax1.set_xlim(-10, 10)
ax1.set_title(u'两列相干波')
line3, = ax2.plot([],[],lw=2,color='r')
ax2.set_xlim(-10,10)
ax2.set_ylim(-3, 3)
ax2.set_title(u'驻波形成')
fig.show()


def update(t):
    global y1,y2
    t=t*1.5
    y11 = y1+t*v 
    x11 = A*cos(w*(t-y11/v))
    y22 = y2-t*v
    x22 = A*cos(w*(t+y22/v))
    line1.set_data(y11, x11)
    line2.set_data(y22, x22)
    if y11.max() > y22.min() and y22.max() > y11.min():
        if y22.min() < y11.min():
            y3 = np.linspace(y11.min(), y22.max(),200)
        else: 
            y3 = np.linspace(y22.min(), y11.max(),200)
#    else:
#        y3 = np.array([])
#        print y3
        line3.set_data(y3,  A*cos(w*(t-y3/v))+A*cos(w*(t+y3/v)))
    return mplfig_to_npimage(fig)
    
animation =mpy.VideoClip(update, duration=15)
animation.write_gif("zhub.gif", fps=20)
    
    
    
    
   