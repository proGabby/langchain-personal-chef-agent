import os
from dotenv import load_dotenv
# Load credentials from .env file
load_dotenv()

from tavily import TavilyClient
from langchain.tools import tool
from typing import Dict, Any
# pyrefly: ignore [missing-import]
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# Verify keys are loaded
assert os.environ.get("GEMINI_API_KEY"), "GEMINI_API_KEY is missing!"
assert os.environ.get("TAVILY_API_KEY"), "TAVILY_API_KEY is missing!"
print("Environment keys loaded successfully.")

# Initialize the Tavily tool to search the web for recipes
tavily_client = TavilyClient()

@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)

system_prompt = """
You are a Personal Chef. Find recipes using only the leftover ingredients.
Use the search tool to find recipes, list prep times, highlight used/extra ingredients, and answer cooking follow-up questions.
"""

# Initialize Gemini Chat Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

from langchain.agents import create_agent

# Create the agent using the Gemini model object
agent = create_agent(
    model=llm,
    tools=[web_search],
    system_prompt=system_prompt
)

# Interactive chat loop to converse with the chef
print("\n=== Personal Chef Assistant is ready! ===")
print("Type your leftover ingredients to get recipes, and ask follow-up questions.")
print("Type 'exit' or 'quit' to end the session.\n")

messages = []

while True:
    try:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Chef: Happy cooking! Goodbye!")
            break
            
        if not user_input.strip():
            continue
            
        # Add the human message to the history
        messages.append(HumanMessage(content=user_input))
        
        # Run the agent
        response = agent.invoke({"messages": messages})
        
        # Extract the agent's response message
        agent_message = response["messages"][-1]
        
        # Save it to the conversation history
        messages.append(agent_message)
        
        # Extract the text cleanly
        content = agent_message.content
        text_response = ""
        if isinstance(content, str):
            text_response = content
        elif isinstance(content, list):
            text_response = "".join(
                block.get("text", "") for block in content 
                if isinstance(block, dict) and block.get("type") == "text"
            )
            
        print(f"\nChef:\n{text_response}\n")
        
    except KeyboardInterrupt:
        print("\nChef: Happy cooking! Goodbye!")
        break
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")
