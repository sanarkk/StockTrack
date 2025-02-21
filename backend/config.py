import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
USERS_TABLE = os.getenv("USERS_TABLE", "users")
POSTS_TABLE = os.getenv("POSTS_TABLE", "posts")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AWS_REGION = os.getenv("AWS_REGION", "")
SECRET_KEY = os.getenv("SECRET_KEY", "default_key")
ALGORITHM = os.getenv("ALGORITHM", "default_algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = 120
