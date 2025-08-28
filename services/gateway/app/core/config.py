from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr"
    api_key_secret: str = "myverysecureapikey123"
    agent_service_url: str = "http://agent:9000"

settings = Settings()
