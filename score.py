import numpy as np
from scipy import interpolate
import pylab as pl

# 插值拟合点
miles = [0, 0.125, 0.25, 0.5, 0.75, 1, 1.25, 1.5] #英里
scores = [100, 99.8, 97.5, 75, 40, 12.5, 5, 0] #分数

def mile2km(mile):
    factor = 0.62137119
    return mile/factor

kms = [mile2km(mile) for mile in miles]
km_max = max(kms)
score_max = max(scores)

def get_func():
    func = interpolate.interp1d(kms, scores, kind="quadratic")
    return func

def plot(func):
    xnew = np.linspace(0, km_max, 101)
    ynew = func(xnew)
    pl.plot(xnew, ynew, label="quadratic")
    pl.legend(loc='upper right')
    pl.xlim((0, km_max + 0.2))
    pl.ylim((0, score_max + 5))
    pl.grid(axis='both')
    pl.show()