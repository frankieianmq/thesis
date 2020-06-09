
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
from openpyxl import Workbook
import xml.etree.ElementTree as ET
import matplotlib.pylab as pylab
params = {'legend.fontsize': 14,
         'axes.labelsize': 14,
         'axes.titlesize': 14,
         'xtick.labelsize': 14,
         'ytick.labelsize': 14}
pylab.rcParams.update(params)


plt.gcf().subplots_adjust(bottom=0.15)


# Location can be either a folder location or
# a list of logs
folder = 'C:\\Users\\Frankie\\Google Drive\\Thesis\\Workload Logs - Analysis'

files = grabPath(folder)
fileNames = grabName(folder)
fileNames = ["Workload", "Generated"]
graphTypes = ['b-', 'r--', 'g--', 'g-','r-', ]

startTime = parseLogInfo(files, "UnixStartTime:")
timeZone = parseLogInfo(files, "TimeZoneString:")
endTime = parseLogInfo(files, "EndTime:")
print(endTime)
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
        store = []
        for y in x:
            oldTime = 0
            for z in y:
                if len(z) != 0:
                    time = int(z[variable])
                    if oldTime != time:
                        store.append(time - oldTime)
                        oldCalc = time - oldTime
                        oldTime = time
        extractedLog.append(store)
    return extractedLog


# Extracts the BOT (Bag of Tasks)
def extractBOT(log, variable):
    bot = []
    jobCount = []

    for x in log:
        storeSize = 0
        store = []
        for y in x:
            oldTime = 0
            botCount = 0
            for z in y:
                if len(z) != 0:
                    time = int(z[variable])
                    storeSize += 1

                    if oldTime == time:
                        botCount += 1
                    else:
                        if botCount > 0:
                            store.append(botCount)
                            botCount = 0
                        oldTime = time
        bot.append(store)
        jobCount.append(storeSize)
    return bot


def whatMonths(log):
    arrivalTime = []

    for x in log:
        logIndex = 0
        store = {}
        for y in x:
            for z in y:
                time = int(z[1]) + int(startTime[logIndex])
                spec = datetime.fromtimestamp(time, tz=timezone(timeZone[logIndex]))
                if store.get(spec.month) == None:
                    store[spec.month] = 0
        logIndex += 1
        arrivalTime.append(store)
    return arrivalTime


def extractMonths(log, variable):
    arrivalTime = []

    for x in log:
        logIndex = 0
        store = {}
        for y in x:
            for z in y:
                time = int(z[1]) + int(startTime[logIndex])
                spec = datetime.fromtimestamp(time, tz=timezone(timeZone[logIndex]))                    
                if store.get(spec.month) == None:
                    store[spec.month] = [z[variable]]
                else:
                    list = store.get(spec.month)
                    list.append(z[variable])
                    store.update({spec.month: list})
        logIndex += 1
        arrivalTime.append(store)
    return arrivalTime


def extractMonth(log, variable, month):
    extracted = []

    for x in log:
        logIndex = 0
        store = []
        for y in x:
            for z in y:
                time = int(z[1]) + int(startTime[logIndex][0])
                spec = datetime.fromtimestamp(time, tz=timezone(timeZone[logIndex][0]))
                if spec.month == month:
                    store.append(z[variable])
        logIndex += 1
        extracted.append(store)
    return extracted

def extractDay(log,variable, month):
    extracted = []
    logIndex = 0
    for x in log:
        store = []
        for y in x:
            for z in y:
                time = int(z[1]) + int(startTime[logIndex][0])
                spec = datetime.fromtimestamp(time, tz=timezone(timeZone[logIndex][0]))
                if spec.month == month and spec.day == 20:
                    store.append(z[variable])
        logIndex += 1
        extracted.append(store)
    return extracted

# Extract the arrival time from the logs
# Adding the seconds to the unix start time
# So we know what time it is
# Variable settings, extracts info
# 1 = hour, 2 = day
def extractArrivalTime(log, variable):
    arrivalTime = []
    logIndex = 0

    for x in log:
        store = []
        for y in x:
            for z in y:
                time = int(z[1]) + int(startTime[logIndex][0])
                spec = datetime.fromtimestamp(time, tz=timezone(timeZone[logIndex][0]))
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
    calcList = []
    for item in interTimeList:
        store = []
        count = Counter(item)
        print(count.most_common(10))
        sorted_inter = np.sort(item)
        print(len(sorted_inter))
        yvals = np.arange(len(sorted_inter)) / float(len(sorted_inter) - 1)
        store.append(sorted_inter)
        store.append(yvals)
        calcList.append(store)


    for index in range(len(calcList)):
        plt.plot(calcList[index][0], calcList[index][1], graphTypes[index], label=fileNames[index])


    plt.ticklabel_format(style='plain')
    plt.xlabel("Inter-arrival Time (Seconds)")
    plt.ylabel("Number of Jobs (%)")
    plt.legend(loc='lower right')
    plt.xscale("log")
    plt.xlim(1,100000)
    plt.ylim(0, 1)
    plt.show()


def graphArrivalRate(logs):
    CounterList = []
    for item in logs:
        length = len(item)
        count = Counter(item)
        print(count)
        store = [(x/length * 100) for x in count.values()]
        CounterList.append([count.keys(), store])


    for x in range(len(CounterList)):
        plt.figure()
        plt.bar(CounterList[x][0], CounterList[x][1])
        plt.xlabel("Time (hour)")
        plt.ylabel("Number of Jobs")

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

    #plt.ticklabel_format(style='plain')
    plt.xlabel("Run time (Seconds)")
    plt.ylabel("Number of Jobs (%)")
    plt.legend(loc='lower right')
    plt.xscale("log")
    plt.ylim(-0.05, 1)
    plt.show()


# Graphs job size
def graphJobSize(jobSize):
    Counter = []
    for item in jobSize:
        store = []
        sorted_runTime = np.sort(item)
        yvals = np.arange(len(sorted_runTime)) / float(len(sorted_runTime) - 1)
        store.append(sorted_runTime)
        store.append(yvals)
        Counter.append(store)

    for index in range(len(Counter)):
        plt.plot(Counter[index][0], Counter[index][1], graphTypes[index], label=fileNames[index])

    # plt.ticklabel_format(style='plain')
    plt.xlabel("Job Size (Cores)")
    plt.ylabel("Number of Jobs (%)")
    plt.legend(loc='lower right')
    plt.xscale("log")
    plt.ylim(-0.05, 1)
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
    '''
    print(remCount/jobCount, remEven/remCount, remOdd/remCount)
    print(remainder)
    print(jobCount)
    '''
    analyse = [inRange/jobCount, powerOfTwo/jobCount, even/jobCount, odd/jobCount]

    return analyse

# Todo - Graph Job Cancellations
def analyseJobCanc(canc):
    count = []
    for list in canc:
        count.append(Counter(list))


    jobCount = []

    for x in count:
        jobCount.append(sum(x.values()))


    analyse = []
    for x in range(len(count)):
        analyse.append(round(count[x][5] / jobCount[x], 3)*100)
    return analyse


# Analysing the memory of jobs
# Input is List of memory
# Output = displays graph with cdfs of each
# workload log
def analyseJobMem(mem):
    listMem = []
    for item in mem:
        store = []
        sorted_mem = np.sort(item)
        print(Counter(item).most_common(10))
        yvals = np.arange(len(sorted_mem)) / float(len(sorted_mem) - 1)
        store.append(sorted_mem)
        store.append(yvals)
        listMem.append(store)


    for index in range(len(listMem)):
        plt.plot(listMem[index][0], listMem[index][1], graphTypes[index], label=fileNames[index])

    plt.ticklabel_format(style='plain')
    plt.xlabel("Memory Size (MB)")
    plt.ylabel("Number of Jobs (%)")
    plt.legend(loc='lower right')
    plt.xscale("log")
    plt.ylim(-0.05, 1)
    plt.show()


def writeToExcel(log, type, workload):
    filename = type + workload + '.xlsx'
    workbook = Workbook()
    sheet = workbook.active
    for index in range(len(log)):
        sheet['A' + str(index+1)] = log[index]
    workbook.save(filename = filename)
    

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
    plt.xlabel("Memory Size (MB)")
    plt.ylabel("Number of jobs (%)")
    plt.legend(loc='upper left')
    plt.xscale("log")
    plt.ylim(-0.05, 1)

    plt.show()

def extractJobXML(xml):
    for x in xml:
        print(x['memory'])


# Todo - Complete full graph construction
def main():
    print(files)
    allLogs = [parseLog([x]) for x in files]
    #allLogs = [allLogs[0], allLogs[3]]

    '''
        # Job Size
        jobSize = extractInfo(logOne, 4)
        # graphJobSize(jobSize)

        #Job Canc
        jobCanc = extractInfo(logOne, 10)
        analyseJobCanc(jobCanc)

        # Job Memory
        jobMem = extractMultiLog(allLogs, 6)
        analyseJobMem(jobMem)
         jobMem = [extractInfo(allLogs[0], 6)]
        jobMem.append(extractInfo(allLogs[1], 6))
        jobMem.append(extractInfo(allLogs[2], 6))
        jobMem.append(extractInfo(allLogs[3], 9))

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

         # Runtime 3 or 8
        jobRunTime = extractMultiLog(allLogs, 3)
        graphRunTime(jobRunTime)

        plt.show()
       
    '''
    '''
    oldFile = "C:\\Users\\Frankie\\PycharmProjects\\Thesis\\configs\\ds-jobs.xml"
    genFile = "C:\\Users\\Frankie\\PycharmProjects\\Thesis\\ds-jobs.xml"

    def testing(log):
        extractedLog = []
        oldTime = 0

        for x in log:
            time = x
            if oldTime != time:
                extractedLog.append(time - oldTime)
                oldTime = time
        return extractedLog

    tree = ET.parse(oldFile).getroot()
    storedata = []
    for child in tree.findall('./job'):
        storedata.append(child.attrib['memory'])

    storedata = [int(test) for test in storedata]
    storedata = testing(storedata)

    tree = ET.parse(genFile).getroot()
    genFiledata = []
    for child in tree.findall('./job'):
        genFiledata.append(child.attrib['submitTime'])
    genFiledata = [int(test) for test in genFiledata]
    genFiledata = testing(genFiledata)

    jobMem = extractInterTime([allLogs[0]], 1)
    jobMem.append(storedata)
    jobMem.append(genFiledata)

    storedata = testing(storedata)
    # Job Memory
    jobMem = extractInterTime([allLogs[2]],1)
    jobMem.append(storedata)
    '''
    oldFile = "C:\\Users\\Frankie\\PycharmProjects\\Thesis\\xml\\ds-jobs-low.xml"

    def testing(log):
        extractedLog = []
        oldTime = 0

        for x in log:
            time = x
            if oldTime != time:
                extractedLog.append(time - oldTime)
                oldTime = time
        return extractedLog

    tree = ET.parse(oldFile).getroot()
    storedata = []
    for child in tree.findall('./job'):
        storedata.append(child.attrib['estRunTime'])

    storedata = [int(test) for test in storedata]
   # storedata = testing(storedata)

    jobMem = extractMultiLog([allLogs[0]], 3)
    jobMem.append(storedata)
    graphRunTime(jobMem)









if __name__ == "__main__":
    main()