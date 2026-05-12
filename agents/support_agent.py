from rag.generator import generate_answer

class CustomerSupportAgent:
    def handle(self, query, memory):
        previous_context = memory.get_context()

        enriched_query = f"""
Previous conversation:
{previous_context}

Current user query:
{query}
"""

        response = generate_answer(enriched_query)
        memory.add("assistant", response)
        return response
