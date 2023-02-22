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


def generate_codewords():
    # Field 2 n = 7 - even 1's
    out = []
    messages = [[int(char) for char in string] for string in generate_binary_permutations(7)]

    for m in messages:
        if m.count(1) % 2 == 0: out.append(m)
    return out


def add_under_field(list1, list2, field):
    assert len(list1) == len(list2)
    return [(list1[i] + list2[i]) % field for i in range(len(list1))]


def run(codewords, field):
    for x in range(len(codewords)):
        for y in range(x + 1, len(codewords)):
            t1 = add_under_field(codewords[x], codewords[y], field)
            if t1 not in codewords:
                print(f"Contradiction: not in codewords: {t1}: {codewords[x]} + {codewords[y]}")
                return


if __name__ == '__main__':
    code_2 = [
        [0, 2, 1],
        [2, 0, 1],
        [1, 0, 2],
        [1, 1, 1],
        [2, 1, 0],
        [0, 0, 0],
        [2, 2, 2],
        [1, 2, 0]
    ]

    codes_even_ones = generate_codewords()
    print((codes_even_ones))
    run(codes_even_ones, 2)

    print()

    print(run(code_2, 3))
