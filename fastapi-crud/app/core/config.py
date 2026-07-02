from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://myuser:mypassword@localhost:5432/mydb"
    app_name: str = "FastAPI CRUD"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
