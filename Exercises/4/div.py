var = []
generators = []

for i in range(1, 17):
    for j in range(1, 17):
        var.append((i ** j) % 17)
    if len(set(var)) == 16:
        generators.append(i)
    var = []

print(generators)

for gen in generators:
    for i in range(1, 17):
        print(f"{gen} ^ {i}: == {gen ** i % 17}")
    print()
print(generators)
print(len(generators))
