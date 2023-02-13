import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc


def hamming_decoder(received_word):
    # Function to decode the received word using Hamming code
    # Use the parity bits to detect and correct errors
    H_t = np.array([[1, 0, 1, 0, 1, 0, 1],
                    [0, 1, 1, 0, 0, 1, 1],
                    [0, 0, 0, 1, 1, 1, 1]])
    syndrome = np.mod(np.matmul(H_t, received_word), 2)
    error_pos = np.dot(syndrome, [1, 2, 4])
    if error_pos > 0:
        received_word[error_pos - 1] = 1 - received_word[error_pos - 1]
    decoded_word = received_word[2:]
    return decoded_word


def hamming_encoder(data):
    # Function to encode the data using Hamming code
    G = np.array([[1, 1, 0, 1],
                  [1, 0, 1, 1],
                  [1, 0, 0, 0],
                  [0, 1, 1, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]])
    encoded_word = np.matmul(data, G) % 2
    return encoded_word


def BSC(data, p):
    # Function to simulate a binary symmetric channel
    # Add random noise to the data with probability p
    noise = np.random.rand(len(data))
    noise = np.where(noise < p, 1, 0)
    received_word = np.mod(data + noise, 2)
    return received_word


def theoretical_error_prob(Eb_N0_dB):
    Eb_N0 = 10 ** (Eb_N0_dB / 10)
    Pb = 0.5 * erfc(np.sqrt(Eb_N0))
    return Pb


def simulate():
    # Sim parameters
    N = 10000  # number of bits to simulate
    p = 0.05  # channel crossover probability

    # BPSK and hamming code simulation
    Eb_N0_dB = np.linspace(0, 10, 100)
    Pb_hamming = np.zeros(len(Eb_N0_dB))
    Pb_bpsk = np.zeros(len(Eb_N0_dB))

    for i in range(len(Eb_N0_dB)):
        Eb_N0 = 10 ** (Eb_N0_dB[i] / 10)
        N0 = 1 / Eb_N0
        p = np.sqrt(2 * N0)
        error_count_hamming = 0
        error_count_bpsk = 0
        for j in range(N):
            # Generate a random bit
            data = np.random.randint(2, size=4)
            # encode data using hamming code
            encoded_word = hamming_encoder(data)
            # pass through  BSC
            received_word = BSC(encoded_word, p)
            # decode using hamming code
            decoded_word = hamming_decoder(received_word)
            # check for errors
            error_count_hamming += np.sum(np.abs(data - decoded_word))
            # pass data through the BSC for uncoded BPSK
            received_data = BSC(data, p)
            # check for errors in received data
            error_count_bpsk += np.sum(np.abs(data - received_data))
        Pb_hamming[i] = error_count_hamming / (4 * N)
        Pb_bpsk[i] = error_count_bpsk / N

    # Plot the error probability
    plt.semilogy(Eb_N0_dB, Pb_hamming, 'b', label='Hamming code')
    plt.semilogy(Eb_N0_dB, Pb_bpsk, 'r', label='BPSK')
    plt.semilogy(Eb_N0_dB, theoretical_error_prob(Eb_N0_dB), 'g', label='Theoretical')
    plt.xlabel('Eb/N0 (dB)')
    plt.ylabel('Probability of bit error')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Coding gain calculation
    Eb_N0_target = 10 ** (-5)
    index = np.argmin(np.abs(Pb_bpsk - Eb_N0_target))
    coding_gain = Eb_N0_dB[index] - Eb_N0_dB[np.argmin(np.abs(Pb_hamming - Eb_N0_target))]
    print('Coding gain at Pb = 10^(-5):', coding_gain, 'dB')


if __name__ == '__main__':
    simulate()
