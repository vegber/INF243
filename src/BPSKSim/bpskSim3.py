import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc


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


Pe, SNR = bpsk_simulation(1)

plt.plot(SNR, Pe)
plt.xlabel('SNR (dB)')
plt.ylabel('Pe')
plt.title('Theoretical BPSK Simulation')
plt.grid(True)
plt.show()
