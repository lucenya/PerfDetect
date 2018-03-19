from scipy.optimize import least_squares
import numpy as np
import peakutils

def gaussFunc(par, t):
    return (par[0]/par[1])*np.exp(-np.power(t-par[2],2)/(2*np.power(par[1],2)))

def errFunc(par, t, y):
    err= y - gaussFunc(par,t)
    return err

def getP0(density):
    xs = density['x']
    ys = density['y']
    indices= peakutils.indexes(-ys)
    indices= np.append(indices,0)
    indices= np.append(indices,int(len(xs)-1))
    muEst = max(ys)
    valleies = xs[indices]
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
    pEst= least_squares(errFunc, p0, args = (density['x'], density['y']))
    density['yEst'] = gaussFunc(pEst.x,density['x'])
    density['param'] = pEst.x
    density['threshold'] = getThreshold(pEst.x)
    return density


