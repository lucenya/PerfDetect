from scipy.optimize import leastsq
import numpy as np
import peakutils
import pandas as pd

lastTwoGaussPFile = "./lastTwoGaussP.csv"

def twoGaussFunc(par, t):
    return (par[0]/2)*np.exp(-np.power(t-par[2],2)/(2*np.power(par[1],2))) + \
            (par[3]/2)*np.exp(-np.power(t-par[5],2)/(2*np.power(par[4],2)))
    
def errTwoGaussFunc(par, t, y):
    err= y - twoGaussFunc(par,t)
    return err

def getFirstTwoPeakIndex(density):
    peakIndices = peakutils.indexes(density['y'])
    peakIndices.sort()
    return peakIndices[:2]

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
    if (len(valleyIndices)==0):
        valleyIndices = np.append(valleyIndices, int(np.average(twoPeakIndex)))
    valleies = xs[valleyIndices]
    valleies= np.append(valleies,min(xs))
    valleies= np.append(valleies,max(xs))
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
    twoPeakIndex = getFirstTwoPeakIndex(density)
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

def getLastTwoGaussP(perfKey):
    lastTwoGaussP = pd.read_csv(lastTwoGaussPFile, header=0)
    lastTwoGaussPDic = lastTwoGaussP.to_dict('list')
    return lastTwoGaussPDic

def setLastTwoGaussP(lastTwoGaussPDic, perfKey, pValue):
    lastTwoGaussPDic[perfKey] = pValue
    df = pd.DataFrame.from_dict(lastTwoGaussPDic)
    df.to_csv(lastTwoGaussPFile, index=False)

def Fitting(density, perfKey):
    lastTwoGaussP = getLastTwoGaussP(perfKey)
    lastPerfKeyP = lastTwoGaussP[perfKey] if perfKey in lastTwoGaussP else []
    p0 = getTwoGaussP0(density, lastPerfKeyP)
    pEst= leastsq(errTwoGaussFunc, p0, args = (density['x'], density['y']))
    density['param0'] = p0
    density['y0Est'] = twoGaussFunc(p0,density['x'])
    density['param'] = pEst[0]
    density['yEst'] = twoGaussFunc(pEst[0],density['x'])
    density['threshold'] = getThreshold(pEst[0])
    setLastTwoGaussP(lastTwoGaussP, perfKey, density['param'].tolist())
    return density


