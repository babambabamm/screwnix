import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BLOCK_MODE = os.getenv("BLOCK_MODE") == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")