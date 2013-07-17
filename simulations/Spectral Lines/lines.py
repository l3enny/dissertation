import numpy as np
from numpy import sqrt, log, pi, exp
from scipy.special import wofz
import matplotlib.pyplot as plt

fwhm = 1.0

def G(x):
    c = fwhm / (2 * sqrt(2 * log(2)))
    a = 1 / (c * sqrt(2 * pi))
    return a * exp(-x**2 / (2 * c**2))

def L(x):
    gamma = 0.5 * fwhm
    return gamma / (pi * (x**2 + gamma**2))

def V(x):
    gamma = 0.6107 / 2
    sigma = 0.6107 / (2 * sqrt(2 * log(2)))
    z = (x + 1j * gamma) / (sigma * sqrt(2))
    return wofz(z).real / (sigma * sqrt(2*pi))

x = np.linspace(-3, 3, 200)

np.savetxt('x.csv', x, delimiter=',')
np.savetxt('g.csv', G(x), delimiter=',')
np.savetxt('l.csv', L(x), delimiter=',')
np.savetxt('v.csv', V(x), delimiter=',')

#plt.plot(x, G(x))
#plt.plot(x, L(x))
#plt.plot(x, V(x))
#plt.show()
