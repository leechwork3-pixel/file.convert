# 📚 Telegram eBook Converter Bot

A secure, Docker-ready Telegram bot to convert ebooks and documents into popular formats like PDF, EPUB, MOBI, AZW3, FB2, CBZ, and HTML.

---

## 🚀 Features

- ✅ Inline format selection (via buttons)
- ✅ Supports PDF, EPUB, MOBI, AZW3, CBZ, FB2, HTML, DOCX, RTF, TXT
- ✅ MongoDB logging for users & files
- ✅ Admin commands: ban/unban users, logs/stats
- ✅ Dashboard built with Flask Admin
- ✅ Docker & Koyeb/VPS deployable
- ✅ Prometheus Metrics (`/metrics`)

---

## 🧑 User Commands

| Command   | Description                     |
|-----------|---------------------------------|
| `/start`  | Start the bot                   |
| `/help`   | Show help and usage             |
| `/formats`| Show supported formats          |
| `/stats`  | Show total users & conversions  |

---

## 🔐 Admin Commands

| Command        | Description                         |
|----------------|-------------------------------------|
| `/ban <id>`    | Ban a user by Telegram ID           |
| `/unban <id>`  | Unban a user                        |
| `/users`       | Show recent users                   |
| `/log`         | Show recent file conversion logs    |

---

## 🛠 Deployment

### 1. Clone and configure
git clone https://your-repo-url.git
cd advanced_converter_bot
cp .env.example .env

Fill credentials
text

### 2. Using Docker
docker build -t ebook-bot .
docker run --env-file .env ebook-bot

text

### 3. Deploy on Koyeb
- Push to GitHub
- Create service from repo
- Configure environment variables
- Expose port 8080 if using Flask dashboard or metrics

---
## 📊 Monitoring
- Metrics exposed at `/metrics` via Prometheus
- Dashboard available at `dashboard/app.py`
  → Visit `http://localhost:8080/admin`

---

## 📂 Tests

Run test script:
python tests/test_script.py

text

Run Postman collection via:
newman run tests/advanced_converter_bot.postman_collection.json


What is the "Log Channel" function?
Purpose: It acts as a centralized place where the bot can send messages about its activity that you, as the bot owner/admin, want to track.

Typical Usage:

Logging new user join events (e.g., when a user starts the bot).

Logging file conversions done by users, including details like user info and file names.

Alerting about admin actions or errors if implemented.

For example, in your bot code, when a new user sends /start, the bot writes a message like:
👤 New user: @username (user_id)
to the log channel. Similarly, after converting an ebook file, the bot sends a message with details to the same channel.

Why use a log channel?
Monitoring: It helps you keep track of users interacting with the bot and actions performed without going through logs on the server.

Auditing: Keeps a record of conversions and admin commands, useful for moderation or analytics.

Debugging: Helps detect problems or suspicious behavior quickly.

How it works technically:
The log channel is identified by its chat ID or username, stored in your .env configuration as LOG_CHANNEL (e.g., -1001234567890).

Your bot uses Pyrogram’s send_message or send_document methods to send logs or files to this channel.

Summary:
The log channel function in your bot is a way to send real-time logs and notifications about usage and conversions to a designated Telegram channel, serving as an audit and monitoring tool for you as an admin.

Suppose your .env has:

text
LOG_CHANNEL=-1001234567890
Whenever a user starts the bot or converts a file, you will see messages show up in your log channel, sent by the bot.

Example: Logging a New User
When a user sends /start, your bot logs:

python
await app.send_message(
    LOG_CHANNEL,
    f"👤 New user: {message.from_user.mention} (`{message.from_user.id}`)"
)
What appears in your log channel:

text
👤 New user: @alex (12345678)
Example: Logging a File Conversion
After a successful file conversion, your bot logs:

python
await app.send_document(
    LOG_CHANNEL,
    document=output_path,
    caption=(
        f"📁 File Converted\n"
        f"👤 User: @{callback.from_user.username or 'N/A'} (`{callback.from_user.id}`)\n"
        f"📝 {doc.file_name} → {format.upper()}"
    )
)
What appears in your log channel:

text
[File Attachment: Book.pdf_converted.epub]
📁 File Converted
👤 User: @alex (12345678)
📝 Book.pdf → EPUB
Summary:
Every time a new user joins or anyone converts a file, you’ll get a message in your log channel (with files attached as needed). This gives you real-time visibility into user activity and bot usage, all inside Telegram.
