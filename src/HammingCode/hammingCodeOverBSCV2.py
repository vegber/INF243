import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc


def hamming_encoder(data):
    """Encoding the data bits using (7, 4) Hamming code"""
    G = np.array([[1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 0, 0], [0, 1, 1, 1], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    return np.matmul(G, data) % 2


def hamming_decoder(code):
    """Decoding data using (7, 4) Hamming code"""
    n = 7
    k = 4
    data = np.zeros(k)
    data[0] = code[0] ^ code[2] ^ code[5] ^ code[6]
    data[1] = code[1] ^ code[2] ^ code[5] ^ code[6]
    data[2] = code[3] ^ code[5] ^ code[2] ^ code[6]
    data[3] = code[4] ^ code[5] ^ code[2] ^ code[6]
    return data


def bsc_channel(code, p):
    """Transmitting data over BSC channel"""
    n = 7
    k = 4
    for i in range(n):
        if np.random.rand() < p:
            code[i] = 1 - code[i]
    return code


def bpsk_modulation(data):
    """Modulating data using BPSK"""
    modulated_data = 2 * data - 1
    return modulated_data


def bpsk_demodulation(modulated_data, received_signal):
    """Demodulating data using BPSK"""
#    received_signal = np.array(received_signal, dtype=int)
    # print(len(received_signal))
    data = np.zeros(len(modulated_data))
    for i in range(len(modulated_data)):
        if (received_signal * modulated_data[i]) > 0:
            data[i] = 0
        else:
            data[i] = 1
    return data


def bpsk_error_probability(ebno_db):
    """Calculating the theoretical error probability of uncoded BPSK transmission"""
    ebno = 10 ** (ebno_db / 10)
    p = 0.5 * erfc(np.sqrt(ebno))
    return p


def hamming_error_probability(ebno_db, p):
    """Calculating the error probability of (7, 4) Hamming code over BSC"""
    n = 7
    k = 4
    num_bits = 10000
    num_errors = 0
    ebno = 10 ** (ebno_db / 10)
    noise_variance = 1 / (2 * ebno)
    noise_standard_deviation = np.sqrt(noise_variance)
    for i in range(num_bits):
        data = np.random.randint(0, 2, k)
        code = hamming_encoder(data)
        modulated_code = bpsk_modulation(code)
        noise = noise_standard_deviation * np.random.randn(n)
        received_signal = modulated_code + noise
        # received_signal = modulated_code + noise_standard_deviation * np.random.randn(len(noise_standard_deviation))
        demodulated_code = bpsk_demodulation(received_signal, p)
        code_after_bsc = bsc_channel(modulated_code, p)
        decoded_data = hamming_decoder(code_after_bsc)
        num_errors += np.sum(data != decoded_data)
    return num_errors / num_bits


def theoretical_error_probability(ebno_db):
    """Calculating the theoretical error probability of BPSK over AWGN channel"""
    ebno = 10 ** (ebno_db / 10)
    return 0.5 * (1 - np.sqrt(ebno / (1 + ebno)))


def plot_error_probability(hamming_error_probs, theoretical_error_probs, ebno_db):
    """Plotting the error probability of (7, 4) Hamming code and BPSK over BSC"""
    plt.semilogy(ebno_db, hamming_error_probs, label='Hamming (7, 4)')
    plt.semilogy(ebno_db, theoretical_error_probs, label='BPSK')
    plt.xlabel('Eb/No (dB)')
    plt.ylabel('Bit Error Rate (BER)')
    plt.title('Error Probability of (7, 4) Hamming code and BPSK over BSC')
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == '__main__':
    ebno_db = np.linspace(0, 15, 16)
    p = 0.1
    hamming_error_probs = [hamming_error_probability(ebno, p) for ebno in ebno_db]
    theoretical_error_probs = [theoretical_error_probability(ebno) for ebno in ebno_db]
    plot_error_probability(hamming_error_probs, theoretical_error_probs, ebno_db)
