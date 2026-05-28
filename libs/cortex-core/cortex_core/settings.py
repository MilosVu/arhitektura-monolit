from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+psycopg://cortex:cortex@localhost:5432/cortex"
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "amqp://cortex:cortex@localhost:5672//"
    celery_result_backend: str = "redis://localhost:6379/1"
    jwt_secret: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    weaviate_url: str = "http://localhost:8080"
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "cortex123"
    rabbitmq_management_url: str = "http://localhost:15672"


def get_settings() -> Settings:
    return Settings()
