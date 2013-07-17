from math import log, exp, sqrt
import numpy as np
from scipy.constants import *
from scipy.interpolate import UnivariateSpline as Spline
from scipy.integrate import trapz
import matplotlib.pyplot as plt

# User settings
P    = 4.0            # pressure, Torr
T_g  = 300            # gas temperature, K
#dENdt = 1e-21 / 1e-09 # rate of rise of electric field, V-m^2/s
#EN_m = 500e-10        # maximum applied electric field, V-m^2
eps  = 1e-20          # solution convergence criteria
h    = 1e-12          # integrator time step
Q = 6.00e-20          # mean momentum transfer cross section, m^2
debug = False

# Values @ breakdown in equilibrium
EN_0 = 4.4e-21        # Breakdown reduced electric field, V-m^2

# Derived quantities
N_g  = 133.332 * P / (k * T_g)  # gas density
l_e = 1 / (Q * N_g)        # mean free path, m

# Load BOLSIG+ simulation data
muN_data = np.loadtxt('../BOLSIG+/mobility.dat', delimiter='\t', skiprows=1)
alphaN_data = np.loadtxt('../BOLSIG+/townsend_coeff.dat', delimiter='\t', skiprows=1)
energy_data = np.loadtxt('../BOLSIG+/mean_energy.dat', delimiter='\t',
        skiprows=1)

energy_spline = Spline(1e-21 * energy_data[:, 0], energy_data[:, 1] * e, s=0)
mu_spline = Spline(1e-21 * muN_data[:, 0], muN_data[:, 1] / N_g, s=0)
alpha_spline = Spline(1e-21 * alphaN_data[:, 0], alphaN_data[:, 1] * N_g, s=0)

def EN(t):
    #return (dENdt * t, EN_m)
    return dENdt * t

def C_e(EN):
    energy = energy_spline(EN)
    if energy < 0:
        energy = 300 * k
    return (2./3) * (2. * energy * e / m_e)**0.5

def mu_func(t):
    if EN(t) < 1e-21 * muN_data[0, 0]:
        return muN_data[0, 1] / N_g
    else:
        return mu_spline(EN(t))


delays = np.logspace(-10, -8)
slopes = EN_0 / delays
xi_c = []
R_c = []
for dENdt in slopes:
    t0  = EN_0 / dENdt
    t = 0.0
    E_r = 0.0
    xi  = 0.0
    alpha = 0.0
    R = 0.0
    i = 0
    N_e = 1.0
    exponent = 0.0
    while E_r <= EN(t) * N_g or N_e < 2:
        if t > t0:
            # Calculate avalanche length
            dxi = mu_func(t) * EN(t) * N_g * h
            xi += dxi

            # Calculate free diffusion radius
            D = l_e * C_e(EN(t)) / 3
            dR = (2 * D * h)**0.5
            R += dR

            # Calculate electron population
            alpha = alpha_spline(EN(t))
            dexponent = alpha * dxi
            exponent += dexponent
            N_e = exp(exponent)

            # Calculate maximum avalanche field
            E_r = 0.428 * e * N_e / (4 * pi * epsilon_0 * R**2)

        t += h
        i += 1

        if debug and i % 1000 == 0:
            print "R =", R
            print "xi =", xi
            print "EN_r =", E_r / N_g
            print "EN =", EN(t)
            print "a =", alpha
            print "N_e =", N_e, '\n'

        if i > 1e7:
            print "Aborting, too many steps."
            break

    # Save the interesting stuff
    xi_c.append(xi)
    R_c.append(R)
    print "---=== For %e (Td/s) ===---" % dENdt
    print "Solution Steps:  ", i
    print "Critical Radius: ", R
    print "Critical Length: ", xi
    print "Critical Field:  ", 1e21 * E_r / N_g, '\n'

np.savetxt('slopes.dat', slopes, delimiter=',')
np.savetxt('delays.dat', delays, delimiter=',')
np.savetxt('lengths.dat', xi_c, delimiter=',')
np.savetxt('delays.dat', R_c, delimiter=',')
np.savetxt('ne.dat', np.array(R_c)**-3, delimiter=',')
