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
        answer = response.choices[0].message.content.strip()

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
        answer = response.choices[0].message.content.strip()

    # 🔥 STEP 2 — Semantic Search (Main Logic)
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
            answer = "Not found in SOP."
        else:
            print("\n[DEBUG] Using this chunk:")
            print(relevant_chunk)

            # 🔥 STEP 3 — Hybrid + Controlled Response
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
- Keep the answer short and crisp (max 1–2 sentences).
- Use simple language.
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

                # 🔥 Smart post-processing (1–2 sentences max)
                sentences = answer.split(". ")

                if len(sentences) > 2:
                    answer = ". ".join(sentences[:2]) + "."

                answer = answer.strip()

    # ✅ FINAL OUTPUT
    print("\nAI Response:")
    print(answer)