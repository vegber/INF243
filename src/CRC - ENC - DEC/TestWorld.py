import os


def crc_encode(data, g=0b10001100000000000):
    generator_bits = f'{g:b}'.zfill(17)
    generator_bits = [int(bit) for bit in generator_bits]
    crc_register = [0] * len(generator_bits)
    crc_register += [0] * (8 - (len(crc_register) % 8))
    for byte in data:
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
    crc = bytes([sum([bit << (7 - i) for i, bit in enumerate(crc_register)])])
    return data + crc


def crc_decode(m, g=0b10001100000000000):
    generator_bits = f'{g:b}'.zfill(17)
    generator_bits = [int(bit) for bit in generator_bits]
    crc_size = len(generator_bits) // 8
    m, crc_received = m[:-crc_size], m[-crc_size:]
    padded_message = m + b'\x00' * (len(generator_bits) - 1)
    crc_register = [0] * len(generator_bits)
    crc_register += [0] * (8 - (len(crc_register) % 8))
    for byte in padded_message:
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
    crc_calculated = bytes([sum([bit << (7 - i) for i, bit in enumerate(crc_register)])])
    if crc_received != crc_calculated:
        raise ValueError("Invalid CRC checksum")
    return m


def crc_encode_file(in_file, out_file, g):
    with open(in_file, "rb") as input_file, open(out_file, "wb") as output_file:
        while True:
            data = input_file.read(1024)
            if not data:
                break
            encoded_data = crc_encode(data, generator)
            output_file.write(encoded_data)


def crc_decode_file(in_file, out_file, g):
    with open(in_file, "rb") as input_file, open(out_file, "wb") as output_file:
        while True:
            data = input_file.read(1024)
            if not data:
                break
            decoded_data = crc_decode(data, g)
            output_file.write(decoded_data)


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
    generator = 0b1000000001100001
    crc_encode_file(filename, encoded_filename, generator)

    # Decode the file and compare with the original
    decoded_filename = "decoded_test_file.txt"
    crc_decode_file(encoded_filename, decoded_filename, generator)

    # Compare the decoded file with the original file
    with open(filename, "rb") as f1, open(decoded_filename, "rb") as f2:
        original_data = f1.read()
        decoded_data = f2.read()

        if original_data == decoded_data:
            print("Success: The original file and the decoded file are the same.")
        else:
            print("Error: The original file and the decoded file are different.")
