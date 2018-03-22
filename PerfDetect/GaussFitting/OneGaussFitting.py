from scipy.optimize import leastsq
import numpy as np
import peakutils

def gaussFunc(par, t):
    return par[0]*np.exp(-np.power(t-par[2],2)/(2*np.power(par[1],2)))

def errFunc(par, t, y):
    err= y - gaussFunc(par,t)
    return err

def getP0(density):
    xs = density['x']
    ys = density['y']
    indices= peakutils.indexes(-ys)
    valleies = xs[indices]
    valleies= np.append(valleies,min(xs))
    valleies= np.append(valleies,max(xs))
    muEst = xs[np.argmax(ys)]
    dis = abs(valleies-muEst)
    sEst = (min(dis)/2)
    p0 = [1/np.sqrt(2*np.pi)/sEst, sEst, muEst]
    return p0

def getThreshold(pEst):
    mu= pEst[2]
    s= abs(pEst[1])
    return mu+2*s

def Fitting(density):
    p0 = getP0(density)
    pEst= leastsq(errFunc, p0, args = (density['x'], density['y']))
    density['param0'] = p0
    density['y0Est'] = gaussFunc(p0,density['x'])
    density['param'] = pEst[0]
    density['yEst'] = gaussFunc(pEst[0],density['x'])
    density['threshold'] = getThreshold(pEst[0])
    return density


