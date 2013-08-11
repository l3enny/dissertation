import numpy as np
from scipy.constants import c
from scipy.interpolate import UnivariateSpline as spline
import matplotlib.pyplot as plt


debug = False        # do stuff that is useful
dx = 0.0762          # separation of measurement locations
bounds = [900, 1080]  # domain of first pulse
res = 1000           # resolution of interpolation
smooth = 0.0001      # degree of smoothing


#-----------------------------------------------------------------------------

if debug:
    import matplotlib.pyplot as plt

locations = ["Upstream", "Midstream", "Downstream"]
#pressures = ["0.3Torr", "0.5Torr", "1.0Torr", "2.0Torr", "3.0Torr",
#             "4.0Torr", "8.0Torr", "16.0Torr"]
pressures = ["4.0Torr", "8.0Torr", "16.0Torr"]
transitions = [389, 396, 402, 447, 492, 501, 587, 667, 707, 728]
#transitions = [396]

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

            # generate derivative of intensities, find peak growth time
            dI = intensities[1:] - intensities[:-1]
            Is = spline(times, intensities, s=smooth)
            tf = np.linspace(min(times), max(times), num=res)
            dIs = np.zeros(res)
            for i in range(res):
                dIs[i] = Is.derivatives(tf[i])[1]
            #i = np.where(dI == max(dI))
            i = np.where(dIs ==max(dIs))
            peak_times.append(tf[i])

        v_a.append(dx / (peak_times[1] - peak_times[0]))
        v_b.append(dx / (peak_times[2] - peak_times[1]))
        v_c.append(2 * dx / (peak_times[2] - peak_times[0]))


    # Check for validity
    v_a = filter(lambda x: not(np.isnan(x) or np.isinf(x)), v_a)
    v_b = filter(lambda x: not(np.isnan(x) or np.isinf(x)), v_b)
    v_c = filter(lambda x: not(np.isnan(x) or np.isinf(x)), v_c)

    i = np.where(peak_intensities == max(peak_intensities))[0]
    print "Upstream velocity: %e +/- %e (m/s)" % (np.mean(v_a), np.std(v_a))
    print "Downstream velocity: %e +/- %e (m/s)" % (np.mean(v_b), np.std(v_b))
    print "Overall velocity: %e +/- %e (m/s)\n" % (np.mean(v_c), np.std(v_c))
