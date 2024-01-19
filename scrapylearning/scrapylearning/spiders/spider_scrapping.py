from typing import Any
from ..items import ScrapylearningItem
import scrapy
from scrapy.http import Response


class ScrapingSpider(scrapy.Spider):
    name = 'scraping'
    start_urls = [
        'https://gndec.ac.in/faculty/?deptt=21'
    ]

    def parse(self, response: Response, **kwargs: Any) -> Any:

        items = ScrapylearningItem()

        data = response.xpath('//table//tr')


        for row in data:
            name = row.xpath('td[1]/text()').extract()
            desigination = row.xpath('td[2]/text()').extract()
            email = row.xpath('td[3]/text()').extract()

            items['name'] = name
            items['desigination'] = desigination
            items['email'] = email

            yield items



        # yield {
        #     'data':div_quotes
        # }

