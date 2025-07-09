"""
Application settings and logging configuration.
"""
import logging
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource
)


__all__ = ["settings", "logger",]

_CURRENT_DIR_ = Path(__file__).parent.resolve()
_SETTINGS_FILE_ = _CURRENT_DIR_ / "settings.yaml"

_MODELS_ = {
    "o4-mini",
    "gpt-4.1",
}


class Settings(BaseSettings):
    openai_api_key: Optional[str] = Field(..., description="API key for OpenAI. Do NOT set here. Must be provided by the `$KESTRABOT_OPENAI_API_KEY` environment variable.")
    openai_model: str = Field("o4-mini", description="Default OpenAI model to use for generating the Kestra Flow.")

    developer_prompt: str = Field(..., description="Developer prompt for the OpenAI agen to generate the Kestra Flow from the user input.")
    metadata: Optional[str] = Field(None, description="Additional Metadata for the Kestra Flow.")

    logging_level: str = Field("INFO", description="Python logging level for the application. Defaults to INFO.")

    model_config = SettingsConfigDict(
        env_prefix="KESTRABOT_",
        extra="ignore",

        yaml_file=[_SETTINGS_FILE_, "settings.yaml", "../settings.yaml", "settings.yml", "../settings.yml"],
        yaml_file_encoding="utf-8",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )

    @field_validator("logging_level", mode="before")
    def validate_logging_level(cls, value: str) -> str:
        """
        Validates the logging level to ensure it is a valid logging level.
        Converts the value to uppercase to match Python's logging module standards.
        If the provided value is not valid, returns the default "INFO" level.
        """
        if isinstance(value, str):
            value = value.upper()
            if value not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
                return "INFO"
        elif isinstance(value, int):
            # If an integer is provided, convert it to the corresponding logging level name
            value = logging.getLevelName(value)
            if not isinstance(value, str) or value not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
                return "INFO"
        else:
            return "INFO"
        return value
    
    @field_validator("openai_model", mode="before")
    def validate_openai_model(cls, value: str) -> str:
        """
        Validates the OpenAI model to ensure it is one of the supported models.
        If the provided value is not valid, returns the default "o4-mini" model.
        """
        if value not in _MODELS_:
            return "o4-mini"
        return value


def setup_logging(settings: Settings) -> logging.Logger:
    """
    Configures the Python logging module based on the settings.
    Sets up a logger with a formatter that includes timestamp, logger name,
    log level, and the message.
    """
    numeric_level = getattr(logging, settings.logging_level.upper(), None) or logging.INFO
    # Create and configure the logger
    logger = logging.getLogger("main")
    logger.setLevel(numeric_level)
    # Check if the logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)
        # Define a formatter with timestamp, logger name, log level, and message
        formatter = logging.Formatter("[%(levelname)-8s] [%(asctime)s] - %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.propagate = False

    return logger


# =======================================
# Module global variables
# Initialize settings and logger
# =======================================
settings: Settings = Settings()
logger: logging.Logger = setup_logging(settings)
