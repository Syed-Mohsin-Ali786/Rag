from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openrouter_api_key: str
    embedding_model: str
    chat_model: str
    qdrant_path: str = "./qdrant_data"
    collection_name: str = "documents"

    class Config:
        env_file = ".env"

settings = Settings()