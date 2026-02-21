from dotenv import load_dotenv
import os
load_dotenv()

class Settings:
    ENV: str = os.getenv("ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
settings = Settings()

from datetime import time

WORK_START_TIME = time(9, 0)   
WORK_END_TIME = time(17, 0)    
SLOT_DURATION_MINUTES = 30