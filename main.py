import xml.etree.ElementTree as ET
import random
import sys

sys.path.insert(0, 'Component')

from Component import runtime as rt
from Component import submitTime as st
from Component import memReq as mr
from Component import coreReq as cr
import writeJobs as wj

config_file = "configs/config_testing_low.xml"
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


def CalcTotalCoreCount(child):
    root = ET.parse(config_file).getroot()
    total = 0

    for type_tag in root.iter(child):
        total += int(type_tag.get("coreCount"))

    return total


def main():
    # Obtain endtime and jobcount from config
    simEndTime = int(obtain_xml('termination/condition', 'value', 'type', 'endtime'))
    maxJobCount = int(obtain_xml('termination/condition', 'value', 'type', 'jobcount'))

    # Grab largest server type
    maxCapacity = largest_prop('servers/server', ['coreCount', 'memory', 'disk'])
    print(maxCapacity)
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
    category = mr.pickDist(totalCores)
    print(category)
    hour = 0
    botProbability = 0.2

    jobsList = []
    jID = 0
    arrivalRate = st.genArrivalRate(hour)
    oldJob = [0, 0]
    hourSeconds = 60*60
    secondsLeft = hourSeconds
    avg = int(hourSeconds/ arrivalRate)
    minTime = 1
    maxTime = hourSeconds
    hourTime = 0
    hourCount = 0
    allocated = False
    botMin = 1
    botMax = max(int(round(arrivalRate * botProbability)),2)
    botCount = 0

    print("Starting generation!")


    while jID < maxJobCount and submitTime < simEndTime:
        job = {}
        job['id'] = jID
        print("Generating Job: " + str(jID))

        # Check if submit time greater than
        if hourCount == arrivalRate:
            hour += 1

            # Check if hour is greater than 24
            if hour > 23:
                hour = 0

            # Set new arrival rate and its
            # components
            arrivalRate = st.genArrivalRate(hour)
            avg = int(hourSeconds / arrivalRate)
            botMin = 1
            botMax = min(int(round(arrivalRate * botProbability)),2)

            # Add remaining time as it is new hour
            submitTime += secondsLeft

            # Reset variables to original state
            hourCount = 0
            secondsLeft = hourSeconds
            minTime = 1
            maxTime = hourSeconds
            hourTime = 0
            oldJob = [0, 0]
            allocated = False

        # Check BOT is allocated
        if oldJob[1] > 0:
            botCount += 1

        # Check whether BOT jobs are all allocated
        if botCount == botMax:
            allocated = True

        # Generate a submit time that is not the same
        interArrival = st.genSubmitTime(minTime, maxTime, oldJob, category, botMin, botMax, allocated)
        oldJob = interArrival
        submitTime += interArrival[0]
        job["submitTime"] = submitTime

        hourCount += 1
        secondsLeft = secondsLeft - interArrival[0]
        hourTime += interArrival[0]

        calc = (hourCount * avg) - hourTime

        if calc <= 0:
            maxTime = avg
            minTime = 1
        else:
            minTime = calc
            maxTime = min(calc + avg, hourTime)

        if minTime >= maxTime:
            maxTime = minTime
            minTime = int(maxTime * 0.5)

        if interArrival[0] == 0:
            job = jobsList[jID - 1]
            job['id'] = jID

            # Grab the job type config attributes minRunTime and maxRuntime, processing them to give a runtime
            minRuntime = int(jobTypes[jType]["minRunTime"])
            maxRuntime = int(jobTypes[jType]["maxRunTime"])
            actRuntime = rt.genRunTime(minRuntime, maxRuntime)
            job["actRunTime"] = actRuntime

            # Estimate Runtime
            estError = random.randint(0, 5000) % actRuntime

            if random.randint(1, 5000) % 2 == 0:
                estRunTime = actRuntime - estError
            else:
                estRunTime = actRuntime + estError

            job["estRunTime"] = estRunTime
        else:
            # Check current load based on num of cores used
            coresInUse = CalcCoresInUse(submitTime, jobsList, jID)
            curLoad = coresInUse / totalCores * 100

            # Generate runtimes based on job type
            jType = GetJobType(jobTypes)
            job["type"] = jobTypes[jType]["type"]

            # Grab the job type config attributes minRunTime and maxRuntime, processing them to give a runtime
            minRuntime = int(jobTypes[jType]["minRunTime"])
            maxRuntime = int(jobTypes[jType]["maxRunTime"])
            actRuntime = rt.genRunTime(minRuntime, maxRuntime)
            job["actRunTime"] = actRuntime

            # Estimate Runtime
            estError = random.randint(0, 5000) % actRuntime

            if random.randint(1, 5000) % 2 == 0:
                estRunTime = actRuntime - estError
            else:
                estRunTime = actRuntime + estError

            job["estRunTime"] = estRunTime

            # Generate Job requirements
            resReq = {}

            # Generate core job requirements
            if curLoad < targetLoad:
                resReq["cores"] = cr.genJobSize(1, maxCapacity[0])
            else:
                resReq["cores"] = min(max(1, round(min(HOUR_IN_SECONDS, actRuntime) / (MIN_IN_SECONDS * 10))), maxCapacity[0])
                estError = random.randint(0, 5000) % (resReq["cores"] * 2)
                if random.randint(0, 5000) % 2 == 0:
                    resReq["cores"] = max(1, resReq["cores"] - estError)
                else:
                    resReq["cores"] = min(resReq["cores"] + estError, maxCapacity[0])

            # Generate Memory requirements
            resReq["mem"] = mr.genMem(MIN_MEM_PER_JOB_CORE, maxCapacity[1], category)

            # Generate disk requirements
            resReq["disk"] = (MIN_DISK_PER_JOB_CORE + random.randint(0, 5000) % ((1 + resReq["cores"] / 10)
                                                                                 * MIN_DISK_PER_JOB_CORE)) * resReq["cores"]
            resReq["disk"] -= resReq["disk"] % 100
            resReq["disk"] = min(resReq["disk"], maxCapacity[2])

            job["resReq"] = resReq

        jobsList.append(job)
        jID += 1
    return jobsList

# Testing area
if __name__ == "__main__":
    jobTypes = grab_jobTypes()
    wj.createXML(main(), jobTypes)
    print("Done generating!")


