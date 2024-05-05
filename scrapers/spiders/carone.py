import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapers.items import CarItem


class CaroneSpider(CrawlSpider):
    name = "carone"
    custom_settings = {
        "USER_AGENT": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ),
        "FEEDS": {
            "carone_data.json": {"format": "json"},
        },
        "CLOSESPIDER_ITEMCOUNT": 30,
    }
    start_urls = [
        "https://carone.com.uy/autos-usados-y-0km",
    ]

    rules = (
        Rule(
            LinkExtractor(
                restrict_css=".carone-car-info-data a.link-primary",
                unique=True
            ),
            callback="parse_car"
        ),
    )

    def parse_car(self, response: scrapy.http.Response):
        car_url = response.url
        price = response.css('.price-container .price::text').get()

        yield CarItem(
            url=car_url,
            price=price,
            source="carone"
        )
