import scrapy
from scrapy.item import Item, Field

class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()

class CarItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    year = scrapy.Field()
    kilometers = scrapy.Field()
    source = scrapy.Field()
    engine = scrapy.Field()
    airbags = scrapy.Field()
    image_urls = scrapy.Field()
