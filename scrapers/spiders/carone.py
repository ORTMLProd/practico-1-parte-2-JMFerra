import scrapy
from scrapers.items import CarItem

class CarOneSpider(scrapy.Spider):
    name = 'carone'
    allowed_domains = ['carone.com.uy']
    
    def start_requests(self):
        page_number = 1
        while True:
            url = f'https://carone.com.uy/autos-usados-y-0km?p={page_number}'
            yield scrapy.Request(url=url, callback=self.parse)
            page_number += 1

    def parse(self, response):
        # Obtener los enlaces de los autos
        cars = response.xpath('//a[@class="link-primary"]/@href').getall()
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
            engine=response.xpath('//p[contains(.,"Cilindrada")]/following-sibling::p/text()').get(),
            airbags=response.xpath('//p[contains(.,"Airbags")]/following-sibling::p/text()').get(),
            transmission=response.xpath('//p[contains(.,"Transmisión")]/following-sibling::p/text()').get(),
            source="Concesionaria Car One"
        )
        
        # Extraer enlaces de las imágenes
        image_urls = response.css('div#drawer-background::attr(style)').re(r'url\((.*?)\)')
        image_urls = [url.strip('url("').strip('")') for url in image_urls if url.startswith("http")]
        
        car_item['image_urls'] = image_urls
        
        yield car_item









