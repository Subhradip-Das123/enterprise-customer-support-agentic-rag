from crewai import Task

from crew_ai.agents import (
    retriever_agent,
    support_response_agent,
    customer_management_agent,
    sentiment_feedback_agent,
    final_synthesis_agent
)


def build_tasks(user_query: str):
    retrieval_task = Task(
        description=(
            f"User query: {user_query}\n\n"
            "Use the Customer Support RAG Search Tool to retrieve relevant evidence "
            "from the customer support framework. Return the most important evidence "
            "with source names. Do not generate the final answer yet."
        ),
        expected_output=(
            "Relevant retrieved customer support evidence with source snippets."
        ),
        agent=retriever_agent
    )

    support_response_task = Task(
        description=(
            f"User query: {user_query}\n\n"
            "Using the retrieved evidence, prepare a practical customer support answer. "
            "Focus on actions support teams should take, communication style, empathy, "
            "follow-up, and issue resolution."
        ),
        expected_output=(
            "A customer support response grounded in the retrieved evidence."
        ),
        agent=support_response_agent,
        context=[retrieval_task]
    )

    management_task = Task(
        description=(
            f"User query: {user_query}\n\n"
            "Analyze the query from a customer management and escalation perspective. "
            "Decide whether escalation, customer success follow-up, retention action, "
            "or manager review is required."
        ),
        expected_output=(
            "Escalation and customer management analysis with recommended next actions."
        ),
        agent=customer_management_agent,
        context=[retrieval_task]
    )

    sentiment_task = Task(
        description=(
            f"User query: {user_query}\n\n"
            "Analyze the sentiment, urgency, and customer feedback signal. "
            "Identify whether the customer appears satisfied, neutral, dissatisfied, "
            "urgent, or requiring reassurance."
        ),
        expected_output=(
            "Sentiment, urgency, and feedback analysis."
        ),
        agent=sentiment_feedback_agent
    )

    final_task = Task(
        description=(
            f"User query: {user_query}\n\n"
            "Combine all previous agent outputs into a final response.\n\n"
            "Final response must include:\n"
            "1. Direct answer to the user\n"
            "2. Retrieved evidence summary\n"
            "3. Support recommendation\n"
            "4. Escalation/customer management recommendation\n"
            "5. Sentiment/urgency assessment\n\n"
            "Keep the answer professional and structured."
        ),
        expected_output=(
            "Final enterprise customer support intelligence response."
        ),
        agent=final_synthesis_agent,
        context=[
            retrieval_task,
            support_response_task,
            management_task,
            sentiment_task
        ]
    )

    return [
        retrieval_task,
        support_response_task,
        management_task,
        sentiment_task,
        final_task
    ]
