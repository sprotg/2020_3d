import random
from math import sqrt, e, pi
import matplotlib.pyplot as plt

def normal(x, s, mu):
    return (1/sqrt(2*pi*s**2) * e**(-1*((x-mu)**2)/(2*s**2)))

def get_average(X):
    s = 0
    for e in X:
        s += e
    return s/len(X)

def get_variance(X, mu):
    s = 0
    for e in X:
        s += (e - mu)**2
    v = s / (len(X)-1)
    return v


max = 10
min = 0
step = (max - min)/100

X = [5 + random.random() * 2 for i in range(1000)]
X_graf = [min + x*step for x in range(100)]

#Middelværdi
mu = get_average(X)
#Varians
s = get_variance(X, mu)

print(mu, s)

X_graf = [min + x*step for x in range(100)]
Y = [normal(X_graf[i] , s, mu) for i in range(100)]

#Tegning af histogrammet
plt.hist(X, bins=10, density=True)

#Tegning af grafen for normalfordelingen
plt.plot(X_graf,Y)
plt.show()
