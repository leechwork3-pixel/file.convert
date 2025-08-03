import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))
MONGO_URI = os.getenv("MONGO_URI")
SUDO_ADMINS = list(map(int, os.getenv("SUDO_ADMINS", "").split()))

DOWNLOAD_DIR = "downloads"
MAX_FILE_SIZE_MB = 200
