import numpy as np
from math import pi
import matplotlib.pyplot as plt

tau = 5e-9
debug = False
signal = "Impulse"

dirs = ["1.0 Torr", "4.0 Torr", "8.0 Torr (D)", "8.0 Torr (M)", "8.0 Torr (U)"]
files = ["1torr_populations.csv", "4torr_populations.csv",
         "8torr_populations.csv", "8torr_populations.csv",
         "8torr_populations.csv"]
times = ["1torr_times.csv", "4torr_times.csv", "8torr_times.csv",
         "8torr_times.csv", "8torr_times.csv"]

for i in range(len(dirs)):
    N = np.loadtxt(dirs[i] + "/" + files[i], delimiter=",")
    t = np.loadtxt(dirs[i] + "/" + times[i], delimiter=",")
    dt = t[1] - t[0]
    width = tau / dt
    N_m = N[:, 1]
    dim = len(N_m)

    if signal == "Impulse":
        height = 1. / width
        resolution = width
        f = np.zeros(width)
        f[:] = height
    elif signal == "Gaussian":
        sigma = tau / (2  *np.sqrt(2 * np.log(2)))
        resolution = int(12 * sigma / dt)
        x = np.linspace(-6 * sigma, 6 * sigma, num=resolution)
        f = 5e-12 * np.exp(-x**2/(2 * sigma**2)) / (sigma * np.sqrt(2 * pi))
        pass

    N_convolve = np.convolve(N_m, f, mode="full")[resolution/2:-resolution/2 + 1]

    if debug:
        plt.plot(t, N_m)
        plt.plot(t, N_convolve)
        plt.legend(["Initial", "Convolved"])
        plt.show()
    
    np.savetxt(dirs[i] + "/" + "nm_convolved.csv", N_convolve, delimiter=",")
