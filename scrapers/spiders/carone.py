import scrapy
from scrapers.items import CarItem

class CarOneSpider(scrapy.Spider):
    name = 'carone'
    allowed_domains = ['carone.com.uy']
    
    def start_requests(self):
        for page_number in range(1, 51):
            url = f'https://carone.com.uy/autos-usados-y-0km?p={page_number}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Obtener los enlaces de los autos
        cars = response.xpath('//a[@class="link-primary"]/@href').getall()
        if not cars:
            self.logger.info(f"No se encontraron más autos en la página: {response.url}")
            return
        
        for car_link in cars:
            yield response.follow(car_link, callback=self.parse_car)

    def parse_car(self, response):
        car_id = response.url.split('/')[-1]
        car_item = CarItem(
            id=car_id,
            url=response.url,
            price=response.css('span.price-wrapper span.price::text').get(),
            year=response.xpath('//p[contains(text(), "Año")]/preceding-sibling::p/text()').get(),
            kilometers=response.xpath('//p[contains(text(), "Kilómetros")]/preceding-sibling::p/text()').get(),
            source="Concesionaria Car One"
        )
        yield car_item
