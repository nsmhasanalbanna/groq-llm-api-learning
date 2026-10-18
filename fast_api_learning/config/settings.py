from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key : str
    groq_model : str
    voyage_api_key: str
    post_gres_password : str
    post_gres_host : str
    post_gres_user : str
    post_gres_dbname : str
    post_gres_port : int
    flight_api_key : str
    geo_api_key : str
    jwt_secret_key: str
    jwt_algorithm: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

    