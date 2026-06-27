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


