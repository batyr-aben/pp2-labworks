a = 33
b = 34
if b == a:
  print("a and b are equal")
elif b > a:
  print("b is greater than a")

score = 70
if score >= 90:
  print("Your grade is A")
elif score >= 80:
  print("Your grade is B")
elif score >= 70:
  print("Your grade is C")

age = 15
if age <= 13:
  print("You are a child")
elif age <= 18:
  print("You are a teenager")
elif age <= 65:
  print("You are an adult")

username = "Batyr"
if len(username) == 0:
  print("Enter your username")
elif len(username) != 0:
  print(f"Hello, {username}")

number = -9
if number > 0:
  print("The number is positive")
elif number < 0:
  print("The number is negative")
else:
  print("Zero")

letter = "B"
if letter == "C":
  print("letter is C")
elif letter == "A":
  print("letter is A")
elif letter == "B":
  print("letter is B")
