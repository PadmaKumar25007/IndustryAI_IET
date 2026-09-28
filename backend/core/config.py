from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database connection string
    # Default provided so FastAPI can start even if .env is missing/empty
    DATABASE_URL: str = "postgresql+psycopg://user:password@localhost:5432/dbname"
    
    # Load from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Instantiate settings
settings = Settings()
