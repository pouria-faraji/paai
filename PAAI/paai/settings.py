from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    General settings for the application
    """
    project_name: str = "PAAI - Programming Assignment AI"
    api_version: int = 1
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "debug"
    hot_reload: bool = True