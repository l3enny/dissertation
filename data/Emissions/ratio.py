import numpy as np
from scipy.constants import c, h, k, e
from scipy.optimize import curve_fit, bisect
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline


debug = True          # do stuff that is useful
scheme = "n3"

if scheme == "n3":
    print "--== Ratio of 706.7/728.3 ==--"
    l_ki = np.array([7.06720, 7.283357]) * 1e-7
    A_ki = np.array([2.785e7, 1.830e7])
    transitions = ["707", "728"]
    confile = "temperature_ratio1.csv"
    outname = "ratio1_temperatures.csv"
    diagname = "ratios1.csv"
    V_pmt =  np.array([22.95, 10.08]) * 1e-3 

if scheme == "n4":
    print "--== Ratio of 471.3/492.2 ==--"
    l_ki = np.array([4.71317110, 4.9219310128]) * 1e-7
    A_ki = np.array([0.9521e6, 1.986e7])
    transitions = ["471", "492"]
    confile = "temperature_ratio2.csv"
    outname = "ratio2_temperatures.csv"
    diagname = "ratios2.csv"
    V_pmt =  np.array([44.71, 44.74]) * 1e-3 

#-----------------------------------------------------------------------------

if debug:
    import matplotlib.pyplot as plt

# File and directory structure as well as analysis conditions
locations = ["Upstream", "Midstream", "Downstream"]
pressures = ["0.3Torr", "0.5Torr", "1.0Torr", "2.0Torr", "3.0Torr",
             "4.0Torr", "8.0Torr", "16.0Torr"]

# Physical values for the transitions in question
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
    I_measured = V_pmt - dark

    # correction factor
    Q = spline_actual(l_ki) / I_measured
    return Q

Q = calibration()

for p in pressures:
    print "Analyzing", p[:3], p[-4:], "..."
    for l in locations:

        if p == "3.0Torr" and l == "Upstream":
            continue

        # initialize arrays
        spectra = np.zeros((num, len(transitions)))
        temperatures = np.zeros(num)
        variance = np.zeros(num)

        # Assemble histories into spectra
        for i in range(len(transitions)):
            
            # load data for transition
            data = np.loadtxt("/".join((l, p, "C1" + transitions[i] +
                              "00000.txt")), delimiter=",", skiprows=5)

            # extract data to individual arrays
            times = data[:, 0]
            intensities = -(data[:, 1] - np.mean(data[:600, 1]))

            # calibrate data and insert into record
            spectra[:, i] = Q[i] * intensities

        # calculate ratios and write out
        ratios = spectra[:, 0] / spectra[:, 1]
        with open("/".join((l, p, diagname)), mode="w") as f:
            np.savetxt(f, ratios, delimiter=",")
            
        # load reference conversion file
        conversion = np.loadtxt(confile, delimiter=",", skiprows=1)
        cspline = UnivariateSpline(conversion[1650:, 0], conversion[1650:, 1], s=0)

        # generate empty array for temperatures
        temperatures = np.zeros(len(ratios))
        for i in range(len(ratios)):
            if ratios[i] < conversion[-1, 1] or ratios[i] > conversion[1650, 1]:
                temperatures[i] = 0.0
            else:
                temperatures[i] = bisect(lambda x: cspline(x) - ratios[i],
                                         conversion[1650, 0], conversion[-1, 0])

        with open("/".join((l, p, outname)), mode="w") as f:
            np.savetxt(f, temperatures, delimiter=",")
