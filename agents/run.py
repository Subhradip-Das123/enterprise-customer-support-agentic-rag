from agents.memory import ConversationMemory
from agents.planner_agent import PlannerAgent
from agents.support_agent import CustomerSupportAgent
from agents.management_agent import CustomerManagementAgent

memory = ConversationMemory()
planner = PlannerAgent()
support_agent = CustomerSupportAgent()
management_agent = CustomerManagementAgent()


def execute(query):
    memory.add("user", query)

    decision = planner.route(query)

    if decision == "SUPPORT":
        print("\n[PlannerAgent] Route selected: CustomerSupportAgent")
        return support_agent.handle(query, memory)

    if decision == "MANAGEMENT":
        print("\n[PlannerAgent] Route selected: CustomerManagementAgent")
        return management_agent.handle(query, memory)

    return "Unable to route the query."


if __name__ == "__main__":
    print("✅ Full Multi-Agent Customer Support System Started")

    while True:
        query = input("\nUser query (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        response = execute(query)

        print("\n✅ Final Response:\n")
        print(response)
