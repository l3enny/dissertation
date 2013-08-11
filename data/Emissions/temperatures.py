import numpy as np
from scipy.constants import c, h
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


debug = False         # do stuff that is useful
#bounds = [900, 1080]  # domain of first pulse
#dx = 0.0762          # separation of measurement locations
#res = 1000           # resolution of interpolation
#smooth = 0.0001      # degree of smoothing


#-----------------------------------------------------------------------------

if debug:
    import matplotlib.pyplot as plt

locations = ["Upstream", "Midstream", "Downstream"]
pressures = ["0.3Torr", "0.5Torr", "1.0Torr", "2.0Torr", "3.0Torr",
             "4.0Torr", "8.0Torr", "16.0Torr"]
transitions = ["389", "396", "402", "447", "492", "501", "587", "667", "707",
               "728"]

Lki = np.array([3.8897, 3.9659, 4.0273, 4.4728, 4.9233, 5.0171, 5.8773, 6.6800,
                7.0672, 7.2834]) * 1e-7
energies = (h * c) / wavelengths
Aki = np.array([9.46e6, 6.95e6, 1.16e7, 2.46e7, 1.99e7, 1.34e7, 7.07e7, 6.37e7,
                2.79e7, 1.83e7])
gk = np.array([9, 3, 15, 15, 5, 3, 15, 5, 3, 1])

num = 5000

def calibrate(I):
    actual = np.array([])
    measured = np.array([])
    Q = actual / measured
    return I * Q

def model(x, a, b):
    return a*x + b

for p in pressures:
    print "Analyzing", p[:3], p[-4:], "..."

    for l in locations:

        spectra = np.zeros((num, len(transitions)))
        temperatures = np.zeros(num)
        for i in range(len(transitions)):
            # load data for transition
            data = np.loadtxt("/".join((l, p, "C1" + transitions[i] + "00000.txt")),
                              delimiter=",", skiprows=5)

            # extract data to individual arrays
            times = data[:, 0]
            intensities = calibrate(-data[:, 1])
            spectra[:, i] = intensities

        # crop data to pre-determined range
        #times = times[bounds[0]:bounds[1]]
        #intensities = intensities[bounds[0]:bounds[1], :]

        for i in range(num):
            Iki = intensities[i, :]
            y = np.log(Iki * Lki / (gk * Aki))
            popt, pconv = curve_fit(model, energies, y)
            temperatures[i] = popt[0]
