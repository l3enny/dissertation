import numpy as np
from scipy.constants import *
from scipy.interpolate import interp1d

# System conditions
Tg = 300                # gas temperature, K
M = 4.002602 * atomic_mass # atomic mass, kg
fi = 8.0e-5             # impurity fraction
ne = 1e12 * 1e6         # approximate electron density

l = 11 * 2.54 * 1e-2                    # plasma length, m
r = 0.033/2                             # plasma radius, m
L2 = 1./((pi/l)**2 + (2.405/r)**2)      # diffusion length, m^2

pressures_torr = [0.3, 4.0, 16.0]
pressures = np.array(pressures_torr) * 133.322368

for P in pressures:
    N0 = P / (k * Tg)       # neutral gas density, m^-3
    Ng = (1. - fi) * N0     # helium gas density, m^-3
    Ni = fi * Ng            # impurity density, m^-3

    # Deloche, Monchicourt, Cheret, and Lambert (1976)
    def deloche(Nm):
        D0 = 410./((273./293)*atm) * 1e-4  # Diffusion, m^2/s
        d = 0.2                    # He* + 2He -> He_2^* + He, Torr^-2/s
        B11 = 1.5e-9 * 1e-6        # He* + He* -> He^+ + He + e, m^3/s
        g1 = 4.2e-9 * 1e-6         # He* + e -> He + e, m^3/s
        C = 7.0e-11 * 1e-6         # He* + A_2 -> He + A_2^+ + e
        diffusion = Nm * D0/L2
        three_body = d * P**2 * Nm
        penning = B11 * Nm**2
        impurity = C * Ni * Nm
        total = diffusion + three_body + penning + impurity
        return diffusion, three_body, penning, impurity, total

    def deloche2(Nm):
        DM1 = 410./((273./293)*atm) * 1e-4  # Diffusion, m^2/s
        d = 0.2                    # He* + 2He -> He_2^* + He, Torr^-2/s
        B11 = 1.5e-9 * 1e-6        # He* + He* -> He^+ + He + e, m^3/s
                                   #           -> He_2^+ + e, m^3/s (dominant)
        g1 = 4.2e-9 * 1e-6         # He* + e -> He + e, m^3/s
        z1 = 0
        C = 7.0e-11 * 1e-6         # He* + A_2 -> He + A_2^+ + e
        diffusion = Nm * DM1/L2
        ameta_ameta = B11 * Nm**2
        superelastic = g1 * M1 * ne * (T_e / T_g)**(z1)
        molecular_conversion = d * P**2 * Nm
        n2_penning = C * Ni * Nm
        total = diffusion + ameta_ameta + superelastic + molecular_conversion\
                + n2_penning
        return (diffusion, ameta_ameta, superelastic, molecular_conversion,
               n2_penning)


    Nm = np.logspace(13, 18)
    losses = deloche(Nm)
    np.savetxt(str(P) + '_diffusion.csv',losses[0], delimiter=',')
    np.savetxt(str(P) + '_three.csv',     losses[1], delimiter=',')
    np.savetxt(str(P) + '_penning.csv',   losses[2],  delimiter=',')
    np.savetxt(str(P) + '_impurity.csv',  losses[3],  delimiter=',')
    np.savetxt(str(P) + '_total.csv',     losses[4],  delimiter=',')
    np.savetxt(str(P) + '_nm.csv', Nm, delimiter=',')
