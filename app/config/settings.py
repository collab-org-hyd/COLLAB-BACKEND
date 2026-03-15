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
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
