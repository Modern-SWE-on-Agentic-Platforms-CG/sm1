from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from urllib.parse import quote_plus


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "smarthiremain001"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""

    # JWT
    JWT_SECRET: str = "change-me-to-a-strong-random-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 480

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:8016,http://127.0.0.1:5173,http://127.0.0.1:8016"

    # File storage
    UPLOAD_DIR: str = "backend/uploads"

    # SMTP
    SMTP_ENABLED: bool = False
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_FROM: str = "noreply@smartrecruit.local"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{quote_plus(self.DB_USER)}:{quote_plus(self.DB_PASSWORD)}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        # Always include loopback origins for local dev/demo stability.
        configured = [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        required_local = [
            "http://localhost:5173",
            "http://localhost:8016",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:8016",
        ]

        origins: list[str] = []
        for origin in configured + required_local:
            if origin not in origins:
                origins.append(origin)

        return origins


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
