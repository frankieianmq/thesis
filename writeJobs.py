'''
This file grabs the generated jobs, and writes into a XML file so DS-SIM can read it
'''

from lxml import etree

def createXML(jobs, jobTypes):
    # create XML
    root = etree.Element('jobs')

    for x in jobTypes:
        root.append(etree.Element('type', name=x['type'], minRunTime=x['minRunTime'], maxRunTime=x['maxRunTime'], populationRate=x['populationRate']))

    for x in jobs:
        root.append(etree.Element('job', id=str(x['id']), type=x['type'],
                                  submitTime=str(x['submitTime']), estRunTime=str(x['estRunTime']),
                                  cores=str(x['resReq']['cores']), memory=str(x['resReq']['mem'])
                                  ,disk=str(x['resReq']['disk'])))
    # pretty string
    s = etree.tostring(root, pretty_print=True)
    with open('xml/ds-jobs.xml', 'wb') as f:
        f.write(s)

def createXMLOriginal(jobs, jobTypes):
    # create XML
    root = etree.Element('jobs')

    for x in jobTypes:
        root.append(etree.Element('type', name=x['type'], minRunTime=x['minRunTime'], maxRunTime=x['maxRunTime'], populationRate=x['populationRate']))

    for x in jobs:
        root.append(etree.Element('job', id=str(x['id']), type=str(x['type']),
                                  submitTime=str(x['submitTime']), estRunTime=str(x['estRunTime']),
                                  cores=str(x['resReq']['cores']), memory=str(x['resReq']['mem'])
                                  , disk=str(x['resReq']['disk'])))
    # pretty string
    s = etree.tostring(root, pretty_print=True)
    with open('xml/ds-jobs.xml', 'wb') as f:
        f.write(s)