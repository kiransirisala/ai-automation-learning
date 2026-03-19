from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key="sk-xxxxx")

while True:
    user_input = input("\nAsk something (type 'exit' to quit): ")

    if user_input.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an operations and quality audit expert helping with SOP-related queries."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("\nAI Response:")
    print(response.choices[0].message.content)
