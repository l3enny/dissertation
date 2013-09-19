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


