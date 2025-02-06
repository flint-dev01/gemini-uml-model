from langchain_groq import ChatGroq
import os

from dotenv import load_dotenv
load_dotenv()


def InitializeModel():
    GROQ_API_KEY1=os.getenv("GROQ_API_KEY_T")
    GROQ_API_KEY2=os.getenv("GROQ_API_KEY_R")
    chat1 = ChatGroq(temperature=0.1, groq_api_key=GROQ_API_KEY1, model_name="llama-3.1-8b-instant")
    chat2 = ChatGroq(temperature=0.1, groq_api_key=GROQ_API_KEY2, model_name="llama-3.1-8b-instant")
    return chat1,chat2