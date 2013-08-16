import numpy as np
from scipy.constants import c, h, k, e
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline


debug = False         # do stuff that is useful
sample_rate = 1000    #
#bounds = [900, 1080] # domain of first pulse
#dx = 0.0762          # separation of measurement locations
#res = 1000           # resolution of interpolation
#smooth = 0.0001      # degree of smoothing


#-----------------------------------------------------------------------------

if debug:
    import matplotlib.pyplot as plt

# File and directory structure as well as analysis conditions
locations = ["Upstream", "Midstream", "Downstream"]
#locations = ["Upstream"]
pressures = ["0.3Torr", "0.5Torr", "1.0Torr", "2.0Torr", "3.0Torr",
             "4.0Torr", "8.0Torr", "16.0Torr"]
#pressures = ["16.0Torr"]
transitions = ["389", "396", "402", "447", "471", "492", "501", "587", "667", "707",
               "728"]

# Physical values for the transitions in question
l_ki = np.array([3.8897, 3.9659, 4.0273, 4.4728, 4.7145, 4.9233, 5.0171, 5.8773,
                 6.6800, 7.0672, 7.2834]) * 1e-7
A_ki = np.array([9.48e6, 6.95e6, 1.16e7, 2.46e7, 9.52e6, 1.99e7, 1.34e7, 7.07e7,
                 6.37e7, 2.79e7, 1.83e7])
g_k  = np.array([9,      3,      15,     15,     9,       5,      3,      15,     5,
                 3,      1])
energies = (h * c) / l_ki

# number of time points in analysis (something of a hack)
num = 5002

def calibration():
    # Spectral irradiance standard: M-1179 at 6.5 A
    l_actual = np.array([250,  260,  270,   280,  290,  300,  310,  320,  330,
                         340,  350,  360,   370,  380,  390,  400,  450,  500,
                         555,  600,  654.6, 700,  800,  900,  1050, 1150, 1200,
                         1300, 1540, 1600,  1700, 2000, 2100, 2300, 2400, 2500]
                       ) * 1e-9
    I_actual = np.array([5.527e-9, 9.427e-9, 1.510e-8, 2.377e-8,
        3.509e-8, 5.049e-8, 7.028e-8, 9.580e-8, 1.273e-7, 1.652e-7, 2.110e-7,
        2.635e-7, 3.243e-7, 3.921e-7, 4.719e-7, 5.570e-7, 1.101e-6, 1.790e-6,
        2.617e-6, 3.264e-6, 3.975e-6, 4.454e-6, 5.093e-6, 5.275e-6, 4.935e-6,
        4.529e-6, 4.304e-6, 3.838e-6, 2.806e-6, 2.588e-6, 2.255e-6, 1.497e-6,
        1.307e-6, 1.002e-6, 8.777e-7, 7.833e-7])
    spline_actual = UnivariateSpline(l_actual, I_actual, s=0)

    # Measured response of fiber/SPEX HR460/etc.--the whole apparatus
    dark = 241e-6
    I_measured = np.array([27.63, 32.36, 37.36, 44.63, 44.71, 44.74, 44.80, 44.67,
                           41.01, 22.95, 10.08]) * 1e-3 - dark

    # correction factor
    Q = spline_actual(l_ki) / I_measured
    return Q

Q = calibration()
samples = np.zeros((1 + num / sample_rate, len(transitions)))
for p in pressures:
    print "Analyzing", p[:3], p[-4:], "..."
    for l in locations:

        # initialize arrays
        spectra = np.zeros((num, len(transitions)))
        temperatures = np.zeros(num)
        variance = np.zeros(num)

        # Assemble histories into spectra
        for i in range(len(transitions)):
            
            # load data for transition
            try:
                data = np.loadtxt("/".join((l, p, "C1" + transitions[i] +
                                  "00000.txt")), delimiter=",", skiprows=5)
            except IOError:
                continue

            # extract data to individual arrays
            times = data[:, 0]
            intensities = -(data[:, 1] - np.mean(data[:600, 1]))

            # calibrate data and insert into record
            spectra[:, i] = Q[i] * intensities
            

        output = np.zeros((num, 2))

        with open("/".join((l, p, "spectra.csv")), mode="w") as f:
            f.write(",".join(transitions) + "\n")
            np.savetxt(f, spectra, delimiter=",")
