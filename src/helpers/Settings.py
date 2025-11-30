from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    IMAGE_SIZE:int
    CONFIDENCE_THRESHOLD:float
    IOU_THRESHOLD:float
    ALLOWED_IMAGE_TYPES :list[str]
    
    
    class Config:
        case_sensitive=True
        env_file = ".env"
        
        
get_settings=Settings()