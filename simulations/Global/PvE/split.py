import numpy as np

fn = "25_ns"

data = np.load(fn + ".npy")

np.save(fn + "_t.npy", data[:, 0])
np.save(fn + "_N.npy", data[:, 1])
