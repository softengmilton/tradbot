import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    DEBUG = ENVIRONMENT == "development"

config = Config()
