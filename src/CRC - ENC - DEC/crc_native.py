import os
def crc_encode(message, generator):
    """
    Calculates the CRC checksum for a message using the given generator polynomial.

    Args:
        message (bytes): The message to encode.
        generator (int): The generator polynomial, represented as a binary integer.

    Returns:
        bytes: The encoded message with the CRC checksum appended.
    """
    # Convert the generator polynomial to a bit array
    generator_bits = f'{generator:b}'.zfill(17)
    generator_bits = [int(bit) for bit in generator_bits]

    # Pad the message with zeros to make room for the CRC checksum
    padded_message = message + b'\x00' * (len(generator_bits) - 1)

    # Initialize the CRC register to all zeros
    crc_register = [0] * len(generator_bits)

    # Calculate the CRC checksum
    for byte in padded_message:
        # XOR the most significant bit of the byte with the most significant bit of the CRC register
        msb = 1 << 7
        for i in range(8):
            if byte & msb:
                crc_register[0] ^= generator_bits[0]
                for j in range(1, len(generator_bits)):
                    crc_register[j] ^= generator_bits[j] if crc_register[j - 1] else 0
            else:
                for j in range(len(generator_bits) - 1):
                    crc_register[j] = crc_register[j + 1]
                crc_register[-1] = 0
            msb >>= 1

    # Convert the CRC register to a byte array and append it to the message
    crc_bytes = bytes([sum([bit << (7 - i) for i, bit in enumerate(crc_register)])])
    return message + crc_bytes


def crc_decode(message, generator):
    """
    Decodes a message with an appended CRC checksum using the given generator polynomial.

    Args:
        message (bytes): The message to decode.
        generator (int): The generator polynomial, represented as a binary integer.

    Returns:
        bytes: The decoded message, with the CRC checksum removed.

    Raises:
        ValueError: If the CRC checksum is invalid.
    """
    # Convert the generator polynomial to a bit array
    generator_bits = f'{generator:b}'.zfill(17)
    generator_bits = [int(bit) for bit in generator_bits]

    # Split the message into the message and the CRC checksum
    crc_size = len(generator_bits) // 8
    message, crc_received = message[:-crc_size], message[-crc_size:]

    # Pad the message with zeros to make room for the CRC checksum
    padded_message = message + b'\x00' * (len(generator_bits) - 1)

    # Initialize the CRC register to all zeros
    crc_register = [0] * len(generator_bits)

    # Calculate the CRC checksum
    for byte in padded_message:
        # XOR the most significant bit of the byte with the most significant bit of the CRC register
        msb = 1 << 7
        for i in range(8):
            if byte & msb:
                crc_register[0] ^= generator_bits[0]
                for j in range(1, len(generator_bits)):
                    crc_register[j] ^= generator_bits[j] if crc_register[j - 1] else 0
            else:
                for j in range(len(generator_bits) - 1):
                    crc_register[j] = crc_register[j + 1]
                crc_register[-1] = 0
            msb >>= 1

    # Check if the calculated CRC checksum matches the received CRC checksum
    crc_calculated = bytes([sum([bit << (7 - i) for i, bit in enumerate(crc_register)])])
    if crc_received != crc_calculated:
        raise ValueError("Invalid CRC checksum")

    # Return the decoded message
    return message


if __name__ == '__main__':
    # Generate a random file of size 1 MB with message block length of 1024 bytes
    filename = "test_file.txt"
    message_block_size = 1024
    num_blocks = 1024
    total_size = num_blocks * message_block_size
    with open(filename, "wb") as f:
        for i in range(num_blocks):
            message = os.urandom(message_block_size)
            f.write(message)

    # Encode the file
    encoded_filename = "encoded_test_file.txt"
    generator = 0b10001100000100001
#    crc_encode_file(filename, encoded_filename, generator)

    # Decode the file and compare with the original
    decoded_filename = "decoded_test_file.txt"
#    crc_decode_file(encoded_filename, decoded_filename, generator)

    # Compare the decoded file with the original file
    with open(filename, "rb") as f1, open(decoded_filename, "rb") as f2:
        original_data = f1.read()
        decoded_data = f2.read()

    if original_data == decoded_data:
        print("Success: The original file and the decoded file are the same.")
    else:
        print("Error: The original file and the decoded file are different.")
