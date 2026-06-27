import os
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

# Verify keys are loaded
assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY is missing!"
assert os.environ.get("TAVILY_API_KEY"), "TAVILY_API_KEY is missing!"
print("Environment keys loaded successfully.")