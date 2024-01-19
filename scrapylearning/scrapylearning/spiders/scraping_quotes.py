from typing import Any
from ..items import ScrapylearningItem
import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.http import Response, FormRequest
from ..items import ScrapylearningItem


class ScrapingSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/login'
    ]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        token = response.xpath('//form//input/@value').extract_first()
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': 'himanshu',
            'password': 'rerkokm'

        }, callback=self.start_scraping)

    def start_scraping(self, response):
        open_in_browser(response)
        items = ScrapylearningItem()

        data = response.xpath('//div[@class="quote"]')

        for row in data:
            title = row.xpath('.//span[@class="text"]/text()').extract()
            author = row.xpath('.//span//small[@class="author"]/text()').extract()
            tag = row.xpath('.//a[@class="tag"]/text()').extract()

            items['title'] = title
            items['author'] = author
            items['tag'] = tag

            yield items

