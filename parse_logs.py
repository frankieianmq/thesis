"""
This python file will parse the log(s) of workloads and extract the data
"""
import os

# Function will parse logs
# Returns log as a list
# input files must be a list
def parseLog(files):
    logList = []

    if type(files) == str:
        files = grabPath(files)

    for file in files:
        filepath = file
        log = []
        with open(filepath) as fp:
            line = fp.readline()
            while line and len(line) != 0:
                if line[0] != ';':
                    log.append(line.split())
                line = fp.readline()
        logList.append(log)
    return logList


# Input = folder location
# Returns a list of items in folder
def grabPath(path):
    pth = path
    list = []
    for (dirpath, dirnames, filenames) in os.walk(pth):
        list = [(os.path.join(dirpath, y)) for y in filenames]
    return list

def parseLogInfo(files, variable):
    logList = []

    if type(files) == str:
        files = grabPath(files)

    for file in files:
        log = []
        with open(file) as fp:
            line = fp.readline()
            count = 0
            while count == 0:
                if line[0] == ';':
                    splitLine = line.split()
                    if len(splitLine) > 1 and splitLine[1] == variable:
                        logList.append(splitLine[2])
                else:
                    count = 1
                line = fp.readline()
    return logList

def grabName(path):
    pth = path
    list = []
    for (dirpath, dirnames, filenames) in os.walk(pth):
        list = [(y.split('-')[0]) for y in filenames]
    return list