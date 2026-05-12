import os
from dotenv import load_dotenv
from crewai import Agent, LLM

from crew_ai.tools import CustomerSupportRAGTool

load_dotenv()

gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)

rag_tool = CustomerSupportRAGTool()


retriever_agent = Agent(
    role="Customer Support Retriever Agent",
    goal=(
        "Retrieve the most relevant customer support framework evidence "
        "from the FAISS knowledge base."
    ),
    backstory=(
        "You are a retrieval specialist. Your job is not to generate the final answer. "
        "You only search the enterprise customer support framework and return useful evidence."
    ),
    tools=[rag_tool],
    llm=gemini_llm,
    verbose=True
)


support_response_agent = Agent(
    role="Customer Support Response Agent",
    goal=(
        "Generate a helpful customer support answer using the retrieved evidence."
    ),
    backstory=(
        "You are an expert enterprise customer support advisor. "
        "You explain best practices clearly and practically using the retrieved support framework."
    ),
    llm=gemini_llm,
    verbose=True
)


customer_management_agent = Agent(
    role="Customer Management and Escalation Agent",
    goal=(
        "Analyze whether the query indicates escalation, dissatisfaction, urgency, "
        "or customer management attention."
    ),
    backstory=(
        "You are responsible for customer retention, escalation handling, "
        "priority routing, and management-level follow-up recommendations."
    ),
    llm=gemini_llm,
    verbose=True
)


sentiment_feedback_agent = Agent(
    role="Sentiment and Feedback Agent",
    goal=(
        "Evaluate customer tone, urgency, satisfaction level, and feedback signals."
    ),
    backstory=(
        "You analyze customer sentiment and identify whether the interaction "
        "requires empathy, reassurance, escalation, or proactive follow-up."
    ),
    llm=gemini_llm,
    verbose=True
)


final_synthesis_agent = Agent(
    role="Final Customer Support Intelligence Agent",
    goal=(
        "Combine retrieved evidence, support advice, escalation analysis, "
        "and sentiment insights into one final enterprise-grade response."
    ),
    backstory=(
        "You are the final decision-making customer support intelligence agent. "
        "You produce a complete response that is grounded, structured, practical, and professional."
    ),
    llm=gemini_llm,
    verbose=True
)
