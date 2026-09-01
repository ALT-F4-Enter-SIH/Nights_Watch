from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "ShadowLink AI"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True
    database_url: str = "sqlite:///./data/shadowlink.db"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    host: str = "0.0.0.0"
    port: int = 8000
    secret_key: str = "change-me-in-production"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def project_root(self) -> Path:
        return Path(__file__).parent.parent

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
