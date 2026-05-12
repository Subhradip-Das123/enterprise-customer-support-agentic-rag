class ConversationMemory:
    def __init__(self, max_turns=6):
        self.history = []
        self.max_turns = max_turns

    def add(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })

        # Keep only last N messages to avoid context explosion
        if len(self.history) > self.max_turns:
            self.history = self.history[-self.max_turns:]

    def get_context(self):
        if not self.history:
            return "No previous conversation."

        return "\n".join(
            f"{message['role']}: {message['content'][:300]}"
            for message in self.history
        )

    def clear(self):
        self.history = []
