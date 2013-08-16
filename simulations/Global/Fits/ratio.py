import numpy as np
from scipy.constants import c, h, k, e
from scipy.optimize import curve_fit, fixed_point, bisect
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline


debug = False         # do stuff that is useful
scheme = "n4"

if scheme == "n3":
    l_ki = np.array([7.06720, 7.283357]) * 1e-7
    A_ki = np.array([2.785e7, 1.830e7])
    transitions = [13, 19]
    confile = "temperature_ratio1.csv"
    outname = "ratio1_temperatures.csv"
    diagname = "ratios1.csv"
    bounds = [0.14442, 3.8352]

if scheme == "n4":
    l_ki = np.array([4.71317110, 4.9219310128]) * 1e-7
    A_ki = np.array([0.9521e6, 1.986e7])
    transitions = [58, 109]
    confile = "temperature_ratio2.csv"
    outname = "ratio2_temperatures.csv"
    diagname = "ratios2.csv"
    bounds = [0.14442, 4.6586]


#-----------------------------------------------------------------------------

if debug:
    import matplotlib.pyplot as plt

# File and directory structure as well as analysis conditions
directories = ["1.0 Torr", "4.0 Torr", "8.0 Torr (D)", "8.0 Torr (M)",
               "8.0 Torr (U)"]

# Physical values for the transitions in question
energies = (h * c) / l_ki

for d in directories:
    print "Analyzing %s" % d

    # load simulation data
    prefix = "".join((d[0], "torr"))
    try:
        emissions = np.loadtxt("/".join((d, prefix)) + "_emissions.csv",
                               delimiter=",")
    except IOError:
        continue
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

    # Write out ratio file for in-progress diagnostics
    with open("/".join((d, diagname)), mode="w") as f:
        np.savetxt(f, ratios, delimiter=",")

    conversion = np.loadtxt(confile, delimiter=",", skiprows=1)
    temperatures = np.zeros(len(ratios))
    cspline = UnivariateSpline(conversion[200:, 0], conversion[200:, 1], s=0)

    for i in range(len(ratios)):
        if ratios[i] < conversion[200, 1] or ratios[i] > conversion[-1, 1]:
            temperatures[i] = 0.0
        else:
            try:
                #temperatures[i] = fixed_point(cspline, ratios[i])
                temperatures[i] = bisect(lambda x: cspline(x) - ratios[i],
                                         conversion[200, 0], conversion[-1, 0])
            except RuntimeError:
                temperatures[i] = 0.0

    with open("/".join((d, outname)), mode="w") as f:
        np.savetxt(f, temperatures, delimiter=",")
