class PlannerAgent:
    def route(self, query):
        query_lower = query.lower()

        # Informational / knowledge-seeking queries should go to Support Agent
        informational_patterns = [
            "how can",
            "how should",
            "what are",
            "what is",
            "explain",
            "best practices",
            "role of",
            "ways to",
            "steps to"
        ]

        if any(pattern in query_lower for pattern in informational_patterns):
            return "SUPPORT"

        # Direct complaints / escalation requests go to Management Agent
        management_keywords = [
            "i am angry",
            "i am frustrated",
            "i am very angry",
            "i am unhappy",
            "not satisfied",
            "complaint",
            "escalate",
            "manager",
            "urgent issue",
            "unresolved",
            "no one is responding"
        ]

        if any(keyword in query_lower for keyword in management_keywords):
            return "MANAGEMENT"

        # Default route
        return "SUPPORT"
