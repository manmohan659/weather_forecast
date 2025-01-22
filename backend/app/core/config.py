from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    WEATHER_API_KEY: str = "b4396ce9a2e64262a00220130252201"

    class Config:
        env_file = ".env"

settings = Settings()