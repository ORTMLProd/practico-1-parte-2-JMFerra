from typing import Iterator

from requests.utils import requote_uri
from scrapy import signals
from scrapy.http.response.html import HtmlResponse
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
                restrict_css=".resultados .h-product .h-product-content a",
                unique=True
            ),
            callback="parse_car"
        ),
    )

    def parse_car(self, response: HtmlResponse) -> Iterator[dict]:
        def get_with_css(query: str) -> str:
            return response.css(query).get(default="").strip()

        car_id = get_with_css(".id-ficha::text")
        brand = get_with_css(".marca-ficha::text")
        model = get_with_css(".modelo-ficha::text")
        year = get_with_css(".anio-ficha::text")
        price = get_with_css(".precio-ficha::text")
        mileage = get_with_css(".kilometraje-ficha::text")
        fuel_type = get_with_css(".combustible-ficha::text")
        location = get_with_css(".localizacion-ficha::text")
        url = requote_uri(response.request.url)

        car = {
            "id": car_id,
            "brand": brand,
            "model": model,
            "year": year,
            "price": price,
            "mileage": mileage,
            "fuel_type": fuel_type,
            "location": location,
            "url": url,
            "source": "carone",
        }
        yield CarItem(**car)
