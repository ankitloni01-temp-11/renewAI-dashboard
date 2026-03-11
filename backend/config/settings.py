import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application configuration"""
    
    # Gemini API Configuration
    GEMINI_API_KEY = "AIzaSyChP8adR3fzaCBgW_11oMrtxXZ9zJVExGU"
    GEMINI_MODEL = "gemini-2.0-flash"
    GEMINI_TEMPERATURE = 0.7
    
    # Database Configuration
    AUDIT_DB_PATH = "database/audit.db"
    CRM_DB_PATH = "database/crm.db"
    CHROMA_DB_PATH = "database/chroma_db"
    
    # RAG Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    SIMILARITY_THRESHOLD = 0.7
    TOP_K_RESULTS = 3
    
    # Agent Configuration
    MAX_CRITIQUE_RETRIES = 3
    ESCALATION_TIMEOUT = 30
    
    # Supported Languages
    LANGUAGES = ["English", "Hindi", "Marathi", "Tamil", "Telugu", "Kannada", "Bengali", "Gujarati", "Punjabi"]
    
    # Channels
    CHANNELS = ["email", "whatsapp", "voice"]

settings = Settings()