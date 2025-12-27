import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.0-pro",   # ✅ CORRECT
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
)

response = llm.invoke([
    HumanMessage(content="Say hello in one short sentence")
])

print("Gemini response:")
print(response.content)
