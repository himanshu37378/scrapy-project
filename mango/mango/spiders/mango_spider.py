import scrapy


class MangoSpiderSpider(scrapy.Spider):
    name = "mango_spider"
    allowed_domains = ["shop.mango.com"]
    start_urls = ["https://shop.mango.com"]

    def parse(self, response):
        pass
