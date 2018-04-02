import numpy as np
from scipy import stats
import peakutils

def GetDensity(origin):
    xmin = origin.min()
    xmax = origin.max()
    xs = np.arange(int(xmin*0.5),int(xmax*1.2),1)
    densityFunc= stats.gaussian_kde(origin)
    ys = densityFunc(xs)
    density = {"x":xs,"y":ys}
    return density

def IsOneMorePeak(density):
    return len(peakutils.indexes(density['y'])) > 1


