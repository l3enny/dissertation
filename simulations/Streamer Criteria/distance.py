import numpy as np
from scipy.constants import *
from scipy.interpolate import UnivariateSpline

P = 1.0
Tg = 300

Ng = lambda P: 133.332 * P / (k * Tg)

mu_data = np.loadtxt('../BOLSIG+/mobility.dat', delimiter='\t', skiprows=1)
E_sim = mu_data[:, 0] * 1e-21 * Ng
mu = UnivariateSpline(E_sim, mu_data[:, 1], s=0)
alpha_data = np.loadtxt('../BOLSIG+/townsend_coeff.dat', delimiter='\t', skiprows=1)
alpha = UnivariateSpline(E_sim, alpha_data[:, 1], s=0)

ENg = data[:, 0]
def E(t):
    slope = 1e3
    tm = 25e-9
    if t > tm:
        return 0.0
    else:
        return slope * t

E_s = []
t = 0.0
