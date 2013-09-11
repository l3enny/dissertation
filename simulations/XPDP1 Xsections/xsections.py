import numpy as np
import matplotlib.pyplot as plt

extengy0 = 19.8
ionenergy0 = 24.5

def hsigma1(energies):
    """
    e + He -> e + He, elastic scattering
    """
    output = np.zeros(len(energies))
    for i in range(len(energies)):
        output[i] = (8.5e-19 / (energies[i] + 10.0)**1.1)
    return output

def hsigma2(energies):
    """
    e + He -> e + He^*, electron excitation
    """
    output = np.zeros(len(energies))
    for i in range(len(energies)):
        if energies[i] < extengy0:
            output[i] = 0.0
        elif extengy0 <= energies[i] and energies[i] < 27.0:
            output[i] = 2.08e-22 * (energies[i] - extengy0)
        else:
            output[i] = 3.4e-19 / (energies[i] + 200)
    return output

def hsigma3(energies):
    """
    e + He -> e + He^+, electron ionization
    """
    output = np.zeros(len(energies))
    for i in range(len(energies)):
        if energies[i] < ionenergy0:
            output[i] = 0.0
        else:
            output[i] = 1e-17 * (energies[i] - ionenergy0) \
                      / ((energies[i] + 50) * (energies[i] + 300)**1.2)
    return output

resolution = 1e2
energies = np.logspace(-3, 3, num=resolution)

elastic = np.zeros(resolution)
elastic = hsigma1(energies)
excitation = np.zeros(resolution)
excitation = hsigma2(energies)
ionization = np.zeros(resolution)
ionization = hsigma3(energies)
momentum = np.zeros(resolution)
momentum = elastic + excitation + ionization

fn = "elastic.dat"
with open(fn, mode="wb") as f:
    f.write("Energy (eV),Cross Section (m^2)\n")
    formatted = np.array((energies, elastic)).T
    np.savetxt(fn, formatted, delimiter=",")

fn = "excitation.dat"
with open(fn, mode="wb") as f:
    f.write("Energy (eV),Cross Section (m^2)\n")
    formatted = np.array((energies, excitation)).T
    np.savetxt(fn, formatted, delimiter=",")

fn = "ionization.dat"
with open(fn, mode="wb") as f:
    f.write("Energy (eV),Cross Section (m^2)\n")
    formatted = np.array((energies, ionization)).T
    np.savetxt(fn, formatted, delimiter=",")

filename = "bolsig_conv.txt"
with open(filename, mode="wb") as f:
    f.write("ELASTIC\nHe\n0.00013693 / mass ratio\n")
    f.write("COMMENT: elastic scattering, from XPDP1\n")
    f.write("----------------------------------------\n")
    for i in range(len(energies)):
        f.write(" %e\t%e\n" % (energies[i], elastic[i]))
    f.write("\n")

    f.write("EXCITATION\nHe -> He*(19.8eV)\n19.8\n")
    f.write("COMMENT: excitation, from XPDP1\n")
    f.write("----------------------------------------\n")
    for i in range(len(energies)):
        f.write(" %e\t%e\n" % (energies[i], excitation[i]))
    f.write("\n")

    f.write("IONIZATION\nHe -> He^+\n24.5\n")
    f.write("COMMENT: ionization, from XPDP1\n")
    f.write("----------------------------------------\n")
    for i in range(len(energies)):
        f.write(" %e\t%e\n" % (energies[i], ionization[i]))
