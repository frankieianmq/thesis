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

    job = {}

    # Generate runtimes based on job type
    jType = GetJobType(jobTypes)
    job["type"] = jType

    # Grab the job type config attributes minRunTime and maxRuntime, processing them to give a runtime
    actRuntime = int(jobTypes[jType]["minRunTime"]) + random.randint(0, 5000) % (
        max(1, int(jobTypes[jType]["maxRunTime"])))
    job["actRunTime"] = actRuntime
    estError = random.randint(0, 5000) % actRuntime

    if random.randint(0, 5000) % 2 == 0:
        estRunTime = actRuntime - estError
    else:
        estRunTime = actRuntime + estError

    job["estRunTime"] = estRunTime