from pyrogram import Client
import handlers.general as general
import handlers.admin as admin
import handlers.converter as converter
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("converter_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

general.register(app)
admin.register(app)
converter.register(app)

app.run()
