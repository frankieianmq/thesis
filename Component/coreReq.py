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

def is_power_of_two(n):
    if n == 1:
        return False
    return (n != 0) and (n & (n-1) == 0)

# Parameters
probability = [0.722, 0.955, 1]
potParam = [[0.437,0.227], 'rice']
remParam = [[31.24, 47.586], 'laplace']
size = 1


# This will generate the variable for POT
# POT = Power of two
def genPOT(minCore, maxCore):
    logmin = max(int(math.floor(math.log(minCore)/math.log(2))),1)
    logmax = int(math.floor(math.log(maxCore)/math.log(2)))

    if logmin == logmax:
        logmin = 1

    # Obtain PDF and linespace for generation
    rX = np.linspace(logmin, logmax, logmax - logmin)
    dist = getattr(scipy.stats, potParam[1])

    rP = dist.pdf(rX, *potParam[0])


    # Obtain Samples, rounding them up
    samples = np.random.choice(rX, size=size, p=rP / np.sum(rP))
    rounded = [int(round(x)) for x in samples]

    return int(math.pow(2, rounded[0]))


# This will generate the variable for remainder jobs
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

    # Check if number is power of two
    # Use number not power of two
    num = rounded[0]
    while is_power_of_two(num):
        num -= 1

    # Check if serial job
    # If so, return nearest non POT (3)
    if num == 1:
        return 3

    # Return core size
    return num


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
    # Checks min/max are negative
    # Returns 0 (error sign)
    if min <= 0 or max <= 0:
        return 0

    # Checks min/max are same
    if min == max:
        return 0

    coreReq = grabDecision(probability, min, max)

    return coreReq


# Testing ground
if __name__ == "__main__":
    minCore = 1
    maxCore = 8
    while maxCore <= 100:
        print(genJobSize(minCore, maxCore))
        minCore += 10
        maxCore += 10


    print(genJobSize(1,8))
    print(genJobSize(-2, -8))
    print(genJobSize(10, 10))