import numpy as np
from scipy.integrate import trapz

input = "eedfs.dat"

def mean_energy(E, f):
    return trapz(f * E**1.5, E)


runs = []
temperatures = []
with open(input, mode="r") as f:

    i = 0
    read = False
    energies = []
    eedf = []
    anisotropy = []

    for line in f:

        # How to read
        if read:
            try:
                data = line.split()
                energies.append(float(data[0]))
                eedf.append(float(data[1]))
                anisotropy.append(float(data[2]))
            except IndexError:
                read = False
                run = np.array([energies, eedf, anisotropy]).T
                temperatures.append(mean_energy(run[:, 0], run[:, 1]))
                runs.append(run)
                energies = []
                eedf = []
                anisotropy = []

        # Begin reading in from each line
        if "Anisotropy" in line:
            read = True

np.save("bolsig.npy", runs)
np.save("btemps.npy", temperatures)
