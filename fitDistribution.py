
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import scipy
import pandas as pd
from parse_logs import parseLog, grabPath
from analyseLogs import extractInterTime, graphInterTime, extractArrivalTime, graphRunTime
import numpy as np
import scipy.stats as sts

folder = 'G:\My Drive\Thesis\Workload Logs'

files = grabPath(folder)
limit = 6000

RICC = parseLog([files[0]])
HP2CN = parseLog([files[1]])
META = parseLog([files[2]])
PIK = parseLog([files[3]])
allLogs = [RICC, HP2CN, META, PIK]

jobInterTime = extractArrivalTime(allLogs, 1)
#y_df = pd.DataFrame(jobInterTime[0], columns = ['Data'])
#print(y_df.describe())
pts = np.array(jobInterTime[0])
#pts = pts[pts <= limit]
num_bins = 24

count, bins, ignored = plt.hist(pts, num_bins, density=True,
                                edgecolor='k')
plt.title('RICC ', fontsize=20)
plt.xlabel(r'Daily Cycle')
plt.ylabel(r'%')


dist_names = ['gamma', 'beta', 'rayleigh', 'norm', 'pareto']

for dist_name in dist_names:
    print("Ok")
    dist = getattr(scipy.stats, dist_name)
    param = dist.fit(pts)
    print(param)
    rX = np.linspace(0,24,24)
    rP = dist.pdf(rX, *param)
    plt.plot(rX, rP, label=dist_name)




plt.show()

