import numpy as np
import matplotlib.pyplot as plt
import datetime

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

resolution = 1e3
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
header = "Energy (eV),Cross Section (m^2)\r\n"
date = datetime.datetime.now()
with open(fn, mode="wb") as f:
    f.write(header)
    formatted = np.array((energies, elastic)).T
    np.savetxt(f, formatted, delimiter=",")

fn = "excitation.dat"
with open(fn, mode="wb") as f:
    f.write(header)
    formatted = np.array((energies, excitation)).T
    np.savetxt(f, formatted, delimiter=",")

fn = "ionization.dat"
with open(fn, mode="wb") as f:
    f.write(header)
    formatted = np.array((energies, ionization)).T
    np.savetxt(f, formatted, delimiter=",")

filename = "bolsig_conv.txt"
with open(filename, mode="wb") as f:
    f.write("These are the cross sections for helium that are used in\r\n"
            "XPDP1 as developed by Verboncoeur et al. The formatting of\r\n"
            "this file will hopefully work.\r\n\r\n")
    f.write("----------------------------------------\r\n\r\n")
    f.write("COMMENT\r\nHe\r\n")
    f.write("References:\r\n")
    f.write("1) Verboncoeur et al., J. Comp. Physics, 104, pp. 321-328 (1993).\r\n")
    f.write("http://ptsg.egr.msu.edu/pub/codes/xpdp1/\r\n")
    f.write("-----------------------------------------"
            "-----------------------------------------\r\n\r\n")

    f.write("ELASTIC\r\nHe\r\n1.3693e-4\r\n")
    f.write("COMMENT: elastic scattering, from XPDP1\r\n")
    f.write("UPDATED: %s\r\n" % date)
    f.write("-----------------------------------------\r\n")
    for i in range(len(energies)):
        f.write(" %e\t%e\r\n" % (energies[i], elastic[i]))
    f.write("-----------------------------------------\r\n\r\n")

    f.write("EXCITATION\r\nHe -> He*\r\n19.8\r\n")
    f.write("COMMENT: excitation, from XPDP1\r\n")
    f.write("UPDATED: %s\r\n" % date)
    f.write("-----------------------------------------\r\n")
    for i in range(len(energies)):
        if excitation[i] == 0.0:
            continue
        f.write(" %e\t%e\r\n" % (energies[i], excitation[i]))
    f.write("-----------------------------------------\r\n\r\n")

    f.write("IONIZATION\r\nHe -> He^+\r\n24.5\r\n")
    f.write("COMMENT: ionization, from XPDP1\r\n")
    f.write("UPDATED: %s\r\n" % date)
    f.write("-----------------------------------------\r\n")
    for i in range(len(energies)):
        if ionization[i] == 0.0:
            continue
        f.write(" %e\t%e\r\n" % (energies[i], ionization[i]))
    f.write("-----------------------------------------\r\n\r\n\r\n\r\n")
    f.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\r\n")
    f.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\r\n")
    f.write("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\r\n")
