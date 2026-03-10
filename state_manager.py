class AgentState:

    def __init__(self):
        self.task = None
        self.plan = []
        self.history = []

    def set_task(self, task):
        self.task = task

    def add_step(self, step):
        self.plan.append(step)

    def add_history(self, message):
        self.history.append(message)

    def get_state(self):
        return {
            "task": self.task,
            "plan": self.plan,
            "history": self.history
        }