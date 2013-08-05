import numpy as np
from numpy import exp
from math import sqrt
from scipy.constants import e, pi
from scipy.integrate import trapz
from scipy.interpolate import SmoothBivariateSpline as spline2d
from scipy.interpolate import UnivariateSpline as spline
from scipy.interpolate import griddata
import os

debug = False
test_spline = False
resolution = 200

boltzmann = np.load("../../../BOLSIG+/Distributions/bolsig.npy")
btemps = np.load("../../../BOLSIG+/Distributions/btemps.npy")

size = 0
for i in range(len(boltzmann)):
    size += boltzmann[i].shape[0]

x = np.zeros(size)
y = np.zeros(size)
z = np.zeros(size)

index = 0
for i in range(len(boltzmann)):
    dim = boltzmann[i].shape[0]
    x[index:index + dim] = boltzmann[i][:, 0]
    y[index:index + dim] = btemps[i]
    z[index:index + dim] = boltzmann[i][:, 1]
    index += dim

points = np.array([x, y]).T

def maxwellian(E, Te):
    return 3**1.5 / sqrt(2*pi) * Te**-1.5 * exp(-1.5 * E/Te)

def normalize(E, f):
    Q = trapz(f * E**0.5, E)
    return f / Q

def mean_energy(E, f):
    return trapz(f * E**1.5, E)

# Initialize arrays
pic_eedfs = np.zeros((40, 200))
maxwellian_eedfs = np.zeros((40, resolution))
boltzmann_eedfs = np.zeros((40, resolution))

for fn in os.listdir('.'):
    if "eedf" in fn:
        # Determine order in simulation
        step = fn.split("eedf_")[1]
        step = int(step.split(".txt")[0]) - 1

        # Load in data
        data = np.loadtxt(fn, delimiter="\t\t", skiprows=2)
        energies = data[:, 0] # This is in eV!
        eedf = data[:, 1]

        normed_eedf = normalize(energies, eedf)

        # Calculate mean energy of distribution
        temperature = mean_energy(energies, normed_eedf)        
        high_res = np.linspace(min(energies), max(energies), num=resolution)
        maxwellian_eedf = maxwellian(high_res, temperature)
        xi = np.zeros((resolution, 2))
        xi[:, 0] = high_res
        xi[:, 1] = temperature
        boltzmann_eedf = griddata(points, z, xi, method='cubic')

        # Save normalized EEDFs to output array
        pic_eedfs[step, :] = normed_eedf
        maxwellian_eedfs[step, :] = maxwellian_eedf
        boltzmann_eedfs[step, :] = boltzmann_eedf

        # Save individual files for time step comparisons
        np.savetxt("max_" + str(step) + ".txt", maxwellian_eedf, delimiter=',')
        np.savetxt("pic_" + str(step) + ".txt", normed_eedf, delimiter=',')
        np.savetxt("bol_" + str(step) + ".txt", boltzmann_eedf, delimiter=',')

        if debug:

            # Calculate consistency checks
            mint = trapz(maxwellian_eedf * high_res**0.5, high_res)
            pint = trapz(normed_eedf * energies**0.5, energies)

            print "PIC mean = %e eV" % temperature
            print "Maxwellian mean = %e eV" % mean_energy(high_res,
                                                          maxwellian_eedf)
            print "Maxwellian integral = %e" % mint
            print "Normalized PIC integral = %e" % pint

            import matplotlib.pyplot as plt
            plt.semilogy(high_res, maxwellian_eedf)
            plt.semilogy(energies, normed_eedf)
            plt.semilogy(energies, boltzmann_eedf)
            plt.legend(('Maxwellian', 'PIC', 'Boltzmann'))
            plt.axis((0, 50, 1e-5, 1))
            plt.show()

np.save("pic.npy", pic_eedfs)
np.save("maxwellian.npy", maxwellian_eedfs)
np.save("boltzmann.npy", boltzmann_eedfs)
