from typing import Any
from ..items import ScrapylearningItem
import scrapy
from scrapy.http import Response


class ScrapingSpider(scrapy.Spider):
    name = 'data'
    page_number = 2
    start_urls = [
        'https://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response: Response, **kwargs: Any) -> Any:
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

        next_page = 'https://quotes.toscrape.com/page/' + str(ScrapingSpider.page_number) + '/'
        print(next_page)
        if ScrapingSpider.page_number < 11:
            ScrapingSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

