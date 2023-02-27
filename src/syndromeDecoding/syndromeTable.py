import numpy as np

# Define the generator matrix G and parity check matrix H
G = np.array([[1, 0, 1, 0, 1, 1],
              [0, 1, 1, 1, 0, 1],
              [0, 1, 1, 0, 1, 0]])

H = np.array([[1, 1, 0, 1, 1, 0],
              [1, 0, 1, 0, 1, 1],
              [0, 1, 0, 0, 1, 1]])

# Define the binary field
GF2 = np.array([0, 1], dtype=int)

# Define all possible syndrome vectors
s_list = []
for i in range(2 ** H.shape[0]):
    s = np.array(list(np.binary_repr(i, width=H.shape[0])), dtype=int)
    s_list.append(s)

# Create the syndrome decoding table
table = {}

# add zero vector,
# table[np.zeros(G.shape[1], dtype=int)] = []

# add first entry of table
syndromes_ = []
for v in s_list:
    syndromes_.append(np.mod(np.dot(v, G), 2))

table[str(np.zeros(G.shape[1], dtype=int))] = syndromes_


def add_cosetLeader(d: dict, weight: int):
    """
    Generate coset leaders for syndrome table for given weight
    :param d:
    :param weight:
    :return:
    """
    for i in range(2 ** G.shape[0]):
        entry = np.array(list(np.binary_repr(i, width=G.shape[1])), dtype=int)
        print(entry)
    return d


# table = add_cosetLeader(table, 1)
print(s_list[1])
test = np.mod(np.dot(s_list[1], H), 2)
print(test)
