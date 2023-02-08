import random

import numpy as np
import matplotlib.pyplot as plt


def bpsk_simulation(snr_db, p0, N):
    snr = 10 ** (snr_db / 10)
    p1 = 1 - p0
    s = np.random.choice([-1, 1], size=N, p=[p0, p1])
    noise = np.sqrt(1 / (2 * snr)) * np.random.randn(N)
    r = s + noise
    decision = np.sign(r)
    error = (decision != s).mean()
    return error


def DrawPlot(p, error, snr_db_range):
    for l in range(len(error)):
        plt.plot(snr_db_range, error[l], label=f"{p[l]}")
    plt.xlabel("SNR (dB)")
    plt.ylabel("Probability of Bit Error")
    plt.axis([0, 10, 1e-6, 0.1])
    plt.yscale('log')
    plt.title("BPSK Simulation")
    plt.grid()
    plt.legend()
    plt.show()


def plot_probability_of_error(p, N=10000):
    snr_db_range = np.arange(0, 10)
    error = [[bpsk_simulation(snr, p0, N) for snr in snr_db_range] for p0 in p]
    DrawPlot(p, error, snr_db_range)


plot_probability_of_error([0.5, 0.25, 0.1])

# plot_probability_of_error(0.5)
# plot_probability_of_error(0.25)
# plot_probability_of_error(0.1)
