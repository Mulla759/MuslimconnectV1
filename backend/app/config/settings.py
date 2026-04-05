from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    app_name: str = Field(default="MuslimConnect API", validation_alias="APP_NAME")
    debug: bool = Field(default=False, validation_alias="APP_DEBUG")


settings = Settings()
