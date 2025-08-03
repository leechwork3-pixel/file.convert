from pyrogram import filters
from pyrogram.types import Message
from config import SUDO_ADMINS
from utils.database import ban_user, unban_user, get_recent_users, get_recent_files

def register(app):
    @app.on_message(filters.command("ban") & filters.user(SUDO_ADMINS))
    async def ban_cmd(_, msg: Message):
        try:
            user_id = int(msg.command[1])
            await ban_user(user_id)
            await msg.reply(f"✅ Banned {user_id}")
        except:
            await msg.reply("❌ Usage: /ban <user_id>")

    @app.on_message(filters.command("unban") & filters.user(SUDO_ADMINS))
    async def unban_cmd(_, msg: Message):
        try:
            user_id = int(msg.command[1])
            await unban_user(user_id)
            await msg.reply(f"✅ Unbanned {user_id}")
        except:
            await msg.reply("❌ Usage: /unban <user_id>")

    @app.on_message(filters.command("users") & filters.user(SUDO_ADMINS))
    async def users_cmd(_, msg: Message):
        users = await get_recent_users()
        text = "👥 Recent Users:\n"
        for u in users:
            text += f"- {u.get('name', 'N/A')} (@{u.get('username')}) – `{u['_id']}`\n"
        await msg.reply(text)

    @app.on_message(filters.command("log") & filters.user(SUDO_ADMINS))
    async def log_cmd(_, msg: Message):
        logs = await get_recent_files()
        text = "📄 Recent Conversions:\n"
        for f in logs:
            text += f"{f['file_name']} ➜ {f['format']} by `{f['user_id']}`\n"
        await msg.reply(text)
      
