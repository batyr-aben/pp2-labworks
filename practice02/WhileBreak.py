i = 1
while i < 6:
  print(i)
  if i == 3: 
    break
  i += 1

i = 2
while i < 10:
  if i % 2 == 0:
    if i == 4:
      break
    else:
      print(i)
  i += 1

i = 3 
while i < 10:
  if i == 5:
    break
  else:
    print(i)
  i += 1

while True:
    res = input("Enter the number 5: ")
    if res == 5:
        break
