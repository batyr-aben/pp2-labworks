from datetime import datetime

today = datetime.now()
print(today)
    

from datetime import datetime

birth_year = int(input("Enter birthdate: "))
current_year = datetime.now().year

age = current_year - birth_year
print(age)

from datetime import date

today = date.today()

next_year = today.year + 1
new_year = date(next_year, 1, 1)

difference = new_year - today

print(f"Days left till New Year {differnce.days}")

from datetime import datetime

date1 = input()
date2 = input()

d1 = datetime.strptime(date1, "%d.%m.%Y")
d2 = datetime.strptime(date2, "%d.%m.%Y")

difference = d1 - d2

print(abs(difference.days)))


from datetime import datetime, timedelta

user_date = input()

d = datetime.strptime(user_date, "%d.%m.%Y")

new_date = d + timedelta(days=30)

print(new_date.strftime("%d.%m.%Y"))
