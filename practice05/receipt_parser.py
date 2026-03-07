import re
import json
with open("raw.txt", "r") as f:
    text = f.read()

datetime_pattern = r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})"
datetime_match = re.search(datetime_pattern, text)
date = datetime_match.group(1) if datetime_match else None
time = datetime_match.group(2) if datetime_match else None


item_pattern = r"(.+?)\n(\d[\d\s]*,\d{2})"
items_matches = re.findall(item_pattern, text)
items = []
for name in items_matches:
    items.append(name)

amount_pattern = r"\d[\d\s]*,\d{2}"
prices = re.findall(amount_pattern, text)
new_prices = []
for price in prices:
    number = float(price.replace(" ", '').replace(",", "."))
    new_prices.append(number)

total_amount = 0
for new_price in new_prices:
    total_amount += new_price

payment_pattern = r"(Банковская карта):\s*([\d\s]+,\d{2})"
payment_match = re.search(payment_pattern, text)
payment_method = payment_match.group(1).strip() if payment_match else None
payment_amount = payment_match.group(2).strip() if payment_match else None

receipt = {
    "date": date,
    "time": time,
    "items": items,
    "total_amount": total_amount,
    "payment_method": payment_method,
    "payment_amount": payment_amount
}

print(json.dumps(receipt))
