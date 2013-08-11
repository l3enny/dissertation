import numpy as np
from scipy.constants import c
from scipy.interpolate import UnivariateSpline as spline
import matplotlib.pyplot as plt


debug = False         # do stuff that is useful
bounds = [900, 1080]  # domain of first pulse
#dx = 0.0762          # separation of measurement locations
#res = 1000           # resolution of interpolation
#smooth = 0.0001      # degree of smoothing


#-----------------------------------------------------------------------------

if debug:
    import matplotlib.pyplot as plt

locations = ["Upstream", "Midstream", "Downstream"]
pressures = ["0.3Torr", "0.5Torr", "1.0Torr", "2.0Torr", "3.0Torr",
             "4.0Torr", "8.0Torr", "16.0Torr"]
pressures = ["4.0Torr", "8.0Torr", "16.0Torr"]
transitions = [389, 396, 402, 447, 492, 501, 587, 667, 707, 728]
wavelengths = np.array([388.86, 396.47, 402.62, 447.15, 471.31, 492.19,
                        501.57, 587.56, 667.82, 706.52, 728.13]) * 1e-9

for p in pressures:
    print "Analyzing", p[:3], p[-4:], "..."

    v_a = []
    v_b = []
    v_c = []
    peak_intensities = []

    for t in transitions:
        if t == 471:
            # Ignore the case of the missing data
            continue
        peak_times = []
        peak_dI = []

        for l in locations:
            # load data for transition
            data = np.loadtxt("/".join((l, p, "C1" + str(t) + "00000.txt")),
                              delimiter=",", skiprows=5)

            # extract data to individual arrays
            times = data[:, 0]
            intensities = -data[:, 1]

            # pick out most intense transition
            if l is "Upstream":
                peak_intensities.append(max(intensities))

            # crop data to pre-determined range
            times = times[bounds[0]:bounds[1]]
            intensities = intensities[bounds[0]:bounds[1]]
