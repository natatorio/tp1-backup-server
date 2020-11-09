
class Task:
    def __init__(self, entry):
        self.ip = entry.ip
        self.port = entry.port
        self.path = entry.path
        self.rate = entry.rate
        self.remaining = entry.rate

    def advance(self, other = None):
        if other:
            self.remaining = other.remaining
        else:
            self.remaining = max(0, self.remaining - 1)

    def __eq__(self, other):
        return self.ip == other.ip and self.port == other.port and self.path == other.path

    def needs_to_be_executed(self):
        return self.remaining == 0

    def reschedule(self):
        self.remaining = self.rate
