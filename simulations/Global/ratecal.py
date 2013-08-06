import numpy as np
from scipy.interpolate import UnivariateSpline as spline
from scipy.constants import e, k

rates = np.load("ion_rates.npy")
Te = np.logspace(-1, 1.5, num=1e2) * e
K = spline(Te, rates, s=0)

loc = ["./Electric Field/0.9/",
       "./Electric Field/1.1/",
       "./Nominal/"]

for l in loc:
    temperatures = np.loadtxt(l + "4torr_temperatures.csv", delimiter=",")   
    output = []
    for T in temperatures:
        output.append(K(T * k))
    np.savetxt(l + "ion_rates.csv", output, delimiter=",")

