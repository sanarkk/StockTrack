# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BusinessInsiderItem(scrapy.Item):
    # define the fields for your item here like:
    index_key = scrapy.Field()
    title = scrapy.Field()
    publish_date = scrapy.Field()
    article_text = scrapy.Field()
    url = scrapy.Field()
    stock_ticker = scrapy.Field()
    news_source = scrapy.Field()
    parsing_date = scrapy.Field()
    