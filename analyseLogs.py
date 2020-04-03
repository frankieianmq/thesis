"""
This python file will consists of an analysis of the logs
Variable List:
1 - Submit Time
3- Run time
7 - Req Num of Processors
6 - Used Mem / 9 - Req Mem
10 - Status (1: Complete, 0: Failed, 5: cancelled)

"""
from parse_logs import parseLog, grabPath, parseLogInfo
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
from datetime import datetime
import matplotlib.ticker as mtick


# Location can be either a folder location or
# a list of logs
folder = 'G:\My Drive\Thesis\Workload Logs'

files = grabPath(folder)
startTime = parseLogInfo(files)
d = datetime.utcfromtimestamp(int(startTime[0]))
print(startTime[0])
print(d.hour)
print(d.strftime("%A"))
# Checks if it is power of two
# Source https://stackoverflow.com/questions/600293/how-to-check-if-a-number-is-a-power-of-2/600306#600306
def is_power_of_two(n):
    if n == 1:
        return False
    return (n != 0) and (n & (n-1) == 0)


# Extracts inter-arrival time: How long it takes
# for next job to be submitted
def extractInterTime(log, variable):
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


# Extract the arrival time from the logs
# Adding the seconds to the unix start time
# So we know what time it is
def extractArrivalTime(log):
    arrivalTime = []

    for x in log:
        logIndex = 0
        store = []
        for y in x:
            for z in y:
                time = int(z[1]) + int(startTime[logIndex])
                store.append(time)
        logIndex += 1
        arrivalTime.append(store)
    return arrivalTime


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
# Graphs inter-arrival time
# Unable to graph it in a meaningful way,
# Will be doing Arrival rate as most papers utilise
# arrival rate.
def graphInterTime(submitTime):
    count = Counter(submitTime)
    print(count)
    plt.bar(count.keys(), count.values())
    plt.xlim((0, 3000))
    plt.ylim((0, 3000))
    plt.show()
    plt.hist(submitTime, bins=10)
    plt.show()


def graphArrivalRate(logs):
    return 0


# Todo - Graph runtime for all four workloads
def graphRunTime(runTime):
    count = Counter(runTime)
    print(count)
    plt.bar(count.keys(), count.values())
    plt.show()


# Graphs job size
def graphJobSize(jobSize):
    count = Counter(jobSize)

    # Analysis
    print(analyseJobSize(count, 32))
    print(count)
    print(count.values())
    print(count.keys())
    '''
    plt.bar(count.keys(), count.values())
    plt.show()
    '''
    sorted_mem = np.sort(jobSize)

    yvals = np.arange(len(sorted_mem)) / float(len(sorted_mem) - 1)

    plt.plot(sorted_mem, yvals)

    plt.ticklabel_format(style='plain')
    plt.show()


# Analyse job size: Understand
def analyseJobSize(countedJobSize, range):
    remainder = {}
    jobCount = 0
    inRange = 0
    powerOfTwo = 0
    even = 0
    odd = 0

    for key, value in countedJobSize.items():
        jobCount += value

        # Check % of job within range
        # Checks % of job that are power of 2
        if key <= range:
            inRange += value

        if is_power_of_two(key):
            powerOfTwo += value
        elif key != 1:
            remainder[key] = value

        # Check % of job even or odd

    remCount = 0
    remEven = 0
    remOdd = 0

    for key, value in remainder.items():
        remCount += value

        if key % 2 == 0:
            remEven += value
        else:
            remOdd += value

    print(remCount/jobCount, remEven/remCount, remOdd/remCount)
    print(remainder)
    print(jobCount)

    analyse = [inRange/jobCount, powerOfTwo/jobCount, even/jobCount, odd/jobCount]

    return analyse

# Todo - Graph Job Cancellations
def analyseJobCanc(canc):
    count = Counter(canc)

    jobCount = 0

    for x in count.values():
        jobCount += x


    print(count)
    analyse = round(count[5] / jobCount, 3)
    print(analyse)
    return analyse


# Analysing the memory of jobs
# Input is List of memory
# Output = displays graph with cdfs of each
# workload log
def analyseJobMem(mem):
    Counter = []
    for item in mem:
        store = []
        sorted_mem = np.sort(item)
        yvals = np.arange(len(sorted_mem)) / float(len(sorted_mem) - 1)
        store.append(sorted_mem)
        store.append(yvals)
        Counter.append(store)

    RICC = plt.plot(Counter[0][0], Counter[0][1], 'b-', label='RICC')
    HPC2N = plt.plot(Counter[1][0], Counter[1][1], 'r--', label='HPC2N')
    META = plt.plot(Counter[2][0], Counter[2][1], 'g--', label='META')
    PIK = plt.plot(Counter[3][0], Counter[3][1], 'g-', label='PIK')

    plt.ticklabel_format(style='plain')
    plt.xlabel("Memory Size")
    plt.ylabel("% of jobs")
    plt.legend(loc='upper right')
    plt.show()


# Todo - Complete full graph construction
def main():
    print(files)
    file = [files[1]]
    print(file)

    RICC = parseLog([files[0]])
    HP2CN = parseLog([files[1]])
    META = parseLog([files[2]])
    PIK = parseLog([files[3]])

    allLogs = [RICC,HP2CN,META,PIK]

    """
    logTime = parseLogInfo(folder)
    plt.xlim((0, 260))
    plt.ylim((0, 16000))
    
    
    # Job Size
    jobSize = extractInfo(logOne, 4)
    graphJobSize(jobSize)
    
    # Inter-arrival Time
    jobInterTime = []
    jobInterTime.append(extractInterTime(RICC, 1))
    jobInterTime.append(extractInterTime(HP2CN, 1))
    jobInterTime.append(extractInterTime(META, 1))
    jobInterTime.append(extractInterTime(PIK, 1))
    graphInterTime(jobInterTime)
    
    #Job Canc
    jobCanc = extractInfo(logOne, 10)
    analyseJobCanc(jobCanc)
    
   
    
    
       
    # Arrival Rate
    jobArrival = extractArrivalTime(allLogs)
    graphArrivalRate(jobArrival)
    """
     # Job Memory
    jobMem = []
    jobMem.append(extractInfo(RICC, 9))
    jobMem.append(extractInfo(HP2CN, 6))
    jobMem.append(extractInfo(META, 6))
    jobMem.append(extractInfo(PIK, 6))

    analyseJobMem(jobMem)




main()