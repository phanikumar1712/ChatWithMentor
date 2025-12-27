# gemini_memory.py - Gemini chat with memory (remembers conversation)

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()  # Loads your GOOGLE_API_KEY from .env

# Use the lightest model to save your free quota
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",  # Fast, free-tier friendly
    temperature=0.7
)

print("Gemini Chat with Memory (type 'exit' or 'bye' to quit)\n")

# This list stores the full conversation history
history = []

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() in ["exit", "bye", "quit"]:
        print("Goodbye!")
        break
    
    if not user_input:
        continue
    
    # Add your message to history
    history.append(HumanMessage(content=user_input))
    
    # Send full history to Gemini → it remembers everything
    response = llm.invoke(history)
    
    # Print Gemini's reply
    print("Gemini:", response.content.strip(), "\n")
    
    # Add Gemini's reply to history for next turn
    history.append(AIMessage(content=response.content))