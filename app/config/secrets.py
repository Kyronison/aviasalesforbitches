import os
from dotenv import load_dotenv

load_dotenv()

class Secrets:
    @staticmethod
    def get_secret(key: str, default=None):
        return os.getenv(key, default)