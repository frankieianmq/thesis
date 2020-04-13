
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import scipy
import pandas as pd
from scipy.stats import norm
from parse_logs import parseLog, grabPath
from analyseLogs import extractInterTime, graphInterTime


folder = 'G:\My Drive\Thesis\Workload Logs'

files = grabPath(folder)

RICC = parseLog([files[0]])
HP2CN = parseLog([files[1]])
META = parseLog([files[2]])
PIK = parseLog([files[3]])
allLogs = [RICC, HP2CN, META, PIK]

jobInterTime = extractInterTime(allLogs, 1)
graphInterTime(jobInterTime)
#y_df = pd.DataFrame(jobInterTime[0], columns = ['Data'])
#print(y_df.describe())
y = jobInterTime[0]
n, bins, patches = plt.hist(y, bins=100)


# best fit of data
(mu, sigma) = scipy.optimize.curve_fit()

# add a 'best fit' line
t = norm.pdf(bins, mu, sigma)
l = plt.plot(bins,t, 'r--', linewidth=2)

#plot
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.grid(True)

plt.show()

plt.legend(loc='upper right')
plt.show()