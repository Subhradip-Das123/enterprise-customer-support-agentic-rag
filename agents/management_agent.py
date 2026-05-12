class CustomerManagementAgent:
    def handle(self, query, memory):
        response = """
This case appears to require customer management attention.

Recommended action:
- Route the issue to a senior support representative or customer success manager.
- Treat the issue as high priority.
- Review the customer's previous interaction history.
- Follow up promptly with a clear next step.
- Track the case until resolution.
"""

        memory.add("assistant", response)
        return response
