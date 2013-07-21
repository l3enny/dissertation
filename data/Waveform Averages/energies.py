import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simps
import os

#start = 177e-9
starts = np.linspace(167e-9, 187e-9)
reflect = 138e-9
absorbed = []

t = np.linspace(0,2e3 * 1e-9, 5e3)
dt = (2e3 * 1e-9) / 5e3

dirs = os.walk('.')

for d in dirs:
    if 'current.csv' in d[2]:
        print "Maximizing absorption\n"
        for start in starts:
            i = round(start/dt, 0)
            j = round((start + reflect)/dt, 0)
            k = round((start + 2*reflect)/dt, 0)
            power = voltage*current

            incident = simps(power[i:j], t[i:j])
            reflected = - simps(power[j:k], t[j:k])
            #absorbed = incident - reflected
            absorbed.append(incident - reflected)

            #print "Incident (J) =", incident
            #print "Reflected (J) =", reflected
            #print "Absorbed (J) =", absorbed

plt.plot(starts, absorbed)
plt.show()

#index = np.argmax(absorbed)
index = 25
print "Start (s) =", starts[index]
print "Absorbed (mJ) =", (absorbed[index] * 1e3)

plt.hold(True)
plt.plot(t, voltage)
plt.plot(t, current)
plt.vlines((starts[25], starts[25]+reflect, starts[25]+2*reflect), -15, 15)
plt.axis((starts[25], starts[25] + 2*reflect, -15, 15))
plt.show()
