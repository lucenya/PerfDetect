import pandas as pd
import numpy as np
from scipy import stats
from scipy.optimize import leastsq
import peakutils

import matplotlib.pyplot as plt

data = pd.read_csv('BobAccountInCampaignAggregatorServiceWeekday.csv',header = 0)
perf = data.duration_P75

def gaussFunc(par, t):
    return (par[0]/par[1])*np.exp(-np.power(t-par[2],2)/(2*np.power(par[1],2)))

def errFunc(par, t, y):
    err= y - gaussFunc(par,t)
    return err

def getDensity(origin):
    xmin = origin.min()
    xmax = origin.max()
    xs = np.linspace(xmin*0.5,xmax*1.2,1000)
    densityFunc= stats.gaussian_kde(origin)
    ys = densityFunc(xs)
    density = {"x":xs,"y":ys}
    return density

def getP0(density):
    xs = density['x']
    ys = density['y']
    indices= peakutils.indexes(-ys)
    indices= np.append(indices,0)
    indices= np.append(indices,999)
    peakIndex= np.argmax(ys)
    peakMax= xs[peakIndex]
    valleyDis= abs(indices-peakIndex)
    valleyNear= xs[indices[np.argmin(valleyDis)]]
    muEst = peakMax
    sEst = abs(peakMax-valleyNear)/2
    p0 = [1/np.sqrt(2*np.pi)/sEst, sEst, muEst]
    return p0


period = 120
endIndex = len(perf)
for i in range(period,endIndex):
    t0= i-period
    origin = perf[t0:i]
    density = getDensity(origin)
    p0 = getP0(density)
    pEst= leastsq(errFunc, p0, args = (density['x'], density['y']))
    yEst = gaussFunc(pEst[0],density['x'])
    mu= pEst[0][2]
    s= pEst[0][1]
    fig= plt.figure(figsize = (20, 7))
    plt.subplot(1,2,1)
    plt.plot(density['x'],density['y'])
    plt.plot(density['x'],yEst)
    plt.subplot(1,2,2)
    plt.plot(origin)
    plt.plot(origin[origin>mu+2*s],'ro')
    plt.show()