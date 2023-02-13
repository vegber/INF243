import random

from numpy import sqrt
import numpy as np
from numpy.random import rand, randn
import matplotlib.pyplot as plt
from scipy.special import erfc


def BPSK_SIM(p, N=500000):
    EbNodB_range = range(0, 11)
    itr = len(EbNodB_range)
    ber = [None] * itr

    for n in range(0, itr):
        EbNodB = EbNodB_range[n]
        EbNo = 10.0 ** (EbNodB / 10.0)
        x = 2 * (rand(N) >= p) - 1
        noise_std = 1 / sqrt(2 * EbNo)
        y = x + noise_std * randn(N)
        y_d = 2 * (y >= 0) - 1
        errors = (x != y_d).sum()
        ber[n] = 1.0 * errors / N

        print("EbNodB:", EbNodB)
        print("Error bits:", errors)
        print("Error probability:", ber[n])
    return EbNodB_range, ber


def q_function(x):
    return 0.5 * erfc(x / np.sqrt(2))


def bpsk_simulation(Eb):
    # Eb is the energy per bit
    Es = 2 * Eb
    # Calculate the noise power
    N0 = 1 / Es
    # Create a range of values for the signal-to-noise ratio (SNR)
    SNR = np.linspace(0, 10, num=1000)
    # Calculate the probability of error for each SNR value
    Pe = q_function(np.sqrt(Es / (2 * N0)) * np.power(10, SNR / 20))
    return Pe, SNR


def plot(P):
    colors = ["g", "b", "r", "y", 'c', 'm', 'k']
    i = 0
    for p in P:
        EbNodB_range, ber = BPSK_SIM(p)
        plt.plot(EbNodB_range, ber, 'bo--', alpha=0.4, color=colors[i], label=f"{p}")
        i += 1
    pe, snr = bpsk_simulation(1)
    plt.plot(snr, pe, 'r-', color="k", alpha=0.7, label="theoretical")
    plt.axis([0, 10, 1e-6, 0.1])
    #     plt.xscale('linear')
    plt.yscale('log')
    plt.xlabel('Eb/No(dB)')
    plt.ylabel('Probability of error')
    plt.legend()
    plt.grid(True)
    plt.title('BPSK Modulation')
    plt.show()


if __name__ == '__main__':
    plot([0.5, 0.25, 0.1])
