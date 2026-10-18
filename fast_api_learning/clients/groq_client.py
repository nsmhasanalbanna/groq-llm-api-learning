from groq import Groq
from config.settings import settings

groq_client = Groq(api_key=settings.groq_api_key)

groq_model = settings.groq_model

def get_groq_client():
    return groq_client



