from dotenv import load_dotenv
import os
load_dotenv()

class Settings:
    ENV: str = os.getenv("ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()

from datetime import time

WORK_START_TIME = time(9, 0)   # 09:00
WORK_END_TIME = time(17, 0)    # 17:00
SLOT_DURATION_MINUTES = 30