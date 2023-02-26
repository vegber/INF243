import CRCEncodingDecoding as ced

start = "11010011101100"
# x^3 + x + 1
divisor = "1011"


def fnInBin(s):
    return set(s).issubset({'0'}) and bool(s)


import re

a = "1011"
b = "00001"


def xor(a: str, b: str):
    assert len(a) == len(b), print("not equal")
    return ''.join([str(int(a) ^ int(b)) for a, b in zip(a, b)])


def findWindow(bit_stream):
    _ = re.search('1', bit_stream)
    if _ is not None:
        return _.start()
    else:
        return -1


def replace_string(A, B, C):
    if len(A) <= B:
        return A
    elif len(C) >= len(A) - B:
        return A[:B] + C[:len(A) - B]
    else:
        return A[:B] + C + A[B + len(C):]


import CRCEncodingDecoding as sondre

# x^3 + x + 1
div = "1011"
obj = sondre.CRC(div)

message = "11010011101100"
_ = obj.Encode(message, 3)
print(_)
