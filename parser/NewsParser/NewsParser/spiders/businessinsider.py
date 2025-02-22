import scrapy
import subprocess
from NewsParser.items import BusinessInsiderItem
import os
import sys

class BusinessinsiderSpider(scrapy.Spider):
    name = "businessinsider"
    allowed_domains = ["markets.businessinsider.com"]
    page_number = 1
    
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

    def start_requests(self):
        yield scrapy.Request(f'https://markets.businessinsider.com/news?p={self.page_number}&', self.parse)

    def parse(self, response):
        for article in response.css('div.latest-news__story'):
            title = article.css('h3.latest-news__title a.latest-news__link::text').get()
            href = article.css('h3.latest-news__title a.latest-news__link::attr(href)').get()
            news_source = article.css('div.latest-news__meta span.latest-news__source::text').get()
            yield response.follow(href, self.parse_article, meta={'title': title, 'news_source': news_source})

        self.page_number += 1
        yield scrapy.Request(f'https://markets.businessinsider.com/news?p={self.page_number}&', self.parse)

    def parse_article(self, response):

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
