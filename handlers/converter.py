import os
import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import LOG_CHANNEL, DOWNLOAD_DIR
from utils.files import is_allowed_file, is_size_allowed, secure_filename, get_download_path
from utils.database import log_file

formats = ["PDF", "EPUB", "MOBI", "AZW3", "CBZ", "FB2"]
sessions = {}

def register(app):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    @app.on_message(filters.document)
    async def handle_doc(_, message: Message):
        doc = message.document

        if not is_size_allowed(doc.file_size):
            return await message.reply("❌ Max file size is 200MB.")
        if not is_allowed_file(doc.file_name):
            return await message.reply("❌ Unsupported file type.")

        sessions[message.from_user.id] = doc
        buttons = [[InlineKeyboardButton(fmt, callback_data=f"convert:{fmt}")] for fmt in formats]
        await message.reply("Select output format:", reply_markup=InlineKeyboardMarkup(buttons))

    @app.on_callback_query(filters.regex("^convert:"))
    async def conversion_callback(_, call: CallbackQuery):
        fmt = call.data.split(":")[1].lower()
        uid = call.from_user.id

        if uid not in sessions:
            return await call.message.edit_text("❗Session expired. Please re-upload.")

        doc = sessions.pop(uid)
        raw_name = secure_filename(doc.file_name)
        input_path = get_download_path(raw_name)
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}_converted.{fmt}"

        await call.message.edit_text("⚙️ Converting... please wait.")

        try:
            await app.download_media(doc, input_path)

            proc = await asyncio.create_subprocess_exec(
                "ebook-convert", input_path, output_path,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await asyncio.wait_for(proc.communicate(), timeout=300)

            if not os.path.exists(output_path):
                raise Exception("Conversion failed.")

            await call.message.reply_document(output_path)
            await log_file(uid, os.path.basename(output_path), fmt.upper())

            await app.send_document(
                LOG_CHANNEL,
                document=output_path,
                caption=f"📁 Converted by @{call.from_user.username or 'N/A'} (`{uid}`)\n{doc.file_name} → {fmt.upper()}"
            )

        except asyncio.TimeoutError:
            await call.message.edit_text("❌ Conversion timeout.")
        except Exception:
            await call.message.edit_text("❌ Conversion failed.")
        finally:
            for path in [input_path, output_path]:
                if os.path.exists(path):
                    os.remove(path)
