import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
USERS_TABLE = os.getenv("USERS_TABLE", "users")
TICKERS_TABLE = os.getenv("TICKERS_TABLE", "tickers")
ARTICLES_TABLE = os.getenv("PARSED_NEWS_TABLE", "parsed_news")
PROCESSED_ARTICLES_TABLE = os.getenv("PROCESSED_TABLE", "parsed_news")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AWS_REGION = os.getenv("AWS_REGION", "")
SECRET_KEY = os.getenv("SECRET_KEY", "default_key")
ALGORITHM = os.getenv("ALGORITHM", "default_algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = 120
