# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 16:50:05 2020

@author: Salehin
"""
import math
import random
from scipy import interpolate
import seaborn as sns
import numpy as np
import numpy as np
import time
start_time=time.time()
data=[65,32,12,20,60,14,16,21,20,18,40,24,22,25,25]

theta=sum(data)/len(data)
B1=500
B2=500
n=len(data)
nominal1,nominal2,nominal3=85,92,99
def quadratic(x,x0,y0,x1,y1,x2,y2):
    return (y0*((x-x1)*(x-x2))/((x0-x1)*(x0-x2)))+(y1*((x-x0)*(x-x2))/((x1-x0)*(x1-x2)))+(y2*((x-x0)*(x-x1))/((x2-x0)*(x2-x1)))
    
    
def bootstrap(l):
    l1=[]
    for i in range(len(l)):
        a=random.randrange(1,15)
        l1.append(l[a-1])
    return l1
def parameter(l):
    return sum(l)/len(l)
ci=[]
def percentile(interval,l):
    l1=round(((1-(interval/100))/2),4)
    h1=round(l1+(interval/100),4)
    lower1=math.ceil(len(l)*l1)
    higher1=math.ceil(len(l)*h1)
    return (l[lower1-1],l[higher1-1])

cover1,cover2,cover3=0,0,0
for i in range(B1):
    b=bootstrap(data)
    thetas=[]
    for j in range(B2):
        c=bootstrap(b)
        param=parameter(c)
        thetas.append(param)
    thetas.sort()
    lfirst=percentile(nominal1,thetas)
    lsecond=percentile(nominal2,thetas)
    lthird=percentile(nominal3,thetas)        
    if(theta<=lfirst[1]  and theta>=lfirst[0]):
        cover1+=1
    if(theta<=lsecond[1]  and theta>=lsecond[0]):
        cover2+=1
    if(theta<=lthird[1] and theta>=lthird[0]):
        cover3+=1  
covprob1=cover1*100/B1 
covprob2=cover2*100/B1
covprob3=cover3*100/B1
f=interpolate.interp1d([covprob1,covprob2,covprob3],[nominal1,nominal2,nominal3],'quadratic')
y=f(90)
ci.append(y)
print(time.time()-start_time)    
y=quadratic(90,covprob1,nominal1,covprob2,nominal2,covprob3,nominal3)
sns.kdeplot(thetas)
data.sort()
print(percentile(95,data))
gg=np.zeros((200,2))
for j in range(200):
    percentiles=[]
    for i in range(500):
        a=bootstrap(data)
        p=parameter(a)
        percentiles.append(p)
    percentiles.sort()
    g=percentile(90,percentiles)
    gg[j,0]=g[0]
    gg[j,1]=g[1]
sns.distplot(percentiles)   
print(time.time()-start_time)    



        
    