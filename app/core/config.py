from dotenv import load_dotenv
import os
load_dotenv()

class Settings:
    ENV: str = os.getenv("ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()

