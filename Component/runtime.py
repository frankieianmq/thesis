"""
This file aims to generate the runtime of the jobs. The
http://usmanwardag.github.io/python/astronomy/2016/07/10/inverse-transform-sampling-with-python.html
"""

from parse_logs import parseLog, grabPath, parseLogInfo, grabName
from collections import Counter
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import matplotlib.dates as md
import numpy as np
import numpy.random as ra
from datetime import datetime
from pytz import timezone
import matplotlib.ticker as mtick
import scipy.interpolate as interpolate

param = [-420.52, 1640.97]
size = 1
num_bins = 25

def genRunTime(min, max):
    # Checks min/max are negative
    # Returns 0 (error sign)
    if min <= 0 or max <= 0:
        return 0

    # Checks min/max are same
    if min == max:
        return 0

    #Obtain PDF and linespace for generation
    rX = np.linspace(min, max, max-min)
    rP = scipy.stats.gilbrat.pdf(rX, loc= param[0], scale = param[1])

    # Obtain Samples, rounding them up
    samples = np.random.choice(rX, size=size, p=rP / np.sum(rP))
    rounded = [int(round(x)) for x in samples]

    return rounded[0]

# Testing area
if __name__ == "__main__":
    '''
    min = 10
    max = 1000
    while max < 10001:
        print(genRunTime(min,max))
        min += 10
        max += 10
    '''
    print(genRunTime(-1,2))