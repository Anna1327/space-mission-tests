import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Settings:
    def __init__(self):
        self.config = {key: os.getenv(key) for key in os.environ.keys() if not key.startswith("_")}

    def get(self, key, default=None):
        return self.config.get(key, default)


settings = Settings()
