import scrapy
from scrapers.items import CarItem
import re

class CarOneSpider(scrapy.Spider):
    name = 'carone'
    allowed_domains = ['carone.com.uy']
    
    def start_requests(self):
        max_pages = 60
        for page_number in range(1, max_pages + 1):
            url = f'https://carone.com.uy/autos-usados-y-0km?p={page_number}'
            yield scrapy.Request(url=url, callback=self.parse, meta={'page_number': page_number})

    def parse(self, response):
        # Obtener los enlaces de los autos
        car_links = response.css('a.link-primary::attr(href)').getall()
        
        # Verificar si no hay más autos
        if not car_links:
            self.logger.info(f"No se encontraron más autos en la página {response.meta['page_number']}. Terminando el scraping.")
            return
        
        for car_link in car_links:
            yield response.follow(car_link, callback=self.parse_car)

    def parse_car(self, response):
        car_id = response.url.split('/')[-1]
        
        # Obtener la URL base de la imagen
        base_image_url = response.css('.img-container-sm img::attr(src)').get()
        
        # Generar todas las URL de las imágenes de 0-0 a 0-25
        image_urls = [base_image_url.replace('0-0.jpg', f'0-{i}.jpg') for i in range(26)]
        
        car_item = CarItem(
            id=car_id,
            url=response.url,
            image_urls=image_urls,  # Agregar las URL de las imágenes al ítem
            price=response.css('span.price-wrapper span.price::text').get(),
            year=response.xpath('//p[contains(text(), "Año")]/preceding-sibling::p/text()').get(),
            kilometers=response.xpath('//p[contains(text(), "Kilómetros")]/preceding-sibling::p/text()').get(),
            engine=response.xpath('//p[contains(.,"Cilindrada")]/following-sibling::p/text()').get(),
            airbags=response.xpath('//p[contains(.,"Airbags")]/following-sibling::p/text()').get(),
            source="Concesionaria Car One"
        )

        yield car_item




