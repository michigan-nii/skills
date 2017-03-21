import numpy as np
import my

data = np.loadtxt('data.csv', delimiter=',', skiprows=1)
Y = data[:,1]
X = data[:,0]

my.regress(Y, X)
