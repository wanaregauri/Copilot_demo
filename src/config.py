"""Configuration module for Gold Rate Update application."""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration."""
    
    # API Configuration
    METALS_API_URL = "https://www.goldpriceindia.com/"
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", 10))
    
    # Email Configuration
    EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
    EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    
    # Scheduler Configuration
    SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", 8))
    SCHEDULE_MINUTE = int(os.getenv("SCHEDULE_MINUTE", 0))
    
    # Application Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    PROJECT_ROOT = Path(__file__).parent.parent
    LOG_DIR = PROJECT_ROOT / "logs"
    
    # Ensure log directory exists
    LOG_DIR.mkdir(exist_ok=True)
    
    LOG_FILE = LOG_DIR / "gold_rate_update.log"
    DATA_FILE = PROJECT_ROOT / "gold_rates.json"


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = "INFO"


# Select configuration based on environment
config = ProductionConfig()
