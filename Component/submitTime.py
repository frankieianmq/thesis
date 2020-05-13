'''

This file are functions for memory generation. It will include all the limits and functions
required to genenerate memory for ds-sim.

Average	16.46, 4.79
'''

import scipy
import scipy.stats
import numpy as np
import numpy.random as ra
import matplotlib.pyplot as plt

time = 0
arrivalParam = [16.46, 4.79]
interParam = []


# This will generate the arrival rate for the jobs.
def genArrivalRate(min, max):
    # Obtain PDF and linespace for generation
    rX = np.linspace(min, max, max - min)
    rP = scipy.stats.gumbel_l.pdf(rX, loc=arrivalParam[0], scale=arrivalParam[1])
    print(rP)
    plt.plot(rX, rP)

    # Obtain Samples, rounding them up
    samples = np.random.choice(rX, size=1, p=rP / np.sum(rP))
    rounded = [int(round(x)) for x in samples]
    plt.show()
    return rounded


# This will generate the interarrival time
# i.e: The difference between previous job and job after
def genInterArrival():
    return


# This function will generate bag of tasks number
def genBOT():
    return


# This function will return the inter-arrival time for each job
def genSubmitTime():

    return()

if __name__ == "__main__":
    print(genArrivalRate(0,24))
