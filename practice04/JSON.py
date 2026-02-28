import json

data = {
    "name": "Ali",
    "age": 20,
    "is_student": True
}

json_string = json.dumps(data)
print(json_string)


import json

json_string = '{"name": "Sara", "age": 25}'

data = json.loads(json_string)

print(data["name"])
print(type(data))

import json

data = {
    "city": "Almaty",
    "population": 2000000
}

with open("city.json", "w") as file:
    json.dump(data, file)

import json

with open("city.json", "r") as file:
    data = json.load(file)

print(data["city"])

import json

students = [
    {"name": "Ali", "grade": 90},
    {"name": "Sara", "grade": 95},
    {"name": "Timur", "grade": 85}
]

json_data = json.dumps(students, indent=4)
print(json_data)

