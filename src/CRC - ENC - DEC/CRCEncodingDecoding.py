"""
step (1)

    Write CRC encoding and CRC decoder with the generator polynomial
        g(x) = x^16 + x^10 + x^8 + x^7 + x^3 + 1

step (2)
    Generate a random file of size 1 MB with message block length of 1024 bytes. Use
    the file to test your program. I.e Encode then decode the file. Compare the
        decoded file with the original

step (3)
    Test your program further by passing the encoded dat through a binary symmetric
    channel with crossover probabilities of
        0.00001
        0.001
        0.1

    (i)
        Are there ny blocks of data that have errors that are not detected ?
"""
import binascii
import re

def fnInBin(s):
    return set(s).issubset({'0'}) and bool(s)


def xor(a: str, b: str):
    assert len(a) == len(b)
    return ''.join([str(int(a) ^ int(b)) for a, b in zip(a, b)])


def findWindow(bit_stream):
    _ = re.search('1', bit_stream)
    if _ is not None:
        return _.start()
    else:
        return -1

class CRC:
    def __init__(self, divisor: str):
        self.polynomial_bitstream = bin(int(divisor, 2))[2:]

    def Encode(self, data_bitstream: str, crc_bits: int):
        """
        Encode bitstream with crc check trail
        Args:
            data_bitstream: string binary i.e('010') bin(str) Assume clean
            crc_bits: nbr of check bits


        Returns: Encoded data with CRC on right end: tail encoding
        """
        binary_data = data_bitstream.lstrip("0")  # remove any head zero bits
        padding_bits = '0'*crc_bits  # get length of bit stream
        bit_stream = binary_data + padding_bits

        op = len(self.polynomial_bitstream)
        while not fnInBin(bit_stream[:len(bit_stream)-op]):
            t = findWindow(bit_stream)
            rep = xor(bit_stream[t:t+len(self.polynomial_bitstream)],  self.polynomial_bitstream)
            bit_stream = bit_stream[:t] + rep + bit_stream[t + len(rep):]
