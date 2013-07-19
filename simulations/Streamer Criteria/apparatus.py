from math import log, exp, sqrt
import numpy as np
from scipy.constants import *
from scipy.interpolate import UnivariateSpline as Spline
from scipy.integrate import trapz
import matplotlib.pyplot as plt

# User settings
P    = 0.30           # pressure, Torr
T_g  = 300            # gas temperature, K
N_g  = 133.332 * P / (k * T_g)  # gas density
h    = 1e-12          # integrator time step
Q = 6.00e-20          # mean momentum transfer cross section, m^2
debug = False

# Values @ breakdown in equilibrium
EN_0 = 4.4e-21        # Breakdown reduced electric field, V-m^2

# Derived quantities
l_e = 1 / (Q * N_g)        # mean free path, m

# Load BOLSIG+ simulation data
muN_data = np.loadtxt('../BOLSIG+/mobility.dat', delimiter='\t', skiprows=1)
alphaN_data = np.loadtxt('../BOLSIG+/townsend_coeff.dat', delimiter='\t', skiprows=1)
energy_data = np.loadtxt('../BOLSIG+/mean_energy.dat', delimiter='\t',
        skiprows=1)

energy_spline = Spline(1e-21 * energy_data[:, 0], energy_data[:, 1] * e, s=0)
mu_spline = Spline(1e-21 * muN_data[:, 0], muN_data[:, 1] / N_g, s=0)
alpha_spline = Spline(1e-21 * alphaN_data[:, 0], alphaN_data[:, 1] * N_g, s=0)


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


EN_m = np.logspace(0,3) / N_g
slopes = EN_m / 4e-9
xi_c = []
R_c = []
for j in range(len(slopes)):
    def EN(t):
        return min(dENdt * t, EN_m[j])
        #return dENdt * t
    dENdt = slopes[j]
    t0  = EN_0 / dENdt
    t = 0.0
    E_r = 0.0
    xi  = 0.0
    alpha = 0.0
    R = 0.0
    i = 0
    N_e = 1.0
    exponent = 0.0
    abort = False
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

        if t > 25e-9:
            print "Aborting %e, breakdown not achieved." % dENdt
            print "Electron Multiplication =", N_e, '\n'
            abort = True
            break

    if abort:
        xi_c.append(0.0)
        R_c.append(0.0)
    else:
        # Save the interesting stuff
        xi_c.append(xi)
        R_c.append(R)
        print "---=== For %e (Td/s) ===---" % dENdt
        print "Solution Steps:  ", i
        print "Critical Radius: ", R
        print "Critical Length: ", xi
        print "Critical Field:  ", 1e21 * E_r / N_g, '\n'

#np.savetxt('slopes.dat', slopes, delimiter=',')
#np.savetxt('delays.dat', delays, delimiter=',')
#np.savetxt('lengths.dat', xi_c, delimiter=',')
#np.savetxt('delays.dat', R_c, delimiter=',')
#np.savetxt('ne.dat', np.array(R_c)**-3, delimiter=',')
