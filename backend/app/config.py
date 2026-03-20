from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    s3_bucket_name: str = ""

    model_runner_url: str = "http://model-runner.docker.internal/engines/llama.cpp/v1"
    model_name: str = "docker.io/ai/qwen2.5:latest"

    chroma_host: str = "chromadb"
    chroma_port: int = 8000

    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 500
    chunk_overlap: int = 50


settings = Settings()
