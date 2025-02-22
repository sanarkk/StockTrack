# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import boto3
from botocore.exceptions import ClientError
import logging
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import yfinance as yf
from decimal import Decimal
import requests

load_dotenv()

class DynamoDBPipeline:
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.getenv("AWS_REGION_NAME"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self.table = self.dynamodb.Table('InsiderArticles')

    def get_next_index_key(self):
        """Generate the next sequential index key."""
        try:
            response = self.table.scan(ProjectionExpression="index_key", ConsistentRead = True)
            index_keys = [int(item['index_key']) for item in response.get('Items', []) if item.get('index_key')]

            return max(index_keys) + 1 if index_keys else 1
        except Exception as e:
            logging.error(f"Error fetching index keys: {e}")
            return 1

    def process_item(self, item, spider):
        try:
            item['parsing_date'] = datetime.utcnow().isoformat()
            item['index_key'] = str(self.get_next_index_key())

            self.table.put_item(
                Item={
                    'url': item.get('url'),
                    'title': item.get('title'),
                    'publish_date': item.get('publish_date'),
                    'article_text': item.get('article_text'),
                    'stock_ticker': item.get('stock_ticker'),
                    'news_source': item.get('news_source'),
                    'index_key': item.get('index_key'),
                    'parsing_date': item.get('parsing_date')
                }
            )

            #requests.post("http://localhost:8001/send_message", payload)

            spider.logger.info(f"Article saved to DynamoDB: {item.get('url')}")
        except ClientError as e:
            spider.logger.error(f"Failed to save article: {e}")
        return item


class ProcessDatePipeline:
    def process_item(self, item, spider):

        date_str = item.get("publish_date")

        if date_str:
            try:
                item['publish_date'] = datetime.strptime(date_str, '%b. %d, %Y, %I:%M %p').isoformat()
            
            except ValueError as e:
                spider.logger.error(f"Date parsing failed for {date_str}: {e}")
            
        return item

class StockTablePipeline:
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.getenv("AWS_REGION_NAME"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self.table = self.dynamodb.Table('StockTickers')

    def get_stock_name(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            return stock.info.get('longName', None)
        except Exception as e:
            logging.error(f"Error fetching stock name for {ticker}: {e}")
            return None

    def get_current_stock_price(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            current_price = stock.history(period="1d")['Close'].iloc[-1]
            return Decimal(str(current_price))
        except Exception as e:
            logging.error(f"Error fetching current stock price for {ticker}: {e}")
            return None

    def get_day_ago_stock_price(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            day_ago_price = stock.history(period="2d")['Close'].iloc[0]
            return Decimal(str(day_ago_price))
        except Exception as e:
            logging.error(f"Error fetching day-ago stock price for {ticker}: {e}")
            return None

    def process_item(self, item, spider):
        ticker = item.get('stock_ticker')
        stock_name = self.get_stock_name(ticker)
        current_price = self.get_current_stock_price(ticker)
        day_ago_price = self.get_day_ago_stock_price(ticker)

        if ticker and stock_name and current_price is not None:
            try:
                response = self.table.update_item(
                    Key={"ticker": ticker},
                    UpdateExpression="SET #count = if_not_exists(#count, :start) + :increment, #name = :name, #current_price = :current_price, #day_ago_price = :day_ago_price",
                    ExpressionAttributeNames={
                        "#count": "count",
                        "#name": "stock_name",
                        "#current_price": "current_price",
                        "#day_ago_price": "day_ago_price"
                    },
                    ExpressionAttributeValues={
                        ":increment": Decimal('1'),
                        ":start": Decimal('0'),
                        ":name": stock_name,
                        ":current_price": current_price,
                        ":day_ago_price": day_ago_price if day_ago_price is not None else None
                    },
                    ReturnValues="UPDATED_NEW",
                )
                spider.logger.info(f"Updated stock: {ticker}, Count: {response['Attributes']['count']}, Current Price: {current_price}, Day Ago Price: {day_ago_price}")
            except ClientError as e:
                spider.logger.error(f"Error updating DynamoDB: {e}")

        return item
    
# class TriggerTgBotPipeline:
#     def process_item(self, item, spider):
#         try:
#             payload = {
#                 "url": item["url"],
#                 "title": item["title"],
#                 "publish_date": item["publish_date"],
#                 "article_text": item["article_text"],
#                 "stock_ticker": item["stock_ticker"],
#                 "news_source": item["news_source"],
#                 "index_key": item["index_key"],
#                 "parsing_date": item["parsing_date"]
#             }

#             #requests.post("http://localhost:8001/send_message", payload)
#         except Exception as e:
#             logging.error(f"Error sending the requst to Tg bot: {e}")

#         return item