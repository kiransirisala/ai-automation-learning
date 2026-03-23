from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

    query = user_input.lower()

    # 🔥 STEP 1 — Intent Handling (Summary / Explain)
    if "summary" in query or "overview" in query:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=100,
            messages=[
                {
                    "role": "system",
                    "content": f"Summarize this SOP in simple terms:\n{sop_data}"
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        answer = response.choices[0].message.content

    elif "simple" in query or "explain" in query:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=100,
            messages=[
                {
                    "role": "system",
                    "content": f"Explain this SOP in simple terms:\n{sop_data}"
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        answer = response.choices[0].message.content

    # 🔥 STEP 2 — Semantic Search (Main Upgrade)
    else:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(chunks + [query])

        similarity = cosine_similarity(vectors[-1], vectors[:-1])

        best_match_index = similarity.argmax()
        best_score = similarity[0][best_match_index]

        # Threshold to avoid wrong matches
        if best_score < 0.2:
            relevant_chunk = ""
        else:
            relevant_chunk = chunks[best_match_index]

        if not relevant_chunk:
            print("\nAI Response:")
            print("Not found in SOP.")
            continue

        print("\n[DEBUG] Using this chunk:")
        print(relevant_chunk)

        # 🔥 STEP 3 — Hybrid Response
        if len(relevant_chunk.split("\n")) <= 3:
            answer = relevant_chunk
        else:
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
            answer = answer.split(".")[0] + "."

    # ✅ FINAL OUTPUT (COMMON)
    print("\nAI Response:")
    print(answer)