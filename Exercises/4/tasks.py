# sum of all elements field 17

_ = sum([x for x in range(17)]) % 17

mult = {}

for x in range(1, 17):
    y = 1
    while (x * y) != 1 % 17:
        y += 1
    mult[str(x)] = str(y)
    print(mult)
print(mult)
