import scrapy

class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()

class PropertyItem(scrapy.Item):
    id = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    price = scrapy.Field()
    mileage = scrapy.Field()
    fuel_type = scrapy.Field()
    location = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
