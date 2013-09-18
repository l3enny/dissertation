import numpy as np
from scipy.constants import c, h, k, e
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline


debug = True          # do stuff that is useful
#bounds = [900, 1080]  # domain of first pulse
#dx = 0.0762          # separation of measurement locations
#res = 1000           # resolution of interpolation
#smooth = 0.0001      # degree of smoothing


#-----------------------------------------------------------------------------

if debug:
    import matplotlib.pyplot as plt

# Directory structure and transition indices
directories = ["1.0 Torr", "4.0 Torr", "8.0 Torr (D)", "8.0 Torr (M)",
               "8.0 Torr (U)"]
transitions = [11, 18, 23, 29, 16, 20, 26, 19, 24]

for d in directories:
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

    wavelengths = np.loadtxt("/".join((d, prefix)) + "_wavelengths.csv",
                             delimiter=",")
    wavelengths = np.array([wavelengths[i] for i in transitions]) * 1e9
    header = [str(int(i)) for i in wavelengths]

    with open("/".join((d, "spectra.csv")), mode="w") as f:
        f.write(",".join(header) + "\n")
        np.savetxt(f, spectra, delimiter=",")
