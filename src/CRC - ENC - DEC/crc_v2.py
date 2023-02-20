import os
import crcmod


def crc_encode(data, polynomial):
    crc_func = crcmod.mkCrcFun(polynomial)
    crc = crc_func(data)
    crc_bytes = crc.to_bytes(2, byteorder='big')
    return data + crc_bytes


def crc_decode(data, polynomial):
    data, crc_bytes = data[:-2], data[-2:]
    expected_crc = int.from_bytes(crc_bytes, byteorder='big')
    crc_func = crcmod.mkCrcFun(polynomial)
    actual_crc = crc_func(data)
    if actual_crc != expected_crc:
        raise ValueError('CRC check failed')
    return data


def run(p):
    filename = 'test_file.bin'
    filesize = 1024 * 1024  # 1 MB
    blocksize = 1024  # 1024 bytes per block
    with open(filename, 'wb') as f:
        for i in range(filesize // blocksize):
            block = os.urandom(blocksize)
            encoded_block = crc_encode(block, polynomial)
            f.write(encoded_block)
        f.close()

    # Read the file and decode it
    with open(filename, 'rb') as f:
        decoded_data = b''
        while True:
            block = f.read(blocksize + 2)
            if not block:
                break
            decoded_block = crc_decode(block, polynomial)
            decoded_data += decoded_block
        f.close()

    with open(filename, 'rb') as f:
        original_data = f.read()
        f.close()
    if decoded_data == original_data:
        return True
    return False


if __name__ == '__main__':
    # define the generator polynomial
    polynomial = 0x1021  # equivalent to binary 1000000001100001
    print(run(polynomial))
