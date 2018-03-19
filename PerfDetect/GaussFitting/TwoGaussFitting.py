from scipy.optimize import least_squares
import numpy as np
import peakutils

lastTwoGaussP = []

def twoGaussFunc(par, t):
    return (par[0]/par[1])*np.exp(-np.power(t-par[2],2)/(2*np.power(par[1],2))) + \
            (par[3]/par[4])*np.exp(-np.power(t-par[5],2)/(2*np.power(par[4],2)))
    
def errTwoGaussFunc(par, t, y):
    err= y - twoGaussFunc(par,t)
    return err

def getMaxTwoPeakIndex(density):
    peakIndices = peakutils.indexes(density['y'])
    while (len(peakIndices) > 2):
        peaks = ys[peakIndices]
        peakIndices = np.delete(peakIndices,np.argmin(peaks))
    peakIndices.sort()
    return peakIndices

def isSameWithLastMu(muEst, lastTwoGaussP):
    if (len(lastTwoGaussP) < 6):
        return False
    lastMu = [lastTwoGaussP[2], lastTwoGaussP[5]]
    return pow(muEst[0]-lastMu[0],2)+pow(muEst[1]-lastMu[1],2)<100

def getSigma(density, twoPeakIndex):
    xs = density['x']
    ys = density['y']
    sEst = []
    valleyIndices= peakutils.indexes(-ys)
    valleyIndices= np.append(valleyIndices,0)
    valleyIndices= np.append(valleyIndices,int(len(xs)-1))
    valleies = xs[valleyIndices]
    muEst = xs[twoPeakIndex]
    isSecondPeakHigher = ys[twoPeakIndex[0]] < ys[twoPeakIndex[1]]
    if (isSecondPeakHigher):
        muEst = xs[[twoPeakIndex[1], twoPeakIndex[0]]]
    for mu in muEst:
        dis = abs(valleies-mu)
        sEst.append(min(dis)/2)
        valleies = np.delete(valleies, np.argmin(dis))
    if (isSecondPeakHigher):
        return [sEst[1], sEst[0]]
    else:
        return sEst

def getTwoGaussP0(density, lastTwoGaussP):
    xs = density['x']
    ys = density['y']
    twoPeakIndex = getMaxTwoPeakIndex(density)
    muEst = xs[twoPeakIndex]
    if (isSameWithLastMu(muEst, lastTwoGaussP)):
        return lastTwoGaussP
    else:
        sEst = getSigma(density,twoPeakIndex)
        p0 = [1/np.sqrt(2*np.pi)/sEst[0], sEst[0], muEst[0], \
                1/np.sqrt(2*np.pi)/sEst[1], sEst[1], muEst[1]]
        return p0

def getThreshold(pEst):
    mu = pEst[2]
    s = abs(pEst[1])
    if (pEst[2] < 0 or np.argmin([pEst[2],pEst[5]]) == 1):
        mu = pEst[5]
        s = abs(pEst[4])
    return mu+2*s

def Fitting(density, lastTwoGaussP):
    p0 = getTwoGaussP0(density, lastTwoGaussP)
    pEst= least_squares(errTwoGaussFunc, p0, args = (density['x'], density['y']))
    density['yEst'] = twoGaussFunc(pEst.x,density['x'])
    density['param'] = pEst.x
    density['threshold'] = getThreshold(pEst.x)
    return density


