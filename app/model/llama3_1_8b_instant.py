from langchain_groq import ChatGroq
import os

from dotenv import load_dotenv
load_dotenv()


def InitializeModel():
    GROQ_API_KEY=os.getenv("GROQ_API_KEY")
    chat = ChatGroq(temperature=0.1, groq_api_key=GROQ_API_KEY, model_name="llama-3.1-8b-instant")
    return chat