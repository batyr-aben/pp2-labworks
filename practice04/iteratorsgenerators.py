def even_numbers(start, end):
    for num in range(start, end + 1):
        if num % 2 == 0:
            yield num

for n in even_numbers(1, 10):
    print(n)    


def word_splitter(text):
    word = ""
    for char in text:
        if char != " ":
            word += char
        else:
            if word:
                yield word
                word = ""
    if word:
        yield word
for w in word_splitter("hello world python"):
    print(w)

def factorial_generator(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
        yield result
for value in factorial_generator(5):
    print(value)

class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value
    
for num in Countdown(5):
    print(num)

def above_average(lst):
    avg = sum(lst) / len(lst)
    for num in lst:
        if num > avg:
            yield num
numbers = [10, 20, 30, 40, 50]
for n in above_average(numbers):
    print(n)
