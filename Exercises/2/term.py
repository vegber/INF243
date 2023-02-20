def calc(M):
    s = 0
    i = M - 1
    for m in range(M):
        s += i * m
        i -= 1
    return s


print(calc(12))
