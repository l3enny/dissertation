from math import log, exp
import numpy as np
from scipy.constants import *
from scipy.interpolate import UnivariateSpline as Spline
from scipy.integrate import quad, trapz
from scipy.special import erf
import matplotlib.pyplot as plt

# User settings
P    = 1.0           # pressure, Torr
T_g  = 300           # gas temperature, K
dENdt = 1e-21 / 1e-09 # rate of rise of electric field, V-m^2/s
EN_m = 100e-21       # maximum applied electric field, V-m^2
eps  = 1e-20         # solution convergence criteria
h    = 1e-12         # integrator time step

# Values @ breakdown in equilibrium
EN_0 = 4.4e-21    # Breakdown reduced electric field, V-m^2
lambda_e = 3.34e-19   # mean momentum transfer cross section, m^2

# Derived quantities
t0  = EN_0 / dENdt
N_g  = 133.332 * P / (k * T_g) # gas density

# Load BOLSIG+ simulation data
muN_data = np.loadtxt('../BOLSIG+/mobility.dat', delimiter='\t', skiprows=1)
alphaN_data = np.loadtxt('../BOLSIG+/townsend_coeff.dat', delimiter='\t', skiprows=1)
energy_data = np.loadtxt('../BOLSIG+/mean_energy.dat', delimiter='\t',
        skiprows=1)

energy_spline = Spline(1e-21 * energy_data[:, 0], energy_data[:, 1], s=0)
muN_spline = Spline(1e-21 * muN_data[:, 0], muN_data[:, 1], s=0)
alpha_spline = Spline(1e-21 * alphaN_data[:, 0], alphaN_data[:, 1] * N_g, s=0)

def EN(t):
    return min(dENdt * t, EN_m)

def C_e(EN):
    energy = energy_spline(EN)
    if energy < 0:
        energy = 300 * k
    return (2./3) * (2. * energy * e / m_e)**0.5

t = 0.0
u_e = [0.0]
E_r = [0.0]
xi  = [0.0]
alpha = [0.0]
while E_r[-1] <= EN(t):
    u_e.append(u_e[-1] + muN_spline(EN(t)) * dENdt * h)
    if t > t0:
        xi.append(xi[-1] + muN_spline(EN(t)) * dENdt * h)
        alpha.append(alpha_spline(EN(t)))
        E_r.append(0.0511 * e * np.mean(u_e) * exp(trapz(alpha, xi))
                   / (epsilon_0 * lambda_e * C_e(EN(t)) * xi[-1]))
    else:
        E_r.append(0.0)
        alpha.append(0.0)
        xi.append(0.0)
    t += h
print E_r
