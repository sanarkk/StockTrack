import boto3
import pandas as pd
import yfinance as yf
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from decimal import Decimal

# Load environment variables
load_dotenv()

# AWS DynamoDB Configuration
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv("AWS_REGION_NAME"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

# Define tables
tickers_table = dynamodb.Table('StockTickers')
prices_table = dynamodb.Table('StockPrices')

# Fetch tickers from DynamoDB
response = tickers_table.scan()
tickers = [item['ticker'] for item in response['Items']][:10]

# Fetch historical stock prices using yfinance
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

# Function to save to DynamoDB
def save_to_dynamodb(df, ticker):
    for index, row in df.iterrows():
        prices_table.put_item(
            Item={
                'ticker': ticker,
                'date': row.name.strftime('%Y-%m-%d'),
                'open': Decimal(str(row['Open'].item())) if pd.notna(row['Open'].item()) else Decimal('0'),
                'high': Decimal(str(row['High'].item())) if pd.notna(row['High'].item()) else Decimal('0'),
                'low': Decimal(str(row['Low'].item())) if pd.notna(row['Low'].item()) else Decimal('0'),
                'close': Decimal(str(row['Close'].item())) if pd.notna(row['Close'].item()) else Decimal('0'),
                'volume': int(row['Volume'].item()) if pd.notna(row['Volume'].item()) else 0
            }
        )

# Process each ticker
for ticker in tickers:
    print(f"Fetching data for {ticker}")
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
    if not df.empty:
        save_to_dynamodb(df, ticker)
        print(f"Saved data for {ticker}")
    else:
        print(f"No data found for {ticker}")

print("Stock prices data saved to DynamoDB.")
