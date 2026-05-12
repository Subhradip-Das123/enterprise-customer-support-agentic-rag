from crewai import Crew, Process
from crew_ai.tasks import build_tasks


def run_customer_support_crew(user_query: str):
    tasks = build_tasks(user_query)

    crew = Crew(
        agents=[task.agent for task in tasks],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    return str(result)


if __name__ == "__main__":
    print("🚀 CrewAI Multi-Agent Customer Support System Started")

    while True:
        query = input("\nUser query (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        result = run_customer_support_crew(query)

        print("\n✅ Agent Final Answer\n")
        print(result)
