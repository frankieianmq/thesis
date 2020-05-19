'''

This file are functions for memory generation. It will include all the limits and functions
required to genenerate memory for ds-sim.

Average	16.46, 4.79
'''

import scipy
import scipy.stats
import numpy as np
import numpy.random as ra
import matplotlib.pyplot as plt

# Parameters
probability = [0.2]
arrivalParam = [[16.46, 4.79], 'gumbel_l']
botParam = [[2185.18, -699.36, 91.61], 'loggamma']
genParam = [[-1017.67, 1492.75], 'kstwobign']
avgDay = 1000

# Parameters for low, medium and high CPU categories
lowParam = [[24.1, -3.61, 26.23], 'invgauss']
medParam = [[10.92, -9.73, 67.24], 'invgauss']
highParam = [[-573.52, 843.41], 'kstwobign']

# Switch dictionary to determine which distribution
# to use
switch = {
    0: lowParam,
    1: medParam,
    2: highParam,
    3: genParam
}


# This will generate the arrival rate for the jobs.
def genArrivalRate(hour):
    # Obtain PDF and linespace for generation
    rX = np.linspace(0, 24, 24)
    dist = getattr(scipy.stats, arrivalParam[1])

    rP = dist.pdf(rX, *arrivalParam[0])

    calc = round(rP[hour] * avgDay)

    return int(calc)


# This will generate the inter-arrival time
# i.e: The difference between previous job and job after
def genInterArrival(min, max, pick):
    # Pick distribution and get distribution
    param = switch[pick]
    dist = getattr(scipy.stats, param[1])

    # Obtain PDF and linespace for generation
    rX = np.linspace(min, max, max - min)
    rP = dist.pdf(rX, *param[0])

    # Obtain Samples, rounding them up
    samples = np.random.choice(rX, size=1, p=rP / np.sum(rP))
    rounded = [int(round(x)) for x in samples]

    return rounded[0]


# This function will generate bag of tasks number
def genBOT(min, max):



    # Obtain PDF and linespace for generation
    rX = np.linspace(min, max, max - min)

    dist = getattr(scipy.stats, botParam[1])

    rP = dist.pdf(rX, *botParam[0])

    # Obtain Samples, rounding them up
    samples = np.random.choice(rX, size=1, p=rP / np.sum(rP))
    rounded = [int(round(x)) for x in samples]

    return rounded[0]

# Given probability, determine which route to go
def grabDecision(probability):
    randomNum = ra.random()

    # Determine whether job is BOT or not
    if randomNum <= probability[0]:
        return True
    else:
        return False


# This function will return the inter-arrival time for each job
# min - minimum submit time, max - maximum  submit time
# job - previous job
def genSubmitTime(min, max, job, pick, botmin, botmax, allocated):
    # If previous job BOT, use same submit time
    if job[1] > 0:
        return [0, job[1]-1]

    # Checks min/max are negative
    # Returns 0 (error sign)
    if min <= 0 or max <= 0:
        return 0

    # Checks min/max are same
    if min == max:
        return 0

    interArrival = genInterArrival(min,max, pick)

    decision = False

    if not allocated:
        decision = grabDecision(probability)
    bot = 0

    # Decide if job BOT or not
    if decision:
       bot = genBOT(botmin, botmax)

    return [interArrival, bot]
''''''
# Testing area
if __name__ == "__main__":
    # Update this every hour
    arrivalRate = genArrivalRate(11)
    avg = int(60 * 60 / arrivalRate)
    botmin = 1
    botmax = max(int(round(arrivalRate * probability[0])), 2)
    hourBot = int(round(arrivalRate * probability[0]))
    allocated = False

    # Variables
    oldjob = [0, 0]
    count = 0
    botCount = 0
    submitTime = 0
    hour1 = 60 * 60
    hour = 60 * 60
    pick = 0
    aRate = arrivalRate

    minSubmit = 1
    maxSubmit = 100
    while maxSubmit <= 10000:
        print(genSubmitTime(minSubmit, maxSubmit, oldjob, pick, botmin, botmax, allocated))
        minSubmit += 10
        maxSubmit += 10

    print(genSubmitTime(-10, -8, oldjob, pick, botmin, botmax, allocated))
    print(genSubmitTime(10, 10, oldjob, pick, botmin, botmax, allocated))

    '''
    # Update this every hour
    arrivalRate = genArrivalRate(11)
    avg = int(60 * 60 / arrivalRate)
    botmin = 1
    botmax = max(int(round(arrivalRate * probability[0])),2)
    hourBot = int(round(arrivalRate * probability[0]))
    allocated = False

    # Variables
    oldjob = [0, 0]
    count = 0
    botCount = 0
    submitTime = 0
    hour1 = 60 * 60
    hour = 60 * 60
    minTime = 1
    maxTime = hour
    pick = 0
    aRate = arrivalRate

    while count <= arrivalRate-1:
        if oldjob[1] > 0:
            botCount += 1
            #avg = int((hour /(aRate-botCount)))
        if botCount == hourBot:
            allocated = True

        job = genSubmitTime(minTime, maxTime, oldjob, pick, botmin, botmax, allocated)
        oldjob = job
        submitTime += job[0]

        count += 1
        hour1 = hour1 - job[0]

        calc = (count * avg) - submitTime

        if calc < 0:
            maxTime = avg
            minTime = 1
        else:
            minTime = calc
            maxTime = min(calc + avg, hour1)

        if minTime >= maxTime:
            maxTime = minTime
            minTime = int(maxTime * 0.5)
       # print(job[0], hour1, job[1], minTime, maxTime, calc, avg)
        '''