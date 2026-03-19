from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load SOP content
with open("sop.txt", "r") as file:
    sop_data = file.read()

while True:
    user_input = input("\nAsk something (type 'exit' to quit): ")

    if user_input.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are an expert assistant. Use the following SOP to answer:\n{sop_data}"
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("\nAI Response:")
    print(response.choices[0].message.content)