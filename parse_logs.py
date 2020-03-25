"""
This python file will parse the log(s) of workloads and extract the data
"""

# Function will parse logs
# Returns log as a list
# input files must be a list
def parseLog(files):
    logList = []

    for file in files:
        filepath = file
        with open(filepath) as fp:
            line = fp.readline()
            while line and len(line) != 0:
                if line[0] != ';':
                    logList.append(line.split())
                line = fp.readline()

    return logList
