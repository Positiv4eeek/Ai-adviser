from pydantic_settings import BaseSettings
from pydantic import Field
from sqlalchemy.engine import url as sa_url

class DBConfig(BaseSettings):
    DATABASE_URL: str = Field(alias="DATABASE_URL")
    POSTGRES_SUPERUSER_URL: str | None = Field(default=None, alias="POSTGRES_SUPERUSER_URL")
    APP_SCHEMA: str = Field(default="public", alias="APP_SCHEMA")

    class Config:
        env_file = ".env"
        extra = "ignore"

    def app_url(self) -> str:
        return self.DATABASE_URL

    def postgres_super_url(self) -> str | None:
        return self.POSTGRES_SUPERUSER_URL

    def parts(self):
        u = sa_url.make_url(self.DATABASE_URL)
        return {
            "user": u.username,
            "password": u.password or "",
            "host": u.host or "localhost",
            "port": u.port or 5432,
            "db": u.database,
            "drivername": u.drivername,
        }
