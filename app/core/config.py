import os
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, Field, RedisDsn, validator


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    PROJECT_NAME: str = Field(default="FastApi", description="Project Name")
    DEBUG: bool = Field(default=False, description="Debug Mode")

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl | str] = Field(
        default=["*"], description="CORS CONF ALLOWED_HOSTS"
    )
    CORS_ALLOWED_METHODS: List[AnyHttpUrl | str] = Field(
        default=["*"], description="CORS CONF ALLOWED_METHODS"
    )
    CORS_ALLOWED_HEADERS: List[AnyHttpUrl | str] = Field(
        default=["*"], description="CORS CONF ALLOWED_HEADERS"
    )

    DATABASE_DSN: Optional[str] = Field(
        default=f"sqlite:///{BASE_DIR}/database.db", description="Database URL"
    )
    REDIS_DSN: RedisDsn = Field(
        default="redis://user:pass@localhost:6379/1", description="Redis URL"
    )

    CHAT_GPT_ACCESS_TOKEN: str = Field(default="", description="Redis URL")

    @validator(
        "BACKEND_CORS_ORIGINS", "CORS_ALLOWED_METHODS", "CORS_ALLOWED_HEADERS", pre=True
    )
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env", "local.env", "test.env", "prod.env"
        env_file_encoding = "utf-8"


settings = Settings()
