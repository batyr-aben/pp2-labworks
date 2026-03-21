from functools import reduce
numbers = [1, 2, 3, 4, 5]

squares = list(map(lambda x: x**2, numbers))

evens = list(filter(lambda x: x % 2 == 0, numbers))

print(squares)
print(evens)


numbers1 = [1, 2, 3, 4]

sum_all = reduce(lambda x, y: x + y, numbers)
print(sum_all)
