import random
from math import sqrt, pi, e
import matplotlib.pyplot as plt


def normal(x, m, v):
    return 1/(sqrt(2*pi*v)) * e**(-((x-m)**2)/(2*v))

X = [random.random() for i in range(100)]

middel = 0
sum = 0
antal = len(X)
for i in range(0,len(X)):
    v =  X[i]
    sum += v

middel = sum / antal

varians = 0
sum = 0
for i in range(len(X)):
    d = (X[i] - middel)**2
    sum += d

varians = sum / (len(X)-1)

print(middel, varians)

min = 0
max = 1
step = (max - min)/100

X_graf = [min + x * step for x in range(100)]

Y_graf = [normal(X_graf[i], middel, varians) for i in range(0,len(X_graf))]

plt.plot(X_graf, Y_graf)
plt.show()
