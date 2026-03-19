from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load SOP file
with open("sop.txt", "r") as file:
    sop_data = file.read()

# Split SOP into chunks
chunks = sop_data.split("\n\n")

while True:
    user_input = input("\nAsk something (type 'exit' to quit): ")

    if user_input.lower() == "exit":
        break

    # Step 1: Find relevant chunk
    relevant_chunk = ""

    for chunk in chunks:
        if any(word.lower() in chunk.lower() for word in user_input.split()):
            relevant_chunk = chunk
            break

    if not relevant_chunk:
        print("\nAI Response:")
        print("Not found in SOP.")
        continue

    print("\n[DEBUG] Using this chunk:")
    print(relevant_chunk)

    # 🔥 Step 2: Hybrid Control Logic
    if len(relevant_chunk.split("\n")) <= 3:
        # Small chunk → direct answer (SAFE)
        print("\nAI Response:")
        print(relevant_chunk)
    else:
        # Large chunk → controlled AI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=50,
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are a strict SOP-based assistant.

Rules:
- Answer ONLY from the provided SOP.
- If not found, say: "Not found in SOP."
- Keep answer short and exact.
- Do NOT add extra explanation.

SOP:
{relevant_chunk}
"""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        answer = response.choices[0].message.content

        # Force single sentence output
        answer = answer.split(".")[0] + "."

        print("\nAI Response:")
        print(answer)
        