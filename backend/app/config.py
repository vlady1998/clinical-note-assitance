import os

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    asyncpg_url: PostgresDsn = os.getenv("SQL_URL")
    hugging_face_access_token: str = os.getenv("HUGGINGFACE_ACCESS_TOKEN")
    langfuse_secret_key: str = os.getenv("LANGFUSE_SECRET_KEY")
    langfuse_public_key: str = os.getenv("LANGFUSE_PUBLIC_KEY")
    langfuse_host: str = os.getenv("LANGFUSE_HOST")

settings = Settings()
