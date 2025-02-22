import scrapy
import subprocess
from NewsParser.items import BusinessInsiderItem
from dotenv import load_dotenv
import os
import sys
import boto3
from datetime import datetime

load_dotenv()

class BusinessinsiderSpider(scrapy.Spider):
    name = "deltaBusinessinsider"
    allowed_domains = ["markets.businessinsider.com"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the absolute path of parseProxies.py
        proxy_script_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../parseProxies.py")
        )
        self.logger.info(f"Using proxy script at: {proxy_script_path}")

        # Use Python from virtual environment
        python_executable = sys.executable
        self.logger.info(f"Using Python executable at: {python_executable}")

        # Run the script using the virtual environment
        subprocess.run([python_executable, proxy_script_path], check=True)

        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.getenv("AWS_REGION_NAME"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        self.table = self.dynamodb.Table('InsiderArticles')
        self.existing_titles = self.get_existing_titles()

    def get_existing_titles(self):
        """Fetch all article titles from DynamoDB to skip duplicates."""
        try:
            response = self.table.scan(ProjectionExpression='title')
            return {item['title'] for item in response.get('Items', [])}
        except Exception as e:
            self.logger.error(f"Error fetching existing titles: {e}")
            return set()

    def start_requests(self):
        """Only parse the first page for delta parsing."""
        yield scrapy.Request('https://markets.businessinsider.com/news?p=1', self.parse)

    def parse(self, response):
        """Parse articles on the first page and stop if an existing article is found."""
        for article in response.css('div.latest-news__story'):

            title = article.css('h3.latest-news__title a.latest-news__link::text').get()
            href = article.css('h3.latest-news__title a.latest-news__link::attr(href)').get()
            news_source = article.css('div.latest-news__meta span.latest-news__source::text').get()

            if title in self.existing_titles:
                self.logger.info(f"Skipping already scraped article: {title}")
                continue

            yield response.follow(href, self.parse_article, meta={'title': title, 'news_source': news_source})

    def parse_article(self, response):
        """Parse article details and yield only if it's newer than the last one in DynamoDB."""
        business_item = BusinessInsiderItem()

        business_item['title'] = response.meta['title']
        business_item['publish_date'] = response.css('span.news-post-quotetime::text').get()
        business_item['article_text'] = ' '.join(response.css('p::text').getall())
        business_item['url'] = response.url
        business_item['news_source'] = response.meta.get('news_source', 'Business Insider')

        stock_section = response.css('div.box.shares-in-news div.shares-in-news-container div.quote-container')
        
        if stock_section:
            business_item['stock_ticker'] = stock_section.css('div.col-xs-12.no-padding a::text').get()

        yield business_item
