import CRCEncodingDecoding as CRC_En_Dec
import random
import os


# Function to create the
# random binary string
def rand_key(p):
    # Variable to store the
    # string
    key1 = ""
    # Loop to find the string
    # of desired length
    for i in range(p):
        # randint function to generate
        # 0, 1 randomly and converting
        # the result into str
        temp = str(random.randint(0, 1))
        # Concatenation the random 0, 1
        # to the final result
        key1 += temp
    return key1


def Encoding():
    global f
    # do crc encoding
    with open("original_bits.txt", "r+") as f:
        file = f.read()
        it = 0
        with open("encoded_bits.txt", "w+") as ff:
            # go through file in 1024 bit "blocks"
            for chunk in range(1024, len(file), 1024):
                block_message = file[it: chunk]  # one block
                it += 1024  # increment counter

                # encoding
                _, crc_sum = crc_obj.Encode(block_message, 16)
                ff.write(block_message + crc_sum)  # it is redundant I think to store both the zeros and crc sum...
            ff.close()
        f.close()


def Decoding():
    """
    Simulated the client/receiver side of transmission
    Should receive message + crc sum for each 1024 bit block code
    Returns: pass
    """

    with open("encoded_bits.txt", "r+") as f:
        file = f.read()
        jump = 1024 + 16  # start value
        it = 0
        with open("crc_values", "w+") as ff:
            for chunk in range(jump, len(file), jump):
                block = file[it:chunk]
                message = block[:1024]
                crc_bit_check = block[-16:]
                it += 1040
                if crc_obj.CRC_Check(message, crc_bit_check):
                    ff.write("0\n")
                else:
                    ff.write("1\n")
            ff.close()
        f.close()


def Encoding_Sent_Over_BSC(p):
    for prob in p:
        with open("encoded_bits.txt") as f:
            file = f.read()
            with open(f"encodedBSC{prob}.txt", "w+") as ff:
                for bit in file:
                    if random.random() < prob:
                        flip = (1 - int(bit)) % 2
                        ff.write(str(flip))
                    else:
                        ff.write(bit)
                ff.close()
            f.close()


def CheckBSCFiles(p):
    with open("encoded_bits.txt", "r+") as correct, open("encodedBSC0.1.txt", "r+") as encodedp01, open(
            "encodedBSC0.001.txt") as encodedp001, open("encodedBSC1e-05.txt", "r+") as encodedp00001:
        correct_file = correct.read()
        p1_file = encodedp01.read()
        p2_file = encodedp001.read()
        p3_file = encodedp00001.read()

        # correctness for each block
        blockP1 = 0
        blockP2 = 0
        blockP3 = 0

        jump = 1024 + 16
        it = 0
        for chunk in range(jump, len(correct_file), jump):
            block_c = correct_file[it:chunk]
            blocks_P1 = p1_file[it:chunk]
            blocks_P2 = p2_file[it:chunk]
            blocks_P3 = p3_file[it:chunk]

            if blocks_P1 != block_c: blockP1 += 1
            if blocks_P2 != block_c: blockP2 += 1
            if blocks_P3 != block_c: blockP3 += 1
        print(f"Correctness for each block. I.e #blocks that are not equal to the original")
        print(f"Dont look to much into this.... python is doing something weird... ")
        print(f"P1 (0.1) : {blockP1}")
        print(f"P1 (0.001) : {blockP2}")
        print(f"P1 (0.00001) : {blockP3}")
        print()

        correct.close()
        encodedp01.close()
        encodedp001.close()
        encodedp00001.close()

        # !=!==!=!==!
        # uncomment this
        # find_crc_correctness(p)  # calculate crc for each prob over BSC. Write to files
        with open("crc_values") as c, open("crc_values0.1") as p1, open("crc_values0.001") as p2, open(
                "crc_values1e-05") as p3:

            # store onto mem.

            # crc correctness
            crc_checksum_p1 = 0
            crc_checksum_p2 = 0
            crc_checksum_p3 = 0

            for P1, P2, P3 in zip(p1.readlines(), p2.readlines(), p3.readlines()):
                if int(P1) == 0: crc_checksum_p1 += 1
                if int(P2) == 0: crc_checksum_p2 += 1
                if int(P3) == 0: crc_checksum_p3 += 1
            print(f"Counts the #blocks, where CRC vector was 0")
            print(f"CRC - checksum counted (P1): {crc_checksum_p1} (zero vector)")
            print(f"CRC - checksum counted (P2): {crc_checksum_p2} (zero vector)")
            print(f"CRC - checksum counted (P3): {crc_checksum_p3} (zero vector)")
            print()

            c.close()
            p1.close()
            p2.close()
            p3.close()
        print(f"Supposed to be the difference between ACTUAL block & BSC(p) block ")
        print(f"CRC correctness - actual correctness: {abs(crc_checksum_p1 - blockP1)}")
        print(f"CRC correctness - actual correctness: {abs(crc_checksum_p2 - blockP2)}")
        print(f"CRC correctness - actual correctness: {abs(crc_checksum_p3 - blockP3)}")


def find_crc_correctness(p):
    # now check crc - correctness
    for prob in p:
        with open(f"encodedBSC{prob}.txt", "r+") as fff:
            fi = fff.read()
            jump = 1024 + 16  # start value
            it = 0
            with open(f"crc_values{prob}", "w+") as ffff:
                for chunk in range(jump, len(fi), jump):
                    block = fi[it:chunk]
                    message = block[:1024]
                    crc_bit_check = block[-16:]
                    it += 1040
                    if crc_obj.CRC_Check(message, crc_bit_check):
                        ffff.write("0\n")
                    else:
                        ffff.write("1\n")
                ffff.close()
            fff.close()


if __name__ == '__main__':
    # g(x), deg = 16
    div = "1000001011000101"

    # instantiate class
    crc_obj = CRC_En_Dec.CRC(div)

    # if not in directory, create new file
    if not os.path.isfile("original_bits.txt"):
        # write 1 MB of pseudo random bits.
        with open("original_bits.txt", "w+") as f:
            f.write(rand_key(1024 * 1024))
            f.close()
    # run encoding
    # store output
    # in "encoded_bits.txt"
    # with format b0+c0, b1+c1...bn+cn

    # !=!=!=!
    # Remember uncomment this!
    if not os.path.isfile("encoded_bits.txt"):
        Encoding()
        # Run file through BSC with diff. prob
        # write result to individual file
        Encoding_Sent_Over_BSC(p=[0.00001, 0.001, 0.1])

    # Now for "decoding" or crc check
    if not os.path.isfile("crc_values"):
        Decoding()  # creates the "correct" crc values file
        # now check each file over the BSC channel to that file
        CheckBSCFiles(p=[0.00001, 0.001, 0.1])
