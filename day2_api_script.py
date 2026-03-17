import requests

city = input("Enter city name: ")

url = f"https://wttr.in/{city}?format=j1"

response = requests.get(url)

data = response.json()

temp = data["current_condition"][0]["temp_C"]

print("Temperature:", temp)
desc = data["current_condition"][0]["weatherDesc"][0]["value"]

print("Condition:", desc)

