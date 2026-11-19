from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator


class Settings(BaseSettings):
    APP_NAME: str = "TVET e-ASSESS"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_STORAGE_BUCKET: str = "evidence-files"
    SUPABASE_DB_URL: str

    ALLOWED_ORIGINS: Union[str, List[str]] = ["http://localhost:5173"]

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 480

    MAX_FILE_SIZE_MB: int = 100
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
    ALLOWED_VIDEO_TYPES: List[str] = ["video/mp4", "video/quicktime", "video/webm"]
    ALLOWED_AUDIO_TYPES: List[str] = ["audio/mpeg", "audio/wav", "audio/mp4", "audio/x-m4a"]
    ALLOWED_DOC_TYPES: List[str] = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value):
        # Handle None or empty string
        if value is None or value == "":
            return ["http://localhost:5173"]
        # Handle string (comma-separated)
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        # Handle list (already parsed)
        if isinstance(value, list):
            return value
        # Fallback
        return ["http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
