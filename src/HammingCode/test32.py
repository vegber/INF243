import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


def hamming_code_encoder(data):
    """Encoding the data bits using (7, 4) Hamming code"""
    G = np.array([[1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 0, 0], [0, 1, 1, 1], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    return np.matmul(G, data) % 2


def hamming_code_decoder(c, p):
    r = np.zeros(7, dtype=int)
    for i in range(7):
        if np.random.rand() < p:
            r[i] = (c[i] + 1) % 2
    else:
        r = c
    h = np.array([[1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 0, 0], [0, 1, 1, 1], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    s = np.dot(h, r.reshape(7, 1)) % 2
    e = np.zeros(4, dtype=int)
    for i in range(4):
        e[i] = s[i, 0]
    x = (e + r[3:7]) % 2
    return x


def hamming_code_over_bsc(p, N):
    n = 7
    m = np.random.randint(2, size=(N, 4))
    c = np.zeros((N, n), dtype=int)
    for i in range(N):
        c[i, :] = hamming_code_encoder(m[i, :])
    y = np.zeros((N, n), dtype=int)
    for i in range(N):
        for j in range(n):
            if np.random.rand() < p:
                y[i, j] = (c[i, j] + 1) % 2
    decoded = np.zeros((N, 4), dtype=int)
    for i in range(N):
        decoded[i, :] = hamming_code_decoder(y[i, :], p)
    error = np.sum(decoded != m)
    return error / (4.0 * N)


def main():
    EbN0_dB = np.linspace(0, 10, 20)
    EbN0 = 10 ** (EbN0_dB / 10)
    p = norm.sf(np.sqrt(2 * EbN0))
    pe = np.zeros(len(EbN0))
    N = 1000
    for i in range(len(EbN0)):
        pe[i] = hamming_code_over_bsc(p[i], N)
    plt.plot(EbN0_dB, pe, 'o-')
    plt.xlabel('Eb/N0 (dB)')
    plt.ylabel('Probability of Error')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
