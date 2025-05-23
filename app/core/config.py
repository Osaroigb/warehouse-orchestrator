import logging
from dotenv import load_dotenv
from colorlog import ColoredFormatter
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables
load_dotenv()

# Settings class using Pydantic
class AppSettings(BaseSettings):
    app_name: str
    app_host: str
    app_port: int
    database_url: str
    redis_url: str
    erp_api_key: str
    erp_api_secret: str
    erp_base_url: str

    model_config = SettingsConfigDict(env_file=".env") 


# Logging setup
formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
    },
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[handler])


# Instance to use across app
settings = AppSettings()