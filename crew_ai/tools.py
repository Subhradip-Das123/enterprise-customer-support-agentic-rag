from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

from rag.retriever import retrieve


class CustomerSupportRAGInput(BaseModel):
    query: str = Field(
        ...,
        description="Customer support question to search in the FAISS knowledge base."
    )


class CustomerSupportRAGTool(BaseTool):
    name: str = "customer_support_rag_search_tool"
    description: str = (
        "Searches the enterprise customer support knowledge base using FAISS "
        "and returns relevant document evidence with source snippets."
    )
    args_schema: Type[BaseModel] = CustomerSupportRAGInput

    def _run(self, query: str) -> str:
        docs = retrieve(query, k=5)

        if not docs:
            return "No relevant customer support knowledge found."

        output = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "unknown source")
            snippet = doc.page_content[:700].replace("\n", " ")
            output.append(
                f"Source {i}: {source}\n"
                f"Evidence:\n{snippet}\n"
            )

        return "\n" + "\n" + ("-" * 80) + "\n".join(output)
