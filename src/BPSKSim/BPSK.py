"""
Program to simulate BPSK communication system. 
    Unequal bit probabilities

    SNRs - range 0 to 10 dB

    Three cases: P = {0.5, 0.25, 0.1}        
"""

import numpy as np
import matplotlib.pyplot as plt


def BPSK(bits, P_0):
    """
    Simulate BPSK simulation system with unequal bit probabilities
    
    Args: 
        bits  (numpy arr): Binary data to be transmitted 
        P_0 (float): Probability of transmitting a bit '0' 
        
    Returns: 
    numpy array: The received data after passing BPSK system 
    """
    N = len(bits)

    # generate random numbers to determine the transmitted bitgs 
    rand_nums = np.random.rand(N)
    transmitted_bits = np.zeros(N)
    transmitted_bits[rand_nums >= P_0] = 1

    # simulate noise 
    noise = np.random.randn(N)
    # Pass through BPSK system 
    received_bits = transmitted_bits * 2 - 1 + noise

    # determine the received bits based on a threshold of 0 
    received_bits[received_bits > 0] = 1
    received_bits[received_bits <= 0] = 0

    return received_bits


def probability_of_bit_error(bits, received_bits):
    """
    Calculate the probability of bit error. 
    
    Args: 
        bits (numpy array): Original bin data 
        received_b its (numpy array): Bin data received after BPSK 

    Returns: 
        The prob. of bit error (float) 
        
    """

    N = len(bits)
    error_bits = np.sum(bits != received_bits)
    return error_bits / N


def simulation_of_SNRs(P_0):
    """
    Simulate BPSK communication for different SNR values and find error prob. 
    
    args: 
        P_0 (float): Prob. trans '0' 
    
    Returns: 
        SNR values  (numpy arr) 
        Prob. bit error (numpy arr) 
    """
    SNR_values = np.linspace(0, 10, 12)
    print(SNR_values)
    bit_error_prob = []
    for snr in SNR_values:
        bits = np.random.randint(0, 2, 10000)
        received_bits = BPSK(bits=bits, P_0=P_0)
        bit_error_prob.append(probability_of_bit_error(bits=bits, received_bits=received_bits))
    return SNR_values, bit_error_prob


if __name__ == "__main__":
    # plot 
    SNR_values, bit_error_prob = simulation_of_SNRs(0.5)
    plt.plot(SNR_values, bit_error_prob, label="P_0 = 0.5")

    SNR_values, bit_error_prob = simulation_of_SNRs(0.25)
    plt.plot(SNR_values, bit_error_prob, label="P_0 = 0.25")

    SNR_values, bit_error_prob = simulation_of_SNRs(0.1)
    plt.plot(SNR_values, bit_error_prob, label="P_0 = 0.1")
    plt.legend()
    plt.show()
