# x^2 + x + 1 = 0

for x in range(17):
    l = ((x ** 2) + x + 1) % 17
    print(f"{x} = {l}")
