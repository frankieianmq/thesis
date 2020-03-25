import xml.etree.ElementTree as ET
import random

config_file = "configs/config_simple0.xml"
avgLowTime = 3600 + random.randint(0,1000) % 43200
avgHighTime = 3600 + random.randint(0,1000) % 43200
MIN_IN_SECONDS = 60
HOUR_IN_SECONDS = 3600
FORWARD = 1
END_LOAD_STATE = 0
MIN_MEM_PER_JOB_CORE = 100
MIN_DISK_PER_JOB_CORE = 100




# Grabs xml child, where we grab attribute with property containing 'obtain' variable
def obtain_xml(child, attribute, prop, obtain):
    root = ET.parse(config_file).getroot()
    for type_tag in root.findall(child):
        type = type_tag.get(prop)
        if obtain == type:
            value = type_tag.get(attribute)
            return value


# Grabs xml child, where it grabs the largest attribute property
def largest_prop(child, prop):
    root = ET.parse(config_file).getroot()
    largest = []

    for type_tag in root.findall(child):
        property = []
        for x in prop:
            property.append(int(type_tag.get(x)))
        if property > largest:
            largest = property

    return largest


# Grabs the job types from config file (config_file)
def grab_jobTypes():
    jobTypes = []
    root = ET.parse(config_file).getroot()
    for type_tag in root.iter("job"):
        jobTypes.append(type_tag.attrib)
    return jobTypes

# Grabs the job type based on the a random integer
# E.g if "r" is 30, it will get the job type when the
# rates add to 30
def GetJobType(jobTypes):

    # Grab a random integer in the range of 1 - 100
    r = random.randint(0, 5000) % 100

    rMin, i, rMax = 0, 0, 0
    jType = None

    while i < len(jobTypes) and jType is None:
        rMin = rMax
        rMax += int(jobTypes[i]["populationRate"])
        if rMin <= r <= (rMax - 1):
            jType = i
        i += 1

    return jType


def GetNextLoadDuration(lState):
    lDuration = 0
    if lState == 0:
        lDuration = avgLowTime
    elif lState == 4:
        lDuration = avgHighTime
    else:
        if avgLowTime < avgHighTime:
            lDuration = avgLowTime
        else:
            lDuration = avgHighTime
    return lDuration


def CalcTotalCoreCount(child):
    root = ET.parse(config_file).getroot()
    total = 0

    for type_tag in root.iter(child):
        total += int(type_tag.get("coreCount"))

    return total


# Goes through the list, and calculate
def CalcCoresInUse(submitTime, jobList, jID):

    if len(jobList) == 0:
        return 0

    coresInUse = 0

    for x in range(jID):
        job = jobList[x]
        #print(job)
        completionTime = job["submitTime"] + job["actRunTime"]

        if completionTime > submitTime:
            coresInUse += job["resReq"]["cores"]

    return coresInUse


"""
def generateWorkload():
    return 0
def GetWorkloadInfo():
    return 0
"""



def main():
    # Obtain endtime and jobcount from config
    simEndTime = int(obtain_xml('termination/condition', 'value', 'type', 'endtime'))
    maxJobCount = int(obtain_xml('termination/condition', 'value', 'type', 'jobcount'))

    # Grab largest server type
    maxCapacity = largest_prop('servers/server', ['coreCount', 'memory', 'disk'])
    lTimeOffset = 5
    curLoad = 0

    jobTypes = grab_jobTypes()

    lDir = FORWARD
    submitInterval = MIN_IN_SECONDS
    submitTime = 0
    curLoadSTime = 0

    # Todo
    Load_Low = 0
    lState = Load_Low
    curLoadETime = 0
    targetLoad = avgLowTime #workloadInfo.avgLowTime
    loadOffset = 10
    totalCores = CalcTotalCoreCount("server");

    jobsList = []
    random.seed()

    jID = 0
    while jID < maxJobCount and submitTime < simEndTime:
        job = {}

        # Generate a submit time that is not the same
        submitTime += random.randint(0,5000) % submitInterval + 1

        print(submitInterval)

        if submitTime > curLoadETime and ((lDir > 0 and curLoad >= targetLoad) or (lDir < 0 and curLoad <= targetLoad)):

            curLoadSTime = curLoadETime
            if (lState + lDir) < Load_Low or (lState + lDir) >= END_LOAD_STATE:
                lDir = lDir * -1
            lState += lDir
            targetLoad = targetLoad + loadOffset * lDir
            curLoadETime = curLoadSTime + GetNextLoadDuration(lState)

        # Check current load based on num of cores used
        coresInUse = CalcCoresInUse(submitTime, jobsList, jID)
        curLoad = coresInUse / totalCores * 100

        # Checks if current load is smaller than target load (understand)
        if curLoad < targetLoad:
            submitInterval += (-lTimeOffset)
        else:
            submitInterval += lTimeOffset

        if submitInterval < lTimeOffset:
            submitInterval = lTimeOffset

        # submitInterval > limits[WorkloadTime_Limit].max
        if submitInterval > 43200:
            submitInterval = 43200

        job["submitTime"] = submitTime

        # Generate runtimes based on job type
        jType = GetJobType(jobTypes)
        job["type"] = jType

        # Grab the job type config attributes minRunTime and maxRuntime, processing them to give a runtime
        actRuntime = int(jobTypes[jType]["minRunTime"]) + random.randint(0, 5000) % (max(1, int(jobTypes[jType]["maxRunTime"])))
        job["actRunTime"] = actRuntime
        estError = random.randint(0,5000) % actRuntime

        if random.randint(0,5000) % 2 == 0:
            estRunTime = actRuntime - estError
        else:
            estRunTime = actRuntime + estError

        job["estRunTime"] = estRunTime

        # When load below min load, set cores to at least half of max cores
        # else, cores is relative to  the job type
        resReq = {}

        if curLoad < targetLoad:
            resReq["cores"] = random.randint(0,5000) % maxCapacity[0] + 1
        else:
            resReq["cores"] = min(max(1,round(min(HOUR_IN_SECONDS, actRuntime) / (MIN_IN_SECONDS * 10))), maxCapacity[0])
            estError = random.randint(0,5000) % (resReq["cores"] * 2)
            if random.randint(0,5000) % 2 == 0:
                resReq["cores"] = max(1, resReq["cores"] - estError)
            else:
                resReq["cores"] = min(resReq["cores"] + estError, maxCapacity[0])

        resReq["mem"] = (MIN_MEM_PER_JOB_CORE + random.randint(0,5000) % ((1 + resReq["cores"] / 10)
                                                                          * MIN_MEM_PER_JOB_CORE)) * resReq["cores"]
        resReq["mem"] -= resReq["mem"] % 100
        resReq["mem"] = min(resReq["mem"], maxCapacity[1])

        resReq["disk"] = (MIN_DISK_PER_JOB_CORE + random.randint(0,5000) % ((1+ resReq["cores"] / 10 )
                                                                            * MIN_DISK_PER_JOB_CORE)) * resReq["cores"]
        resReq["disk"] -= resReq["disk"] % 100
        resReq["disk"] = min(resReq["disk"], maxCapacity[2])

        job["resReq"] = resReq

        jobsList.append(job)
        jID += 1

main()

test =  grab_jobTypes()


t = GetJobType(test)

