import math
import random
import numpy as np
import matplotlib.pyplot as plt


def BPSK_Sim(p):
    ### Constants ###
    N = 10000
    dB = 10.0
    EbN0dB_range = range(0, 11)
    ber = [None] * len(EbN0dB_range)

    for n in range(len(EbN0dB_range)):
        EbN0dB = EbN0dB_range[n]
        EbN0 = pow(dB, (EbN0dB / dB))

        x = 2 * (np.random.rand(N) >= p) - 1

        noise_std = 1 / math.sqrt(2 * EbN0)

        # div = np.random.randint(N, size=N)
        # y = [x + (random.gauss(0, noise_std) * y) for y in div]
        # y = x + (random.gauss(0, noise_std) * np.random.rand(N))
        errors = 0
        for m in range(0, N):
            tx_symbol = 2 * random.randint(0, 1) - 1
            noise = random.gauss(0, noise_std)
            rx = tx_symbol + noise
            det_ = 2 * (rx >= 0) - 1

            # y_d = np.array(2 * (y >= 0) - 1)
            errors = np.sum(x != det_)

        ber[n] = 1.0 * errors / N

        print(f"EbN0dB: {EbN0dB}")
        print(f"Error bits: {errors}")
        print(f"Error prob: {ber[n]}")

    return EbN0dB_range, ber


def secondTry(p=0.5):
    N = 100000
    snrindB_range = range(0, 10)
    itr = len(snrindB_range)
    ber = [None] * itr
    ber1 = [None] * itr
    tx_symbol = 0
    noise = 0
    ch_coeff = 0
    rx_symbol = 0
    det_symbol = 0
    for n in range(0, itr):

        snrindB = snrindB_range[n]
        snr = 10.0 ** (snrindB / 10.0)
        noise_std = 1 / math.sqrt(2 * snr)
        noise_mean = 0

        no_errors = 0
        for m in range(0, N):
            tx_symbol = 2 * random.randint(0, 1) - 1
            noise = random.gauss(noise_mean, noise_std)
            rx_symbol = tx_symbol + noise
            det_symbol = 2 * (rx_symbol >= 0) - 1
            no_errors += 1 * (tx_symbol != det_symbol)

        ber[n] = no_errors / N
        print("SNR in dB:", snrindB)
        print("Numbder of errors:", no_errors)
        print("Error probability:", ber[n])
    plt.plot(snrindB_range, ber, 'o-', label='practical')
    plt.axis([0, 10, 0, 0.1])
    plt.xlabel('snr(dB)')
    plt.ylabel('BER')
    plt.grid(True)
    plt.title('BPSK Modulation')
    plt.legend()
    plt.show()


def runFirst():
    snrIndBRangek, ber = BPSK_Sim(0.3)
    plt.plot(snrIndBRangek, ber, 'o-', label='practical')
    plt.axis([0, 10, 0, 0.1])
    plt.xlabel('snr(dB)')
    plt.ylabel('BER')
    plt.grid(True)
    plt.title('BPSK Modulation (Sim.)')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    secondTry()
    secondTry(0.25)
    secondTry(0.1)