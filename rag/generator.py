from rag.retriever import retrieve
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyDq-IEQGV8JuSkbd5TRDf7ftlPQ9ljq8dc"))

model = genai.GenerativeModel("models/gemini-2.5-flash")


def generate_answer(query: str, k: int = 10):
    docs = retrieve(query, k=k)

    context = "\n\n".join(
        [f"- {doc.page_content}" for doc in docs]
    )

    prompt = f"""
You are an enterprise customer support advisor.

Instructions:
- Use the context below as your primary source.
- Summarize best practices, principles, and examples from the text.
- You may generalize carefully if ideas are clearly implied.
- Do NOT invent policies, numbers, or rules not mentioned.
- If the context is clearly unrelated, say you lack sufficient information.

Context:
{context}

Question:
{query}

Answer (in 4–6 clear bullet points):
"""

    response = model.generate_content(prompt)
    return response.text.strip()


if __name__ == "__main__":
    test_questions = [
        "How should customer support communicate when there are delays in response?",
        "What are best practices for handling unhappy customers?",
        "How can support teams de‑escalate frustrated customers?",
        "What role does empathy play in customer support?",
        "How should support teams follow up after resolving an issue?"
    ]

    for q in test_questions:
        print("\nQUESTION:", q)
        print(generate_answer(q))
