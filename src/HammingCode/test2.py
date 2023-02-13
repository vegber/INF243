import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


def hamming_code_encoder(message):
    # Encoding the message using (7, 4) Hamming code
    encoded = np.zeros(7)
    encoded[::-1][:4] = message
    encoded[2] = message[0] ^ message[1] ^ message[2]
    encoded[4] = message[0] ^ message[1] ^ message[3]
    encoded[5] = message[0] ^ message[2] ^ message[3]
    encoded[6] = message[1] ^ message[2] ^ message[3]
    return encoded


def hamming_code_decoder(y, p):
    n = 7
    r = 3
    H = np.array([[1, 0, 1, 0, 1, 0, 1],
                  [0, 1, 1, 0, 0, 1, 1],
                  [0, 0, 0, 1, 1, 1, 1]])

    for i in range(r):
        syndrome = np.dot(y, H[i]) % 2
        if syndrome != 0:
            position = np.dot(syndrome, 2 ** np.arange(r - 1, -1, -1))
            if np.random.rand() < p:
                y[position - 1] = (y[position - 1] + 1) % 2
    return y[:4]


def hamming_code_over_bsc(p, N):
    # Simulating the performance of (7, 4) Hamming code over BSC
    errors = 0
    for i in range(N):
        message = np.random.randint(2, size=4)
        encoded = hamming_code_encoder(message)
        received = encoded.copy()
        for j in range(7):
            if np.random.rand() < p:
                received[j] = not received[j]
        decoded = hamming_code_decoder(received, p)
        errors += np.sum(message != decoded)
    return errors / N


# Plotting the probability of error as a function of E_b/N_0 in dB
E_b_N_0_dB = np.arange(0, 6, 0.1)
E_b_N_0 = 10 ** (E_b_N_0_dB / 10)
p = norm.ppf(np.sqrt(2 * E_b_N_0)) / np.sqrt(7)
pe = np.zeros(len(E_b_N_0))
N = 10 ** 5
for i in range(len(E_b_N_0)):
    pe[i] = hamming_code_over_bsc(p[i], N)
plt.semilogy(E_b_N_0_dB, pe, '-o')
plt.xlabel('E_b/N_0 (dB)')
plt.ylabel('Probability of Error')
plt.grid()
plt.show()


Tell me how a program that will simulate performance of the
(7,4) Hamming code over a BSC channel with channel
crossover probability p = Q (sqrt(2E_b/N_0)) and plot the probability
of error as a function of Eb/NO in dB would work? On the same
plot, plot the theoretical probability of error for uncoded
BPSK transmission. Identify what the coding gain is for a
probability of error Pb = 10^-5