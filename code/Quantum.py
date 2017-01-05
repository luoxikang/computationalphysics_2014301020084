# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 13:44:14 2016

@author: Administrator
"""

import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab 
from math import pi

class Schrodinger(object):
    def __init__(self, dx=0.01,N=130):
        self.xl=np.zeros(N)
        self.nxl=[]
        self.e=0
        self.de=0.5
        self.b=2
        self.lastd=0
        self.lastc=1
        self.dx=dx
        
        
    def shooting_cal(self, v , symm=1, e=0, de=0.5):
        if symm == 1:
            self.xl[0]=1
            self.xl[1]=1
        elif symm == 0:
            self.xl[0]=-self.dx
            self.xl[1]=0
        else:
            raise ValueError("symm must be 1 or 0")
        self.v=v
        self.e=e
        self.de=de
        while abs(self.de) > 0.0001:
            for i in range(len(self.v)-1)[1:]:
                self.xl[i+1]=2*self.xl[i]-self.xl[i-1]-2*(self.e-self.v[i])*self.dx**2*self.xl[i]
                if abs(self.xl[i+1]) > self.b:
                    self.di=i+1
                    break
            if self.lastd*self.xl[self.di] < 0:
                self.de=-self.de/2
            self.e=self.e+self.de
            self.lastd=self.xl[self.di]
            
##################show the process##################################
#            plt.plot(np.linspace(0,1.3, self.di),self.xl[0:self.di])
#            plt.title("The process of shooting method")
#            plt.xlabel("x")
#            plt.ylabel("$\Psi$")
####################################################################  
         
        if symm ==1:
            self.nxl=self.xl[1:self.di][::-1]
        elif symm == 0:
            self.nxl=-self.xl[1:self.di][::-1]
        self.fxl=np.hstack((self.nxl, self.xl[1:self.di]))
       
    def matching_cal(self,v, xm, e=0, de=0.5):
        self.v=v
        self.e=e
        self.de=de
        self.xml=xm
        self.xmr=-(len(self.xl)-xm)
        self.xr=np.copy(self.xl)
        self.xl[0]=-0.0001*self.dx
        self.xl[1]=0
        self.xr[-2]=0
        self.xr[-1]=0.0001*self.dx
        
        while abs(self.lastc) > 0.0000001:
            for i in range(self.xml+20)[1:]:
                self.xl[i+1]=2*self.xl[i]-self.xl[i-1]-2*(self.e-self.v[i])*self.dx**2*self.xl[i]
            
            for i in np.arange(2, abs(self.xmr)+20, 1):
             
                self.xr[-(i+1)]=2*self.xr[-i]-self.xr[1-i]-2*(self.e-self.v[-i])*self.dx**2*self.xr[-i]
             

            self.xr=self.xr/self.xr[self.xmr]
            self.xl=self.xl/self.xl[self.xml]
            dfl=self.xl[self.xml+1]-self.xl[self.xml-1]
            dfr=self.xr[self.xmr+1]-self.xr[self.xmr-1]
            print dfl, dfr

            
#################show the process##########################          
#            plt.plot(np.linspace(0.5, 5, 450)[:self.xml+20], self.xl[:self.xml+20])
#            plt.plot(np.linspace(0.5, 5, 450)[self.xmr-20:], self.xr[self.xmr-20:])
#            plt.title("The process of matching method")
#            plt.xlabel("x")
#            plt.ylabel("$\Psi$")
##############################################################           
            if self.lastc*(dfl-dfr) < 0:
                self.de=-self.de/2
            self.e=self.e+self.de
            print self.e
            self.lastc=dfl-dfr

        
       


        
    def vari_mc(self, v, fi0, n, dx):
        self.dx=dx
        if len(v.shape) == 1 and len(fi0.shape) == 1:
            self.v = v
            self.fi0=fi0
            self.N=len(self.v)
            self.fi0=self.fi0/np.sqrt(np.dot(self.fi0, self.fi0)*self.dx)
            self.v1=2*self.v*self.dx**2
            self.H=np.zeros((self.N, self.N))
            for i in range(self.N):
                self.H[i, i]=self.v1[i]+2
                if i == 0:
                    self.H[i, i+1]=-1
                elif i == self.N-1:
                    self.H[i, i-1]=-1
                else:
                    self.H[i, i+1]=-1
                    self.H[i, i-1]=-1
                    
            self.E=np.dot(self.fi0, np.dot(self.H, self.fi0))/(2*self.dx**2*np.dot(self.fi0, self.fi0))
            for j in range(n):
                i=np.random.randint(self.N)
                fip=np.copy(self.fi0)
                fip[i]=fip[i]+np.random.random()/50-0.01
                Ep=np.dot(fip, np.dot(self.H,fip))/(2*self.dx**2*np.dot(fip, fip))
                if Ep < self.E:
                    self.fi0=np.copy(fip)
                    self.E=Ep
                    
        elif len(v.shape) == 2 and len(fi0.shape) == 2:
            self.v=v.ravel(0)
            self.fi0=fi0.ravel(0)
            self.N=len(v)
            self.fi0=self.fi0/np.sqrt(np.dot(self.fi0, self.fi0)*self.dx**2)
            self.v1=2*self.v*self.dx**2
            self.H=np.zeros((self.N**2, self.N**2))
            for j in range(self.N):
                for i in range(self.N):
                    ii=j*self.N+i
                    self.H[ii,ii]=self.v1[ii]+4
                    if i == 0:
                        self.H[ii, ii+1]=-1
                    elif i == self.N-1:
                        self.H[ii, ii-1]=-1
                    else:
                        self.H[ii, ii+1]=-1
                        self.H[ii, ii-1]=-1
                        
                    if j == 0:
                        self.H[ii, ii+self.N]=-1
                    elif j == self.N-1:
                        self.H[ii, ii-self.N]=-1
                    else:
                        self.H[ii, ii+self.N]=-1
                        self.H[ii, ii-self.N]=-1
                        
            self.E=np.dot(self.fi0, np.dot(self.H, self.fi0))/(2*self.dx**2*np.dot(self.fi0, self.fi0))
            for j in range(n):
                i=np.random.randint(self.N**2)
                fip=np.copy(self.fi0)
                fip[i]=fip[i]+np.random.random()/5-0.1
                Ep=np.dot(fip, np.dot(self.H,fip))/(2*self.dx**2*np.dot(fip, fip))
                if Ep < self.E:
                    self.fi0=np.copy(fip)
                    self.E=Ep
            self.fi0 = self.fi0.reshape(self.N, self.N)      
            
        else:
            raise ValueError("V and f(x) must have same diension")
            
        
                

 
#############Shooting method###############################################      
#v1=np.hstack((np.zeros(100),np.ones(30)*1000))
#v=np.hstack((v1[::-1], v1))
#a=Schrodinger(N=130)
#a.shooting_cal(v1, symm=0, e=10, de=0.5)
#fig, ax=plt.subplots(1)
#ax.plot(np.linspace(-1.3,1.3,2*a.di-2),a.fxl)
#ax.plot(np.linspace(-1.3, 1.3, 260),v/700, '--')
#ax.set_ylim(-1.5, 1.5)
#ax.text(-0.1, 1.3, "E=%.3f" %a.e)
#ax.set_title(r"First excited odd-parity E=$2\pi^2=19.739$")
#ax.set_xlabel("x")
#ax.set_ylabel("$\Psi$")
##############################################################################


##########################Matching method L-J#################################
#x=np.linspace(0.5, 5,450)
#ljv=40*((1.0/x)**12-(1.0/x)**6)
#x_match=np.where(ljv==min(ljv))[0][0]
#
#plt.plot(x, ljv, '--')
#plt.ylim(-15, 11)
#
#a=Schrodinger(dx=0.01, N=450)
#a.matching_cal(ljv, x_match, e=3, de=0.5)
#
#plt.plot(x[:a.xml+20], a.xl[:a.xml+20]*5)
#plt.plot(x[a.xmr-20:], a.xr[a.xmr-20:]*5)
#plt.plot(x[x_match], a.xl[x_match]*5, "o")
#plt.annotate("matching point", xy=(x[x_match],a.xl[x_match]*5),xycoords='data', xytext=(x[x_match]+0.2,a.xl[x_match]*5-1),textcoords='data',size=12, arrowprops=dict(arrowstyle="->"))
#plt.xlabel("x")
#plt.ylabel(r"$\Psi$")
#plt.title("Second exicited state in L-J potential")
#plt.text(2.5, 8, "E=%.3f" %a.e)
#plt.legend()
########################################################################

####################Matching method tunnel############################

tux=np.linspace(-1.3 ,1.3, 2600)
tuv=np.r_[np.ones(300)*100000, np.zeros(1100), np.ones(200)*100, np.zeros(700),np.ones(300)*100000]
x_ma=900

tuv_scale=np.r_[np.ones(300), np.zeros(1100), np.ones(200)*0.2, np.zeros(700),np.ones(300)]
fig=plt.figure(figsize=(15,8))

fig.suptitle("Other states in tunnel potential")
for i, ei in enumerate((10, 30, 40, 60)):
    b=Schrodinger(dx=0.001, N=2600)
    b.matching_cal(tuv, x_ma, e=ei, de=0.3)
    ax = fig.add_subplot(220+i+1)
    ax.plot(tux[:b.xml+20], b.xl[:b.xml+20])
    ax.plot(tux[b.xmr-20:], b.xr[b.xmr-20:])
    ax.plot(tux,tuv_scale, '--')    
    ax.text(0, 1.2, "E=%.4f" %b.e)
    ax.set_xlabel("x")
    ax.set_ylabel("$\Psi$")
##########################################################################


#######################variational-Monte Carlo###########################
#vx=np.linspace(0.7, 5,43)
#vljv=40*((1.0/vx)**12-(1.0/vx)**6)
#fi=np.r_[np.zeros(3), np.ones(30), np.zeros(10)]
#c=Schrodinger()
#c.vari_mc(vljv, fi, 20000, 0.1)
#plt.plot(vx, c.fi0, '-o')
##for n in (1000, 10000, 20000):
##    c.vari_mc(vljv, fi, n, 0.1)
##    plt.plot(vx, c.fi0, '-o', label="%d M-C moves" %n)
#plt.title("L-J potential,Variational-MC method")
#plt.xlabel("x")
#plt.ylabel("$\Psi$")
#plt.text(2, 1, "E=%.3f" %c.E)
#plt.legend()

#x,y=np.ogrid[-2:2:21j,-2:2:21j]
#V=5*x**2+20*y**2
#fi=np.zeros((21, 21))
#fi[2:-2, 2:-2]=1
#
#fi1=np.exp(-(x**2+y**2)/2)/(2*pi)
#
#d=Schrodinger()
#d.vari_mc(V, fi, 40000, 0.2)
#r=d.fi0
#mlab.clf()
#mlab.surf(x, y, r*2)
#
#plt.plot(np.linspace(-2,2,21), r[10,:], '-o')
#plt.plot(np.linspace(-2,2,21), r[:,10], '-o')
#plt.title("Two dimensional harmonic oscillator")
#plt.xlabel("x or y")
#plt.ylabel("$\Psi$")
#plt.text(1, 1.1, "E=%.3f" %d.E)
#########################################################################