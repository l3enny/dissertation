import numpy as np
from scipy.interpolate import UnivariateSpline as spline
from scipy.constants import k, e
import matplotlib.pyplot as plt

# This script makes a simplified calculation of the final metastable
# and electron density for a fixed electron temperature

P = 1.0
dt = 5e-12
T = 5e-9
res = 100
debug = True

N_0 = P * 133.3224 / (k * 300)

temperatures = np.logspace(0,3,num=res)
K_iz = np.load("ion_rateslong.npy")
K_m = np.load("nm_rateslong.npy")

K_iz_s = spline(temperatures, K_iz, s=0)
K_m_s = spline(temperatures, K_m, s=0)

def dn_edt(T_e):
    return N_0 * n_e * K_iz_s(T_e)

def dN_mdt(T_e):
    return N_0 * n_e * K_m_s(T_e)

N_m_f = np.zeros(res)
n_e_f = np.zeros(res)
for i in range(res):
    # set initial conditions
    n_e = 1
    N_m = 0
    t = 0
    while t < T:
        n_e += dn_edt(temperatures[i]) * dt
        N_m += dN_mdt(temperatures[i]) * dt
        t += dt
    N_m_f[i] = N_m
    n_e_f[i] = n_e
 
if debug:
    plt.plot(temperatures, N_m_f)
    plt.plot(temperatures, n_e_f)
    plt.legend(["Metastable", "Electron"])
    plt.xlabel("Electron Temperature (eV)")
    plt.ylabel("Normalized Density (a.u.)")
    plt.show()

np.save("maxnm.npy", N_m_f)
np.save("maxne.npy", n_e_f)
