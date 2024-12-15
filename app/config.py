# app/config.py
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://dana:zHRpKUSzGoGAFOUP045a58U9meC4LvgN@dpg-ctfc7l1u0jms739l85i0-a.oregon-postgres.render.com/aviasalesforbitches"')
AVIASALES_API_KEY = os.getenv('AVIASALES_API_KEY', 'your_aviasales_api_key')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '6468969844:AAFWL2e_swHkKYQjS3BWO_TF9V-cGZ4n_ck')
USER_MAP_FILE = os.getenv('USER_MAP_FILE', 'user_map.txt')