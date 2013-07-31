from math import log10, e

t0 = 1e-3

pressures = [0.3, 0.5, 1.0, 2.0, 3.0, 4.0, 8.0, 16.0]
a = [-0.0371094, 0.035908, 0.219525, 0.360608, 0.406222, 0.491887, 0.388248,
        0.138826]
b = [-1834.96, -1509.63, -1587.15, -1945.29, -2810.66, -3789.48, -9538.0,
        -15463.1]

Nm = []
for i in range(len(pressures)):
    p = pressures[i]
    Nm.append(1e16 * 10**(a[i] + b[i] * t0))
    print "Pressure =", p
    print "Decay constant = %e" % (-(b[i] / log10(e)))
    print "Pre-pulse =", Nm[-1], "\n"
