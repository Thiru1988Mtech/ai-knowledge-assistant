from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_base_url: str = 'http://localhost:11434'
    llm_model: str = 'llama3.2'
    embed_model: str = 'nomic-embed-text'
    chroma_path: str = './chroma_db'
    collection_name: str = 'knowledge_base'
    top_k: int = 5
    temperature: float = 0.1
    max_tokens: int = 1000
    secret_key: str = 'change-this-in-production'
    app_name: str = 'AI Knowledge Assistant'
    version: str = '1.0.0'

    model_config = {
        "env_file": ".env"
    }

settings = Settings()