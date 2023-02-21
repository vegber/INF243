import numpy as np


# generate all messages binary length four
def generate_binary_permutations(n):
    if n == 0:
        return []
    elif n == 1:
        return ['0', '1']
    else:
        prev = generate_binary_permutations(n - 1)
        result = []
        for p in prev:
            result.append(p + '0')
            result.append(p + '1')
        return result


def matrix_vector_multiply(matrix, vector):
    result = []
    for i in range(len(matrix)):
        sum = 0
        for j in range(len(matrix[i])):
            sum += matrix[i][j] * vector[i]
        result.append(sum % 2)
    return result


G = [[1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0],
     [0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
     [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
     [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1]]

if __name__ == '__main__':
    messages = [[int(char) for char in string] for string in generate_binary_permutations(4)]
    coded_messages = []
    # print(messages)
    A = np.array([messages[1]])
    C = A.dot(G)
    for m in messages:
        m = np.array([m])  # something to do with numpy - needs 2D list
        C = m.dot(G)
        C = [c % 2 for c in C]
        coded_messages.append(C)
    [print(str(x).lstrip("[[").rstrip("]]"), "\n") for x in coded_messages]

# Codewords should be
"""
[(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
 (1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0),
 (0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1),
 (1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1),
 (0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1),
 (1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1),
 (0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0),
 (1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0),
 (0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1),
 (1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1),
 (0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0),
 (1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0),
 (0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0),
 (1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0),
 (0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1),
 (1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1)]
"""
