import numpy as np
from scipy.constants import c, h, k, e
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline


debug = True          # do stuff that is useful


#-----------------------------------------------------------------------------

if debug:
    import matplotlib.pyplot as plt

# File and directory structure as well as analysis conditions
directories = ["1.0 Torr", "4.0 Torr", "8.0 Torr (D)", "8.0 Torr (M)",
               "8.0 Torr (U)"]
transitions = [58, 109]

# Physical values for the transitions in question
l_ki = np.array([4.71317110, 4.9219310128]) * 1e-7
A_ki = np.array([0.9521e6, 1.986e7])
energies = (h * c) / l_ki

# number of time points in analysis (something of a hack)
num = 5002


for d in directories:
    print "Analyzing %s" % d

    # load simulation data
    prefix = "".join((d[0], "torr"))
    emissions = np.loadtxt("/".join((d, prefix)) + "_emissions.csv", delimiter=",")
    times = np.loadtxt("/".join((d, prefix)) + "_times.csv", delimiter=",")
    
    # initialize arrays
    n = len(times)
    spectra = np.zeros((n, len(transitions)))
    temperatures = np.zeros(n)
    variance = np.zeros(n)

    # eliminate unnecessary data
    for i in range(len(transitions)):
        spectra[:, i] = emissions[:, transitions[i]]

    ratios = spectra[:, 0] / spectra[:, 1]
    conversion = np.loadtxt("temperature_ratio2.csv", delimiter=",", skiprows=1)
    temperatures = np.zeros(len(ratios))

    for i in range(len(ratios)):
        cspline = UnivariateSpline(conversion[200:, 0],
                                   conversion[200:, 1] - ratios[i], s=0)
        try:
            temperatures[i] = cspline.roots()
        except ValueError:
            temperatures[i] = 0.0

    with open("/".join((d, "ratios.csv")), mode="w") as f:
        np.savetxt(f, ratios, delimiter=",")
    with open("/".join((d, "ratio_temperatures.csv")), mode="w") as f:
        np.savetxt(f, temperatures, delimiter=",")
