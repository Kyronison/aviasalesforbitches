# app/config.py
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')
AVIASALES_API_KEY = os.getenv('AVIASALES_API_KEY', 'your_aviasales_api_key')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'your_telegram_bot_token')
USER_MAP_FILE = os.getenv('USER_MAP_FILE', 'your_user_map_file')