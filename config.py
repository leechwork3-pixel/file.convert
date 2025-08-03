import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("24171111"))
API_HASH = os.getenv("c850cb56b64b6c3b10ade9c28ef7966a")
BOT_TOKEN = os.getenv("7804274444:AAESKpYJQVhftykvv5cKZP2uyCYvxlwQvow")
LOG_CHANNEL = int(os.getenv("-1002585029413"))
MONGO_URI = os.getenv("mongodb+srv://Furina:furinafile@furinafile.tjrqfwh.mongodb.net/?retryWrites=true&w=majority&appName=Furinafile")
SUDO_ADMINS = list(map(int, os.getenv("SUDO_ADMINS", "1335306418").split()))

DOWNLOAD_DIR = "downloads"
MAX_FILE_SIZE_MB = 200
