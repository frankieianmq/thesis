'''
This file are functions for memory generation. It will include all the limits and functions
required to genenerate memory for ds-sim.

resReq["mem"] = (MIN_MEM_PER_JOB_CORE + random.randint(0,5000) % ((1 + resReq["cores"] / 10)
                                                                          * MIN_MEM_PER_JOB_CORE)) * resReq["cores"]
resReq["mem"] -= resReq["mem"] % 100
resReq["mem"] = min(resReq["mem"], maxCapacity[1])

CPU Count Category:
•	Low: 1-700
•	Medium: 701 - 2000
•	High:2001 – 3100

'''
import scipy
import scipy.stats
import numpy as np
import numpy.random as ra

#Parameters
genParam = []
lowParam =[[24.09, -3.60], 'invgauss']
medParam = [[10.91, -9.73], 'invgauss']
highParam = [[-573.52, 843.41], 'kstwobign']
cpuParam = [1, 701, 2001, 3100]
size = 1

# Switch dictionary to determine which
switch = {
    0: lowParam,
    1: medParam,
    2: highParam,
    3: genParam
}

# Input - Specs of server
# Determines which distribution to pick
def pickDist(specs):
    if cpuParam[0] <= specs < cpuParam[1]:
        return 0
    elif cpuParam[1] <= specs < cpuParam[2]:
        return 1
    elif cpuParam[2] <= specs < cpuParam[3]:
        return 2
    else:
        return 3



def genMem(min, max, pick):
    #Pick distribution and get distribution
    param = switch[pick]
    dist = getattr(scipy.stats, param[1])

    # Obtain PDF and linespace for generation
    rX = np.linspace(min, max, max - min)
    rP = dist.pdf(rX, *param[0])


    # Obtain Samples, rounding them up
    samples = np.random.choice(rX, size=size, p=rP / np.sum(rP))
    rounded = [int(round(x)) for x in samples]

    return rounded[0]

# Testing area
if __name__ == "__main__":
    print(genMem(1801,100000,1))