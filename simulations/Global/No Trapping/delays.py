import numpy as np
import matplotlib.pyplot as plt

loc = ['1.0 Torr/', '4.0 Torr/', '8.0 Torr (D)/', '8.0 Torr (M)/',
       '8.0 Torr (U)/']

prefix = ['1torr', '4torr', '8torr', '8torr', '8torr']

for i in range(len(loc)):
    t = np.loadtxt(loc[i] + prefix[i] + "_times.csv", delimiter=',')
    ne = np.loadtxt(loc[i] + prefix[i] + "_populations.csv", delimiter=',')[:, 19]
    dne = ne[1:] - ne[0:-1]
    if i == 1:
        plt.plot(dne)
        plt.show()
    index = np.where(dne == max(dne))
    print "Peak ionization time:", t[index]
