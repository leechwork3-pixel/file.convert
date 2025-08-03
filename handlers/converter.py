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
        buttons = [
            [InlineKeyboardButton(fmt, callback_data=f"convert:{fmt}")]
            for fmt in formats
        ]
        await message.reply(
            "📤 *Select the format you want to convert to:*",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="Markdown"
        )

    @app.on_callback_query(filters.regex("^convert:"))
    async def conversion_callback(_, call: CallbackQuery):
        fmt = call.data.split(":")[1].lower()
        uid = call.from_user.id

        if uid not in sessions:
            return await call.message.edit_text(
                "❗Session expired, please upload the file again."
            )

        doc = sessions.pop(uid)
        raw_name = secure_filename(doc.file_name)
        input_path = get_download_path(raw_name)
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}_converted.{fmt}"

        await call.message.edit_text("⚙️ Converting your file, please wait...")

        try:
            await app.download_media(doc, input_path)

            proc = await asyncio.create_subprocess_exec(
                "ebook-convert", input_path, output_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=300)

            # Check conversion success
            if proc.returncode != 0 or not os.path.exists(output_path):
                error_log = stderr.decode("utf-8").strip() if stderr else "Unknown error"
                await call.message.edit_text(
                    f"❌ *Conversion failed!*\n\n"
                    f"``````",
                    parse_mode="Markdown"
                )
                return

            # Success! Send converted file to user
            await call.message.reply_document(
                output_path,
                caption=(
                    f"✅ *Conversion Successful!*\n\n"
                    f"*File:* `{os.path.basename(output_path)}`\n"
                    f"*Format:* `{fmt.upper()}`"
                ),
                parse_mode="Markdown"
            )

            # Log to MongoDB
            await log_file(uid, os.path.basename(output_path), fmt.upper())

            # Send to LOG_CHANNEL
            await app.send_document(
                LOG_CHANNEL,
                document=output_path,
                caption=(
                    f"📁 *File Converted*\n"
                    f"👤 *User:* @{call.from_user.username or 'N/A'} (`{uid}`)\n"
                    f"📝 *Original:* `{doc.file_name}`\n"
                    f"📤 *Converted To:* `{fmt.upper()}`"
                ),
                parse_mode="Markdown"
            )

        except asyncio.TimeoutError:
            await call.message.edit_text("❌ Conversion timeout. Please try a smaller file.")
        except Exception as e:
            await call.message.edit_text(
                f"❌ *An error occurred:*\n``````",
                parse_mode="Markdown"
            )
        finally:
            # Cleanup any leftover files
            for path in [input_path, output_path]:
                try:
                    if os.path.exists(path):
                        os.remove(path)
                except Exception:
                    pass
                    
