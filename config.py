import os
import sys
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

# --- Essential Configuration ---

# Telegram API credentials
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Telegram Bot Token from @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")

# --- Optional Configuration ---

# Log channel ID (must be an integer, starts with -100)
# Provide a default value of 0 if not set
LOG_CHANNEL_STR = os.getenv("LOG_CHANNEL", "0") 

# List of Sudo Admins (user IDs). Separate multiple IDs with a space.
# Example: "12345 67890"
SUDO_ADMINS_STR = os.getenv("SUDO_ADMINS", "")

# --- Application Settings ---

# Directory to store downloaded files
DOWNLOAD_DIR = "downloads"

# Maximum file size to handle in Megabytes (MB)
MAX_FILE_SIZE_MB = 200

# --- Data Validation and Type Conversion ---

# Validate essential variables
if not all([API_ID, API_HASH, BOT_TOKEN, MONGO_URI]):
    print("ERROR: One or more essential environment variables (API_ID, API_HASH, BOT_TOKEN, MONGO_URI) are missing.")
    print("Please check your .env file or deployment environment settings.")
    sys.exit(1) # Exit the application if critical info is missing

# Safely convert numeric variables
try:
    API_ID = int(API_ID)
    LOG_CHANNEL = int(LOG_CHANNEL_STR)
except (ValueError, TypeError):
    print(f"ERROR: API_ID ('{API_ID}') or LOG_CHANNEL ('{LOG_CHANNEL_STR}') is not a valid integer.")
    sys.exit(1)

# Safely convert list of admins
SUDO_ADMINS = [int(admin_id) for admin_id in SUDO_ADMINS_STR.split()] if SUDO_ADMINS_STR else []

