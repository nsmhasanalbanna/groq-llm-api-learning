class FakeClient:
    def __init__(self):
        self.chat = FakeChat()

class FakeChat:
    def __init__(self):
        self.completions = FakeCompletions()

class FakeCompletions:
    def create(self, **kwargs):
        response = FakeResponse()
        return response
        

class FakeResponse:
    def __init__(self):
        self.choices = []
        self.choices.insert(0, FakeChoices())

class FakeChoices:
    def __init__(self):
        self.message = FakeMessage()

class FakeMessage:
    def __init__(self):
        self.content = "Fake AI Response"



