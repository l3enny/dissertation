import numpy as np

fn = "fitparams.csv"

data = np.loadtxt(fn, delimiter=',', skiprows=1)

Nm = data[:, 2]

np.save("nm_measured.npy", Nm / max(Nm))
