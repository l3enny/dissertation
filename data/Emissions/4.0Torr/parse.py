from matplotlib import pyplot as plt
import os
import numpy as N

p = '4.0 Torr'

files = os.listdir('.')
fids = []
names = []
for s in files:
    if '.txt' in s and 'C2' not in s:
        fids.append(open(s, 'r'))
        names.append(s[2:5])      

plt.hold(True)
for fid in fids:
    data = N.loadtxt(fid, delimiter=',', skiprows=5)
    data[:, 1] = N.abs(data[:, 1])
    maximum = N.max(data[:, 1])
    #data[:, 1] = data[:, 1]/maximum
    plt.plot(1e6*data[:, 0], data[:, 1], linewidth=2)

plt.legend(names)
plt.axis([10.52, 10.66, 0, 4.0])
plt.xlabel('Time ($\mu$s)')
plt.ylabel('Normalized Intensity (a.u.)')
plt.title(p + ', Midstream')

plt.savefig('trends.pdf')

for fid in fids:
    fid.close()
