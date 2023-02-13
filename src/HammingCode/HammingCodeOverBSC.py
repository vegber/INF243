import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfinv


def hamming_decoder(received_codeword):
    H_t = np.array([[1, 0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1]])
    syndrome = np.dot(H_t, received_codeword) % 2

    if np.count_nonzero(syndrome) == 0:
        return received_codeword[:4]
    else:
        for i, error_vec in enumerate([[1, 0, 0, 0, 0, 0, 0],
                                       [0, 1, 0, 0, 0, 0, 0],
                                       [0, 0, 1, 0, 0, 0, 0],
                                       [0, 0, 0, 1, 0, 0, 0],
                                       [0, 0, 0, 0, 1, 0, 0],
                                       [0, 0, 0, 0, 0, 1, 0],
                                       [0, 0, 0, 0, 0, 0, 1]]):
            if (np.dot(H_t, error_vec) % 2 == syndrome).all():
                corrected_codeword = (received_codeword + error_vec) % 2
                return corrected_codeword[:4]


def simulate_hamming(p, N):
    error_count = 0
    for i in range(N):
        data = np.random.randint(2, size=4)
        codeword = np.zeros(7, dtype=int)
        G = np.arange([[1, 1, 0, 1],
                       [1, 0, 1, 1],
                       [1, 0, 0, 0],
                       [0, 1, 1, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
        codeword[:4] = data
        codeword[4:] = np.dot(codeword[:4], G) % 2
        received_codeword = (codeword + (np.random.rand(7) < p)).astype(int)
        decoded_data = hamming_decoder(received_codeword)
        if not (decoded_data == data).all():
            error_count += 1
    return error_count / N


def theoretical_prob_of_error(p, N):
    return (1 - (1 - 2 * p) ** (N / 2)) / 2


if __name__ == '__main__':
    N = 10000
    EbN0_dB = np.arange(0, 11, 0.1)
    EbN0 = 10 ** (EbN0_dB / 10)
    Eb = 1
    N0 = Eb / EbN0
    Q = erfinv(N0)
