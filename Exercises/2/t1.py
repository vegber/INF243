from scipy.spatial import distance
import BitVector

C = [BitVector.BitVector(bitlist=[0, 0, 0, 0, 0, 0]),
     BitVector.BitVector(bitlist=[0, 0, 1, 1, 1, 1]),
     BitVector.BitVector(bitlist=[1, 1, 0, 0, 1, 1]),
     BitVector.BitVector(bitlist=[1, 1, 1, 1, 0, 0]),
     BitVector.BitVector(bitlist=[1, 0, 1, 0, 1, 0]),
     BitVector.BitVector(bitlist=[1, 1, 1, 1, 1, 0])]


def hamming_distance(arr1, arr2):
    return sum(el1 != el2 for el1, el2 in zip(arr1, arr2))


def one():
    d = 999999
    for i in range(len(C)):
        for j in range(i, len(C) - 1):
            D_ = hamming_distance(C[i], C[j])
            if d > D_: d = D_
    print(d)


def two(C):
    """
    Vector space
    :return:
    """
    C_ = [x for x in C]
    notin = 0
    for i in range(len(C)):
        for j in range(i, len(C)):
            out = C[i] ^ C[j]
            if out not in C_:
                notin += 1
                C_.append(out)
    print(f"Not in C: {notin} with length {len(C_)}", end="\n")
    return C_


def gilbertVarshamovTest(n, k, d, field):
    """
    Implement the Gilbert-Varshamov (GV) test.

    Parameters:
        n (int): The length of the code.
        k (int): The dimension of the code.
        d (int): The minimum distance of the code.
        field (int): The field (e.g. int, float, complex) of the coefficients.

    Returns:
        list: A code that passes the GV test.
    """
    # Generate a random code
    # code = [[random.choice(field) for _ in range(k)] for _ in range(n)]
    code = C
    # Check if the code has the desired properties
    if min([hamming_distance(code[i], code[j]) for i in range(n) for j in range(i + 1, n)]) >= d:
        return code

    return None


"""
first_ = two(C)
var = [print(x) for x in first_]
print()
sec = two(first_)
#var2 = [print(x.__str__()) for x in sec]
"""
x = ([x.__str__() for x in gilbertVarshamovTest(6, 7, 1, 2)])
print(x)
