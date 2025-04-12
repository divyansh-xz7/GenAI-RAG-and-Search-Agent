from langchain_groq import ChatGroq
import os

os.environ['GROQ_API_KEY'] = 'your key'


GROQ_LLM = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.5,
)
