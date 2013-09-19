import numpy as np
from math import pi
import matplotlib.pyplot as plt

tau = 5e-9
debug = False
signal = "Impulse"

prefixes = ["01", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50"]
N_m_filenames = [i + "_ns_N.npy" for i in prefixes]
t_m_filenames = [i + "_ns_t.npy" for i in prefixes]
out_filenames = [i + "_ns_con.npy" for i in prefixes]

for i in range(len(dirs)):
    N_m = np.loadtxt(N_m_filenames[i], delimiter=",")
    t   = np.loadtxt(t_m_filenames[i], delimiter=",")
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
    
    np.save(out_filenames[i], N_convolve)
