from pyrogram import filters
from pyrogram.types import Message
from config import LOG_CHANNEL, SUDO_ADMINS
from utils.database import (
    log_user, is_banned,
    get_total_users, get_total_files,
    get_recent_files, get_recent_users
)

def register(app):
    @app.on_message(filters.command("start"))
    async def start(_, msg: Message):
        if await is_banned(msg.from_user.id):
            return await msg.reply("🚫 You are banned.")
        await log_user(msg.from_user)
        await app.send_message(LOG_CHANNEL, f"👤 New user: {msg.from_user.mention} (`{msg.from_user.id}`)")
        await msg.reply("👋 Welcome! Send me a file to convert.")

    @app.on_message(filters.command("help"))
    async def help_cmd(_, msg: Message):
        await msg.reply(
            "**📢 Commands**\n\n"
            "👤 /start - Start bot\n"
            "💬 /help - Show help\n"
            "📊 /stats - Show total users and conversions\n"
            "📁 /formats - List supported output formats\n\n"
            "👮 Admin Only:\n"
            "/ban <user_id>\n/unban <user_id>\n/users\n/log"
        )

    @app.on_message(filters.command("stats"))
    async def stats(_, msg: Message):
        users = await get_total_users()
        files = await get_total_files()
        await msg.reply(f"📊 Stats:\n👤 Total Users: `{users}`\n📄 Files Converted: `{files}`")

    @app.on_message(filters.command("formats"))
    async def formats(_, msg: Message):
        await msg.reply("🧾 Supported formats:\nPDF, EPUB, MOBI, AZW3, CBZ, FB2, HTML, DOCX, RTF, TXT")
      
