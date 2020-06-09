import scipy
import scipy.stats
import numpy as np
import numpy.random as ra
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
params = {'legend.fontsize': 13,
         'axes.labelsize': 13,
         'axes.titlesize': 13,
         'xtick.labelsize': 13,
         'ytick.labelsize': 13}
pylab.rcParams.update(params)


param = [-420.52, 1640.97]
size = 4000
num_bins = 1000

def main(min, max):
    rX = np.linspace(1, 50000, 50000)
    rP = scipy.stats.gilbrat.pdf(rX, loc=param[0], scale=param[1])
    plt.plot(rX,rP, label="Model")
    plt.legend(loc='upper right')

    samples = np.random.choice(rX, size=50000, p=rP / np.sum(rP))
    plt.hist(samples, num_bins, density=True)
    '''
    sample = np.random.rand(size)
    result = scipy.stats.gilbrat.ppf(sample, loc=param[0], scale=param[1])
    plt.hist(result, num_bins, density=True)
    '''
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.xlabel("Runtime (Seconds)")
    plt.ylabel("Density")
    plt.show()



def main1():
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
        storedata.append(child.attrib['memory'])

    storedata = [int(test) for test in storedata]

main(0,50000)