import random

from numpy import sqrt
from numpy.random import rand, randn
import matplotlib.pyplot as plt


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


def plot(P):
    colors = ["g", "b", "r", "y", 'c', 'm', 'k']
    i = 0
    for p in P:
        EbNodB_range, ber = BPSK_SIM(p)
        plt.plot(EbNodB_range, ber, 'bo--', color=colors[i], label=f"{p}")
        i += 1
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
