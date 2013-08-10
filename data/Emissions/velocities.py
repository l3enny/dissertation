import numpy as np
from scipy.constants import c
from scipy.interpolate import UnivariateSpline as spline
import matplotlib.pyplot as plt


debug = False        # do stuff that is useful
dx = 0.0762          # separation of measurement locations
range = [900, 1080]  # domain of first pulse


#-----------------------------------------------------------------------------

if debug:
    import matplotlib.pyplot as plt

locations = ["Upstream", "Midstream", "Downstream"]
pressures = ["0.3Torr", "0.5Torr", "1.0Torr", "2.0Torr", "3.0Torr",
             "4.0Torr", "8.0Torr", "16.0Torr"]
#pressures = ["3.0Torr"]
#transitions = [389, 396, 402, 447, 492, 501, 587, 667, 707, 728]
transitions = [667]

for p in pressures:
    print "Analyzing", p[:3], p[-4:], "..."

    v_a = []
    v_b = []
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
            times = times[range[0]:range[1]]
            intensities = intensities[range[0]:range[1]]

            # generate derivative of intensities, find peak growth time
            dI = intensities[1:] - intensities[:-1]
            i = np.where(dI == max(dI))
            peak_times.append(times[i])
            peak_dI.append(dI[i])

            plt.plot(times, intensities)

        v_a.append(dx / (peak_times[1] - peak_times[0]))
        v_b.append(dx / (peak_times[2] - peak_times[1]))

    plt.legend(locations)
    plt.title(p)
    plt.show()

    i = np.where(peak_intensities == max(peak_intensities))[0]
    print "Upstream velocity: %e (m/s)" % v_a[i]
    print "Downstream velocity: %e (m/s)\n" % v_b[i]
    #j = np.where(peak_dI == max(peak_dI))[0]
    #print transitions[j]
    #print max(peak_dI)
