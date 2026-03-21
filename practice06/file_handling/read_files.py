with open("sample.txt", "w") as s:
    s.write("Hello, world!\n")
    s.write("This is a sample file\n")

with open("sample.txt", "r") as s:
    content = s.read()
    print(content)
