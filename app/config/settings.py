from pydantic_settings import BaseSettings
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
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
