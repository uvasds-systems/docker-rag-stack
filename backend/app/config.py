from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    s3_bucket_name: str = ""

    model_runner_url: str = "https://open-webui.rc.virginia.edu/api/"
    model_name: str = "Kimi K2.5"
    uvarc_llm_token: str = ""

    chroma_host: str = "chromadb"
    chroma_port: int = 8000

    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 500
    chunk_overlap: int = 50


settings = Settings()
