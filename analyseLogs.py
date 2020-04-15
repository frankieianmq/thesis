"""
This python file will consists of an analysis of the logs
Variable List:
1 - Submit Time
3- Run time
7 - Req Num of Processors
6 - Used Mem / 9 - Req Mem
10 - Status (1: Complete, 0: Failed, 5: cancelled)

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
from scipy.optimize import curve_fit


# Location can be either a folder location or
# a list of logs
folder = 'G:\My Drive\Thesis\Workload Logs'

files = grabPath(folder)
fileNames = grabName(folder)
graphTypes = ['b-', 'r--', 'g--', 'g-']

startTime = parseLogInfo(files, "UnixStartTime:")
timeZone = parseLogInfo(files, "TimeZoneString:")
#d = datetime.fromtimestamp(int(startTime[0]), tz=timezone(timeZone[0]))


# Checks if it is power of two
# Source https://stackoverflow.com/questions/600293/how-to-check-if-a-number-is-a-power-of-2/600306#600306
def is_power_of_two(n):
    if n == 1:
        return False
    return (n != 0) and (n & (n-1) == 0)


def switch_day(day):
    switcher = {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
        "Sunday": 7
    }
    return switcher.get(day)


# Extracts inter-arrival time: How long it takes
# for next job to be submitted
def extractInterTime(log, variable):
    extractedLog = []

    for x in log:
        logIndex = 0
        store = []
        for y in x:
            oldTime = 0
            oldCalc = 0
            for z in y:
                if len(z) != 0:
                    time = int(z[variable])
                    if oldTime == time:
                        store.append(oldCalc)
                    else:
                        store.append(time - oldTime)
                        oldCalc = time - oldTime
                        oldTime = time
        logIndex += 1
        extractedLog.append(store)

    return extractedLog


# Extract the arrival time from the logs
# Adding the seconds to the unix start time
# So we know what time it is
# Variable settings, extracts info
# 1 = hour, 2 = day
def extractArrivalTime(log, variable):
    arrivalTime = []

    for x in log:
        logIndex = 0
        store = []
        for y in x:
            for z in y:
                time = int(z[1]) + int(startTime[logIndex])
                spec = datetime.fromtimestamp(time, tz=timezone(timeZone[logIndex]))
                if variable == 1:
                    store.append(spec.hour)
                else:
                    store.append(switch_day(spec.strftime("%A")))
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
            if len(y) != 0:
                extractedLog.append(int(y[variable]))
    return extractedLog

def extractMultiLog(logs, variable):
    extractedLog = []

    for x in logs:
        logIndex = 0
        store = []
        for y in x:
            for z in y:
                if len(z) != 0:
                    store.append(int(z[variable]))
        logIndex += 1
        extractedLog.append(store)
    return extractedLog


# Todo - Unfinished function
# Graphs inter-arrival time
# Unable to graph it in a meaningful way,
# Will be doing Arrival rate as most papers utilise
# arrival rate.
def graphInterTime(interTimeList):
    Counter = []
    for item in interTimeList:
        store = []
        sorted_inter = np.sort(item)
        yvals = np.arange(len(sorted_inter)) / float(len(sorted_inter) - 1)
        store.append(sorted_inter)
        store.append(yvals)
        Counter.append(store)


    for index in range(len(Counter)):
        plt.plot(Counter[index][0], Counter[index][1], graphTypes[index], label=fileNames[index])


    plt.ticklabel_format(style='plain')
    plt.xlabel("Inter-arrival Time")
    plt.ylabel("% of jobs")
    plt.legend(loc='lower right')
    plt.xscale("log")
    plt.ylim(-0.05, 1)
    plt.show()


def graphArrivalRate(logs):
    CounterList = []
    for item in logs:
        CounterList.append(Counter(item))

    for x in range(len(CounterList)):
        plt.figure()
        plt.bar(CounterList[x].keys(), CounterList[x].values())

    plt.show()


# Todo - Graph runtime for all four workloads
def graphRunTime(runTime):
    Counter = []
    for item in runTime:
        store = []
        sorted_runTime = np.sort(item)
        yvals = np.arange(len(sorted_runTime)) / float(len(sorted_runTime) - 1)
        store.append(sorted_runTime)
        store.append(yvals)
        Counter.append(store)

    for index in range(len(Counter)):
        plt.plot(Counter[index][0], Counter[index][1], graphTypes[index], label=fileNames[index])

    plt.ticklabel_format(style='plain')
    plt.xlabel("Run time")
    plt.ylabel("% of jobs")
    plt.legend(loc='lower right')
    plt.xscale("log")
    plt.ylim(-0.05, 1)
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

    for index in range(len(Counter)):
        plt.plot(Counter[index][0], Counter[index][1], graphTypes[index], label=fileNames[index])

    plt.ticklabel_format(style='plain')
    plt.xlabel("Memory Size")
    plt.ylabel("% of jobs")
    plt.legend(loc='lower right')
    plt.xscale("log")
    plt.ylim(-0.05, 1)
    plt.show()


# Analyse total memory usage. Unlike function analyseJobMem,
# this function is used to calculate and analyse the total memory used for each job
# Each memory logged is only for per core
def analyseTotalMem(mem, core):
    totalMemList = []
    for i in range(len(mem)):
        store =[]
        for index in range(len(mem[i])):
            store.append(int(mem[i][index]) * int(core[i][index]))
        totalMemList.append(store)

    Counter = []
    for item in totalMemList:
        store = []
        sorted_mem = np.sort(item)
        yvals = np.arange(len(sorted_mem)) / float(len(sorted_mem) - 1)
        store.append(sorted_mem)
        store.append(yvals)
        Counter.append(store)

    for index in range(len(Counter)):
        plt.plot(Counter[index][0], Counter[index][1], graphTypes[index], label=fileNames[index])

    plt.ticklabel_format(style='plain')
    plt.xlabel("Memory Size")
    plt.ylabel("% of jobs")
    plt.legend(loc='lower right')
    plt.xscale("log")
    plt.ylim(-0.05, 1)

    plt.show()


# Todo - Complete full graph construction
def main():
    print(files)

    allLogs = [parseLog([x]) for x in files]
    """
    
    # Job Size
    jobSize = extractInfo(logOne, 4)
    graphJobSize(jobSize)
    
    
    
    #Job Canc
    jobCanc = extractInfo(logOne, 10)
    analyseJobCanc(jobCanc)
    
    # Job Memory
    jobMem = extractMultiLog(allLogs, 6)
    analyseJobMem(jobMem)

    
    # Total Job Mem
    jobSize = extractMultiLog(allLogs, 4)
    jobMem = extractMultiLog(allLogs, 6)
    analyseTotalMem(jobMem, jobSize)
    
    # Inter-arrival Time
    jobInterTime = extractInterTime(allLogs, 1)
    graphInterTime(jobInterTime)
    
    # Arrival Rate Daily
    jobArrival = extractArrivalTime(allLogs, 1)
    graphArrivalRate(jobArrival)

    # Arrival Rate Weekly
    jobArrival = extractArrivalTime(allLogs, 2)
    graphArrivalRate(jobArrival)
    
     # Runtime
    jobRunTime = extractMultiLog(allLogs, 3)
    graphRunTime(jobRunTime)
    """
    jobMem = [extractInfo(allLogs[0],6), extractInfo(allLogs[1],9), extractInfo(allLogs[2],6)]
    # Job Memory
    analyseJobMem(jobMem)



if __name__ == "__main__":
    main()