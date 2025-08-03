import os
import re
from pathlib import Path
from werkzeug.utils import secure_filename as werkzeug_secure_filename
from config import DOWNLOAD_DIR, MAX_FILE_SIZE_MB

ALLOWED_EXTENSIONS = {
    '.epub', '.pdf', '.mobi', '.azw3', '.fb2', '.cbz',
    '.html', '.htm', '.txt', '.docx', '.rtf'
}

def is_allowed_file(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def is_size_allowed(size_bytes):
    return (size_bytes / (1024 ** 2)) <= MAX_FILE_SIZE_MB

def secure_filename(filename):
    name = werkzeug_secure_filename(filename)
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    return name[:255]

def get_download_path(filename):
    return os.path.join(DOWNLOAD_DIR, secure_filename(filename))

