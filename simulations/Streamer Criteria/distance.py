from math import log, exp, sqrt
import numpy as np
from scipy.constants import *
from scipy.interpolate import UnivariateSpline as Spline
from scipy.integrate import trapz
import matplotlib.pyplot as plt

# User settings
P    = 1000.0         # pressure, Torr
T_g  = 300            # gas temperature, K
h    = 1e-11         # integrator time step
debug = False         # debug output setting

# Derived quantities
N_g  = 133.3224 * P / (k * T_g)  # gas density

# Load BOLSIG+ simulation data
muN_data = np.loadtxt('../BOLSIG+/mobility.dat', delimiter='\t', skiprows=1)
alphaN_data = np.loadtxt('../BOLSIG+/townsend_coeff.dat', delimiter='\t', skiprows=1)
diff_data = np.loadtxt('../BOLSIG+/diff_coeff.dat', delimiter='\t', skiprows=1)

# Find the special values of E
Eb_index = np.where(alphaN_data[:,1] > 0)[0][0]
EN_0 = alphaN_data[Eb_index, 0] * 1e-21
E_max = 1e-21 * muN_data[-1, 0]
E_min = 1e-21 * muN_data[0, 0]

# Generate splines for interpolating data
mu_spline = Spline(1e-21 * muN_data[:, 0], muN_data[:, 1] / N_g, s=0)
alpha_spline = Spline(1e-21 * alphaN_data[:, 0], alphaN_data[:, 1] * N_g, s=0)
diff_spline = Spline(1e-21 * diff_data[:, 0], diff_data[:, 1] / N_g, s=0)

def D(EN):
    if EN < E_min:
        return diff_data[0, 1] / N_g
    else:
        return diff_spline(EN)

# Mobility
def mu_func(EN):
    if EN < E_min:
        return muN_data[0, 1] / N_g
    else:
        return mu_spline(EN)

delays = np.logspace(-10, -8)
slopes = EN_0 / delays
xi_c = []
R_c = []
for dENdt in slopes:
    def EN(t):
        return dENdt * t

    t0  = EN_0 / dENdt
    t = 0.0
    E_r = 0.0
    xi  = 0.0
    alpha = 0.0
    R = 0.0
    i = 0
    N_e = 1.0
    exponent = 0.0
    D_avg = 0.0
    while E_r <= EN(t) * N_g or N_e < 2:
        if t > t0:
            # Calculate avalanche length
            dxi = mu_func(EN(t)) * EN(t) * N_g * h
            xi += dxi

            # Calculate free diffusion radius
            D_avg = (D_avg * (i - 1) + D(EN(t))) / i
            R = (2 * D_avg * (t - t0))**0.5

            # Calculate electron population
            dexponent = alpha_spline(EN(t)) * dxi
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
            print "N_e =", N_e
            print "mu =", mu_func(EN(t)), '\n'
            raw_input('')

        if i > 1e7 or EN(t) > E_max:
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

np.savetxt(str(P) + 'slopes.dat', slopes, delimiter=',')
np.savetxt(str(P) + 'delays.dat', delays, delimiter=',')
np.savetxt(str(P) + 'lengths.dat', xi_c, delimiter=',')
np.savetxt(str(P) + 'delays.dat', R_c, delimiter=',')
np.savetxt(str(P) + 'ne.dat', np.array(R_c)**-2, delimiter=',')
