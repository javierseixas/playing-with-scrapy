# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'real_estate'
    valuee = 0

    def start_requests(self):
        urls = [
            'https://www.portalinmobiliario.com/venta/casa/puerto-varas-los-lagos?tp=1&op=2&ca=3&ts=1&dd=3&dh=6&bd=2&bh=6&or=&mn=1&sf=1&sp=0&pd=500.000&pi=n4ogqeir3y4tqo2rfecxd0xb'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for title in response.css('.product-item-summary h4'):
            self.save(response)
            yield {'title': title.css('a ::text').extract_first()}

        for next_page in response.css('#PaginacionInferior .siguiente a'):
            yield response.follow(next_page, self.parse)

    def save(self, response):
        self.valuee += 1
        filename = 'quotes-%s.html' % self.valuee
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
