import json

data = {
    "employees": [
        {"name": "John", "score": 85},
        {"name": "Sara", "score": 92},
        {"name": "Mike", "score": 70}
    ]
}

top_employee = max(data["employees"], key=lambda x: x["score"])

print("Top performer:", top_employee["name"])
print("Score:", top_employee["score"])
scores = [emp["score"] for emp in data["employees"]]
average = sum(scores) / len(scores)

print("Average score:", round(average, 2))
print("Above average employees:")

for emp in data["employees"]:
    if emp["score"] > average:
        print(emp["name"])