from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "XPulse: The Tribunal"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "xpulse_tribunal"
    
    DATABASE_URL: str | None = None

    @property
    def sync_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    SYNC_TASKS: bool = False # Set to True to run tasks immediately without Redis
    
    # Zoho
    ZOHO_BOOKS_AUTHTOKEN: str
    ZOHO_ORG_ID: str
    
    # Blockchain
    POLYGON_RPC_URL: str
    PRIVATE_KEY: str
    CONTRACT_ADDRESS: str
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
