"""
This python file will consists of an analysis of the logs
Variable List:
1 - Submit Time
3- Run time
7 - Req Num of Processors
10 - Req Mem

"""
from parse_logs import parseLog, grabPath, parseLogInfo
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt

# Location can be either a folder location or
# a list of logs
folder = 'G:\My Drive\Session 1 2020\Workload Logs'

files = grabPath(folder)


# Checks if it is power of two
# Source https://stackoverflow.com/questions/600293/how-to-check-if-a-number-is-a-power-of-2/600306#600306
def is_power_of_two(n):
    return (n != 0 ) and (n & (n-1) == 0)


# Extracts submit time: How long it takes
# for next job to be submitted
def extractSubTime(log, variable):
    extractedLog = []

    for x in log:
        oldTime = 0
        oldCalc = 0
        for y in x:
            time = int(y[variable])
            if oldTime == time:
                extractedLog.append(oldCalc)
            else:
                extractedLog.append(time - oldTime)
                oldCalc = time - oldTime
                oldTime = time



    return extractedLog


# Extract Information about the specification
# Different to extractSubTime as
# it calculates the differences between previous submit
# time
def extractInfo(log, variable):
    extractedLog = []

    for x in log:
        for y in x:
            extractedLog.append(int(y[variable]))
    return extractedLog


# Todo - Unfinished function
# Graphs submit time
# Unable to graph it in a meaningful way,
# Will be doing Arrival rate as most papers utilise
# arrival rate.
def graphSubmitTime(submitTime):
    count = Counter(submitTime)
    print(count)
    plt.bar(count.keys(), count.values())
    plt.xlim((0, 3000))
    plt.ylim((0, 3000))
    plt.show()
    plt.hist(submitTime, bins=10)
    plt.show()


# Todo - Graph runtime for all four workloads
def graphRunTime(runTime):
    count = Counter(runTime)
    print(count)
    plt.bar(count.keys(), count.values())
    plt.show()


# Todo - Graph Job Requirements (e.g. processors, memory usage)
# Note - This may change to specific functions to graph each requirement
def graphJobReq():
    return 0

def graphJobSize(jobSize):
    count = Counter(jobSize)

    # Analysis
    print(analyseJobSize(count, 32))
    print(count)
    print(count.values())
    print(count.keys())
    plt.bar(count.keys(), count.values())
    plt.show()


#
def analyseJobSize(countedJobSize, range):
    jobCount = 0
    inRange = 0
    powerOfTwo = 0
    even = 0
    odd = 0

    for key, value in countedJobSize.items():
        jobCount += value

        # Check % of job within range
        if key <= range:
            inRange += value

        # Check % of job even or odd
        if key % 2 == 0:
            even += value
        else:
            odd += value

        # Checks % of job that are power of 2
        if is_power_of_two(key):
            powerOfTwo += value
    analyse = [inRange, powerOfTwo, even, odd]
    analyse = [round(x/jobCount, 3) for x in analyse]
    return analyse

# Todo - Graph Job Cancellations
def graphJobCanc():
    return 0


# Todo - Complete full graph construction
def main():

    file = [files[3]]
    print(file)
    logOne = parseLog(file)
    logTime = parseLogInfo(folder)
    plt.xlim((0, 260))
    plt.ylim((0, 16000))
    # submitTime = extractSubTime(logOne, 1)
    # runTime = extractInfo(logOne, 3)
    jobSize = extractInfo(logOne, 4)

    # graphRunTime(runTime)
    graphJobSize(jobSize)


main()