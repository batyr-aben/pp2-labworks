names = ["Alice", "Patrick", "Epstein"]


for index, name in enumerate(names):
    print(index, name)

ages = [20, 25, 30]
for name, age in zip(names, ages):
    print(name, age)
value = "123"

print(isinstance(value, str))

num = int(value)
flt = float(value)

print(num, flt)
