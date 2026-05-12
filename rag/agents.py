"""
Agentic workflow (Planner → Tool → Executor)
WITHOUT LangChain Agent APIs (stable & capstone-safe)
"""

from rag.generator import generate_answer


# -------------------------
# Tool: RAG
# -------------------------
def knowledge_search(query: str) -> str:
    """RAG tool: retrieves and generates a grounded answer."""
    return generate_answer(query)


# -------------------------
# Planner Agent
# -------------------------
def planner(query: str) -> str:
    """
    Decide how to handle the user query.
    For this capstone:
    - If the query relates to customer support practices, use RAG.
    - Otherwise, politely refuse.
    """
    keywords = [
        "customer", "support", "delay", "communication",
        "frustrated", "empathy", "response", "resolution"
    ]

    if any(k in query.lower() for k in keywords):
        return "USE_RAG"
    else:
        return "NO_KNOWLEDGE"


# -------------------------
# Executor Agent
# -------------------------
def execute(query: str) -> str:
    decision = planner(query)

    if decision == "USE_RAG":
        return knowledge_search(query)
    else:
        return "I don’t have enough information to answer this question."


# -------------------------
# Interactive Loop
# -------------------------
if __name__ == "__main__":
    print("✅ Agentic RAG System Ready")

    while True:
        query = input("\nAsk a question (type 'exit' to quit): ")
        if query.lower() == "exit":
            break

        answer = execute(query)
        print("\n✅ Agent Answer:\n")
        print(answer)

