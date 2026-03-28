from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import os
import dotenv


dotenv.load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    database_url: str = os.environ.get("PG_DATABASE_URL")
    
    # App
    app_name: str = "COLLAB Backend"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # CORS - For development with Flutter on localhost (any port)
    # Default allows all localhost ports. For production, set specific origins via CORS_ORIGINS env var
    cors_origins: str = os.environ.get("CORS_ORIGINS", "*")
    
    # Email Configuration
    smtp_server: str = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.environ.get("SMTP_PORT", 587))
    sender_email: str = os.environ.get("SENDER_EMAIL", "")
    sender_password: str = os.environ.get("SENDER_PASSWORD", "")
    sender_name: str = os.environ.get("SENDER_NAME", "COLLAB")
    
    # SMS Configuration
    sms_api_key: str = os.environ.get("SMS_API_KEY", "")
    sms_sender_id: str = os.environ.get("SMS_SENDER_ID", "COLLAB")
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
