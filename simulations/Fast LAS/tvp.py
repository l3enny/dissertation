import numpy as np

pressures = ["0.3Torr.csv", "0.5Torr.csv", "1.0Torr.csv", "2.0Torr.csv",
             "3.0Torr.csv", "4.0Torr.csv", "8.0Torr.csv", "16.0Torr.csv"]
locations = ["Downstream", "Midstream", "Upstream"]

energy = [3.38234, 5.2649, 5.4439, 4.6755, 3.9185, 3.4581, 2.6626, 2.2320]

averages = []
for p in pressures:
    temperatures = []
    for l in locations:
        data = np.loadtxt('/'.join((l, p)), delimiter=',', skiprows=1)
        temperatures.append(np.average(data[-500:-1, 0]))
    averages.append(np.average(temperatures))

with open("averages.csv", mode="wb") as f:
    f.write("Temperatures,+-\n")
    for a in averages:
        f.write(str(a) + ",10\n")
