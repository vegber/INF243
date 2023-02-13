import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc


def hamming_decode(r):
    # Implement the hamming decoder
    H = np.array([[1, 0, 1, 0, 1, 0, 1],
                  [0, 1, 1, 0, 0, 1, 1],
                  [0, 0, 0, 1, 1, 1, 1]])
    s = np.mod(np.matmul(H, r), 2)
    if np.all(s == np.array([0, 0, 0])):
        return r[3:7]
    else:
        for i in range(7):
            if np.all(s == H[:, i]):
                r[i] = (r[i] + 1) % 2
                return r[3:7]


def bsc(x, p):
    # Implement the binary symmetric channel
    n = np.random.rand(x.shape[0])
    y = np.mod(x + (n < p), 2)
    return y


def simulate_hamming(p, N):
    # Simulate the hamming code over a BSC channel
    errors = 0
    for i in range(N):
        # Generate random data
        data = np.random.randint(2, size=4)

        # Encode the data
        G = np.array([[1, 0, 0, 0, 1, 1, 1],
                      [0, 1, 0, 0, 1, 1, 0],
                      [0, 0, 1, 0, 1, 0, 1],
                      [0, 0, 0, 1, 0, 1, 1]])
        encoded = np.matmul(G, data) % 2

        # Pass the encoded data through the BSC channel
        received = bsc(encoded, p)

        # Decode the received data
        decoded = hamming_decode(received)

        # Count the number of errors
        errors += np.sum(np.abs(decoded - data))

    # Calculate the probability of error
    P_b = errors / (N * 4)
    return P_b


def theoretical_probability_error(EbN0_dB):
    # Calculate the theoretical probability of error for uncoded BPSK transmission
    EbN0 = 10 ** (EbN0_dB / 10)
    P_b = 0.5 * erfc(np.sqrt(EbN0 / 2))
    return P_b


# Define the range of E_b/N_0 values
EbN0_dB = np.linspace(0, 10, 100)
EbN0 = 10 ** (EbN0_dB / 10)

# Calculate the channel crossover probability for each E_b/N_0 value
# p =
