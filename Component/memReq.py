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
lowParam = [[20.12, 8.43, -368.97, 62175.72], 'johnsonsb']
medParam = [[0.66, 0.9, 2.47, -0.04, 144.42], 'genexpon']
highParam = [[1010.69, 1157.41], 'logistic']
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
    # Checks min/max are negative
    # Returns 0 (error sign)
    if min <= 0 or max <= 0:
        return 0

    # Checks min/max are same
    if min == max:
        return 0

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
    print(genMem(10,10,3))