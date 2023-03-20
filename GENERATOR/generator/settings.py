from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    General settings for the generator application
    """
    project_name: str = "IoT Device Messaege Generator"
    api_version: int = 1
    host: str = "0.0.0.0"
    port: int = 7000
    log_level: str = "debug"
    hot_reload: bool = True