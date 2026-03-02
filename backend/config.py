import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "renewai-demo")
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_PRO_MODEL = "gemini-2.0-flash"  # Use same model for both in demo
EMBEDDING_MODEL = "models/text-embedding-004"
CORS_ORIGINS = ["*"]
API_PREFIX = "/api"
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
