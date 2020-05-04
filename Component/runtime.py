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
from datetime import datetime
from pytz import timezone
import matplotlib.ticker as mtick

param = [-420.52, 1640.97]

def genRunTime():
    r = scipy.stats.gilbrat.rvs(loc= param[0], scale = param[1], size= 100)

    print(r)

    plt.show()

genRunTime()