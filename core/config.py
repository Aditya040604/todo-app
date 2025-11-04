from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    PROJECT_NAME: str
    API_VERSION: str
    DATABASE_URL: str
    ALGORITHM: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


settings = Config()