"""
Cyclic Redundancy Check (CRC)

- Error detection
- Detect single, burst error

Data word: k bits
Codeword(n) = Data_word + Redundant bits
            n = k + r
"""

import random
import os
import binascii


def generate_random_bits():
    bits = ''.join(str(random.randint(0, 1)) for _ in range(1024))
    data = int(bits, 2).to_bytes(128, byteorder="big")

    # write to file
    with open("random_bits.bin", 'wb') as f:
        f.write(data)


def file_exists(filename) -> bool:
    # Get the list of files in the current directory
    files = os.listdir()

    # check if the file exists in the directory
    if filename in files:
        return True
    return False


def crc_encode(data, divisor):
    # Convert data to binary string
    binary_data = bin(int.from_bytes(data, byteorder='big'))[2:]

    # Pad binary data with zeros
    binary_data += '0' * (len(str(divisor)) - 1)

    # Convert divisor to binary string
    binary_divisor = bin(divisor)[2:]

    # Perform CRC division
    crc = bin(int(binary_data[:len(binary_divisor)], 2) ^ divisor)[2:]
    for bit in binary_data[len(binary_divisor):]:
        crc += bit
        if crc[0] == '1':
            crc = bin(int(crc[1:], 2) ^ divisor)[2:]
        else:
            crc = crc[1:]

    # Convert CRC to bytes
    crc_bytes = binascii.unhexlify(hex(int(crc, 2))[2:].zfill(len(crc) // 4))

    # Return encoded data with CRC appended
    return data + crc_bytes


def crc_decode(data, divisor):
    # Split data into message and CRC
    message = data[:-len(str(divisor))]
    crc = data[-len(str(divisor)):]

    # Compute CRC for message
    computed_crc = binascii.crc_hqx(message, 0xFFFF)

    # Check if computed CRC matches received CRC
    if computed_crc == int.from_bytes(crc, byteorder='big'):
        return message
    else:
        raise ValueError('CRC check failed')


if __name__ == '__main__':
    # if no file present, generate file:
    if not file_exists('random_bits.bin'): generate_random_bits()
    data = open('random_bits.bin')
    """
    g(x) = x ^ 16 + x ^ 10 + x ^ 8 + x ^ 7 + x ^ 3 + 1
    = 1 * x ^ 16 + 0 * x ^ 15 + 0 * x ^ 14 + 0 * x ^ 13 + 0 * x ^ 12 + 0 * x ^ 11 + 1 * x ^ 10 + 0 * x ^ 9
    + 1 * x ^ 8 + 1 * x ^ 7 + 0 * x ^ 6 + 0 * x ^ 5 + 0 * x ^ 4 + 1 * x ^ 3 + 0 * x ^ 2 + 0 * x ^ 1 + 1 * x ^ 0
    """
    g = int('1000000001100001', 16)
    # ggg = int('1000000001100001', 2).to_bytes(128, byteorder="big")
    divisor = 0x11021  # hex(int(0b10001000000100001))
    var = 0x1021
    with open('random_bits.bin', 'rb') as f:

        data_ = f.read()
        f.close()

    coded = crc_encode(data_, divisor=divisor)
    decoded = crc_decode(coded, divisor=divisor)