"""
Configuration module for AI Career Navigator
Centralizes all configuration settings
"""
import os
import logging

logger = logging.getLogger(__name__)

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
# COST OPTIMIZATION: Using GPT-3.5-Turbo (10x cheaper than GPT-4!)
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-35-turbo")
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_CHATGPT_MODEL", "gpt-35-turbo")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

# Cost Control Settings
MAX_TOKENS_DEFAULT = 1200  # Reduced from 2000
MAX_TOKENS_ANALYSIS = 1500  # Reduced from 3000
MAX_TOKENS_INTERVIEW = 2000  # Reduced from 6000
TEMPERATURE = 0.6  # Slightly lower for more focused responses

# Flask Configuration
FLASK_PORT = int(os.getenv("PORT", "8000"))
FLASK_HOST = os.getenv("HOST", "0.0.0.0")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

# Postgres / Database Configuration (local development defaults)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "ai_career_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

# DATABASE_URL can be provided directly or constructed from POSTGRES_* vars
DATABASE_URL = os.getenv("DATABASE_URL") or (
    # Use pg8000 pure-Python driver for local development to avoid native wheels
    f"postgresql+pg8000://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Application Metadata
APP_NAME = "AI Career Navigator"
APP_VERSION = "2.0.1"
APP_DESCRIPTION = "Production-ready AI Career Guidance Platform"

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'

# Validate Configuration
def validate_config():
    """Validate that required configuration is present"""
    missing = []
    
    if not AZURE_OPENAI_ENDPOINT:
        missing.append("AZURE_OPENAI_ENDPOINT")
    if not AZURE_OPENAI_API_KEY:
        missing.append("AZURE_OPENAI_API_KEY")
    
    # If Azure OpenAI credentials are missing but a local DATABASE_URL is provided,
    # allow the app to run in a degraded/local-mode without OpenAI.
    if missing and DATABASE_URL:
        logger.info("⚠️ Azure OpenAI not configured — running with local DATABASE_URL only")
        return True

    if missing:
        logger.warning(f"⚠️ Missing configuration: {', '.join(missing)}")
        return False

    logger.info("✅ Configuration validated successfully")
    return True

