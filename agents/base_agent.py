class BaseAgent:
    def __init__(self, name):
        self.name = name

    def process(self, data):
        raise NotImplementedError("Each agent must implement process()")

    def log(self, message):
        print(f"[{self.name}] {message}")