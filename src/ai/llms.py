from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI


def get_openai_models(model="gemini-2.5-flash"):
    if model is None:
        model = "gemini-2.5-flash"
    return ChatGoogleGenerativeAI(
    model=model,
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0,
    )