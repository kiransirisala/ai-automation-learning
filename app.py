import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load SOP
with open("sop.txt", "r") as file:
    sop_data = file.read()

chunks = sop_data.split("\n\n")

st.title("SOP Mate 🤖")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_input = st.chat_input("Ask your question")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    query = user_input.lower()

    # 🔥 STEP 1 — SUMMARY / OVERVIEW
    if "summary" in query or "overview" in query or "what is this sop" in query:
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

    # 🔥 STEP 2 — SIMPLE EXPLANATION
    elif "simple" in query or "easy" in query or "explain" in query:
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

    # 🔥 STEP 3 — DEFAULT RAG (YOUR EXISTING LOGIC)
    else:
        relevant_chunk = ""

        for chunk in chunks:
            if any(word.lower() in chunk.lower() for word in user_input.split()):
                relevant_chunk = chunk
                break

        if not relevant_chunk:
            answer = "Not found in SOP."
        else:
            if len(relevant_chunk.split("\n")) <= 3:
                answer = relevant_chunk
            else:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    max_tokens=50,
                    messages=[
                        {
                            "role": "system",
                            "content": f"Answer only from this SOP:\n{relevant_chunk}"
                        },
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ]
                )
                answer = response.choices[0].message.content
                answer = answer.split(".")[0] + "."

    # FINAL OUTPUT
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)

    