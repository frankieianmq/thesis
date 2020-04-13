import scipy
import numpy as np
import scipy.stats


n = 100
x = np.linspace(-4,4,n)
f = lambda x,mu,sigma: scipy.stats.norm(mu,sigma).cdf(x)

data = f(x,0.2,1) + 0.05*np.random.randn(n)
print(data)

mu,sigma = scipy.optimize.curve_fit(f,x,c)[0]
