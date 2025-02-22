import boto3
from config import (
    USERS_TABLE,
    AWS_REGION,
    AWS_ACCESS_KEY,
    AWS_SECRET_ACCESS_KEY,
    TICKERS_TABLE,
    ARTICLES_TABLE,
    PROCESSED_ARTICLES_TABLE,
    TICKER_PRICES_TABLE,
)

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

users_table = dynamodb.Table(USERS_TABLE)
stock_tickers_name = dynamodb.Table(TICKERS_TABLE)
articles_table = dynamodb.Table(ARTICLES_TABLE)
processed_table = dynamodb.Table(PROCESSED_ARTICLES_TABLE)
ticker_prices_table = dynamodb.Table(TICKER_PRICES_TABLE)
