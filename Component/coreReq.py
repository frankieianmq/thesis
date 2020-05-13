"""
This file aims to generate the job size of the jobs. The jobs generated
fall into three categories: serial, POT(power of two), and remainder(where not either serial or POT)

Distributions:
POT: Rice
Remainder: laplace
"""
import random
import scipy
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
import math

# Parameters
probability = [0.722, 0.955, 1]
potParam = [[0.437,0.227], 'rice']
remParam = [[31.24, 47.586], 'laplace']
size = 1


# This will generate the variable for POT
# POT = Power of two
def genPOT(minCore, maxCore):
    logmin = max(int(math.floor(math.log(minCore)/math.log(2))), 1)
    logmax = int(math.floor(math.log(maxCore)/math.log(2)))

    # Obtain PDF and linespace for generation
    rX = np.linspace(logmin, logmax, logmax - logmin)
    dist = getattr(scipy.stats, potParam[1])

    rP = dist.pdf(rX, *potParam[0])


    # Obtain Samples, rounding them up
    samples = np.random.choice(rX, size=size, p=rP / np.sum(rP))
    rounded = [int(round(x)) for x in samples]

    return int(math.pow(2, rounded[0]))


# Todo This will generate the variable for remainder jobs
# REM = remainder
# These jobs are neither serial jobs or power of two jobs.
# Output != 1 || log(x)/log(2) == int
def genREM(min, max):
    # Obtain PDF and linespace for generation
    rX = np.linspace(min, max, max - min)
    dist = getattr(scipy.stats, remParam[1])
    rP = dist.pdf(rX, *remParam[0])

    # Obtain Samples, rounding them up
    samples = np.random.choice(rX, size=size, p=rP / np.sum(rP))
    rounded = [int(round(x)) for x in samples]
    if rounded[0]  == 1:
        print()

    return rounded[0]


# Given probability, determine which route to go
def grabDecision(probability, min, max):
    randomNum = random.random()

    # Serial Job or POT job or Remainder Job
    if randomNum <= probability[0]:
        return 1
    elif randomNum <= probability[1]:
        return genPOT(min, max)
    else:
        return genREM(min, max)


# Generates job size
# Input - min, max
# min = minimum job size, max = maximum job size
def genJobSize(min, max):
    coreReq = grabDecision(probability, min, max)

    return coreReq


if __name__ == "__main__":
    '''
   for x in range(1000):
        print(genJobSize(1,8))
    '''
    print(genREM(1,8))