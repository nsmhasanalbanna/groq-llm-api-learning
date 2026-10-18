from tests.fake_groq import FakeClient

def get_fake_groq_client():
    fake_groq_client = FakeClient()
    return fake_groq_client