import os
from dotenv import load_dotenv
# Load credentials from .env file
load_dotenv()

from tavily import TavilyClient
from langchain.tools import tool
from typing import Dict, Any
# pyrefly: ignore [missing-import]
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent

# Verify keys are loaded
assert os.environ.get("GEMINI_API_KEY"), "GEMINI_API_KEY is missing!"
assert os.environ.get("TAVILY_API_KEY"), "TAVILY_API_KEY is missing!"

# Initialize the Tavily tool to search the web for recipes
tavily_client = TavilyClient()

@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)

system_prompt = """
You are a Personal Chef. 
1. In your first interaction, greet the user warmly and ask for their name, as well as any dietary preferences, restrictions, or food allergies.
2. Remember this information. In all subsequent interactions, address them by their name and ensure all recipe suggestions strictly respect their dietary restrictions (e.g. vegetarian, gluten-free) and allergies.
3. Use the search tool to find recipes using their leftover ingredients, list prep times, and highlight both used and extra ingredients.
"""

# Initialize Gemini Chat Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# Initialize the memory saver checkpointer
memory = MemorySaver()

# Create the agent using the Gemini model object and checkpointer memory
agent = create_agent(
    model=llm,
    tools=[web_search],
    system_prompt=system_prompt,
    checkpointer=memory
)

def ask_chef_agent(user_input: str, thread_id: str) -> str:
    """Invokes the agent and returns the clean text output."""
    config = {"configurable": {"thread_id": thread_id}}
    
    # Run the agent
    response = agent.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config
    )
    
    # Extract response text
    agent_message = response["messages"][-1]
    content = agent_message.content
    
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        return "".join(
            block.get("text", "") for block in content 
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return ""
