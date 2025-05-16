from google import genai
import os
from dotenv import load_dotenv

load_dotenv()


def InitializeModel():
    API_KEY=os.getenv("GEMINI_API_KEY")
    chat1 = genai.Client(api_key=API_KEY)

    return chat1