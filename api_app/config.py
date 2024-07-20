from pydantic_settings import BaseSettings


class SettingsDataBase(BaseSettings):
    postgres_host: str
    postgres_user: str
    postgres_db: str
    postgres_port: str
    postgres_password: str
    db_container_name: str
    echo_db: bool


db_settings: SettingsDataBase = SettingsDataBase()
