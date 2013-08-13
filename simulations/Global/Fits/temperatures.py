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
transitions = [22, 155, 94, 109, 47, 31, 40, 13, 19]

# Physical values for the transitions in question
l_ki = np.array([3.8897, 3.9659, 4.4728, 4.9233, 5.0171, 5.8773, 6.6800,
                 7.0672, 7.2834]) * 1e-7
A_ki = np.array([9.48e6, 6.95e6, 2.46e7, 1.99e7, 1.34e7, 7.07e7, 6.37e7,
                 2.79e7, 1.83e7])
g_k  = np.array([9,      3,      15,     5,      3,      15,     5,
                 3,      1])
energies = (h * c) / l_ki


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

    # generate Boltzmann plot and fit for each time point
    for i in range(len(times)):
        I_ki = spectra[i, :]
        y = np.log(I_ki * l_ki / (g_k * A_ki))

        try:
            popt, pconv = curve_fit(lambda x, a, b: a*x + b, energies, y,
                                    p0=(0.5/e, -20))
            if pconv is np.inf:
                pconv = np.zeros((2,2))
        except ValueError:
            popt, pconv = (np.zeros(2), np.zeros((2,2,)))

        temperatures[i] = -1/(popt[0] * e)
        variance[i] = -1/(np.sqrt(pconv[0,0]) * e)

        if debug:
            if i%200 == 0:
                x = np.linspace(min(energies), max(energies))
                f = lambda x: popt[0] * x + popt[1]
                plt.plot(energies / e, y)
                plt.plot(x / e, f(x))
                plt.legend(('Measured', 'Fitted'))
    plt.show()

    output = np.zeros((len(times), 2))
    output[:, 0] = temperatures
    output[:, 1] = variance

    with open("/".join((d, "boltplot.csv")), mode="w") as f:
        f.write("Temperatures,+-\n")
        np.savetxt(f, output, delimiter=",")
