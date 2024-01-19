import re
from urllib.parse import urljoin
import scrapy
from scrapy import Selector

from ..items import BoggiMilanoItem


class BoogiSpiderSpider(scrapy.Spider):
    name = "boogi_spider"
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

    def start_requests(self):
        urls = "https://www.boggi.com/en_IN/clothing/jeans/"

        yield scrapy.Request(url=urls, headers=self.header, callback=self.category_parser,
                             meta={'first_hit': True, 'current_page': 1})

    def category_parser(self, response):
        selector = Selector(text=response.text)
        first_hit = response.meta.get("first_hit", True)
        current_page = response.meta.get("current_page", 1)
        if first_hit:
            total_count_str = selector.xpath('//small/text()').extract_first()
            # total_count = int(''.join(char for char in total_count_str if char.isdigit()))
            total_count = 16
            page_size = 12
            # number_of_pages = int(total_count / page_size)
            number_of_pages = 2
            # print(total_count)
            for pages in range(current_page, number_of_pages):
                # next_page = f'?start={12}&sz=12'
                next_page_url = selector.xpath('//a[contains(@class,"page-switcher next")]/@href').extract_first()
                yield scrapy.Request(url=next_page_url, headers=self.header, callback=self.category_parser,
                                     meta={'first_hit': False, 'current_page': f"{pages}"})

        jeans = selector.xpath(
            '//div[contains(@class,"product-image")]/a[contains(@class,"product-image-render")]/@href').extract()
        for jean in jeans:
            jeans_url = jean
            # print(jeans_url)
            yield scrapy.Request(url=jeans_url, headers=self.header, callback=self.product_parser)

    def product_parser(self, response, ):

        selector = Selector(text=response.text)
        items = BoggiMilanoItem()

        name_str = selector.xpath('//h1[contains(@class,"h4 product-name")]/text()').extract_first()
        name = name_str.replace("\n","").strip()
        breadcrumbs_list = [bread.replace("\n","").strip() for bread in selector.xpath('//div[contains(@class, "breadcrumb-group")]/ul/li/a/text()').extract()]
        # color = selector.xpath('//span[contains(@class,"h6")]/span').extract_first()
        # color = selector.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "h6", " " ))]//span').extract_first()
        color = selector.xpath('//li[@class = "selectable selected"]/a[@class = "swatchanchor swatches-color"]/img/@alt').extract_first()
        description_value = selector.xpath("//div[@class = 'content'][1]//div[contains(@style, 'width:125%;text-align:justify;')]/text()").extract()
        description = "".join(description_value)
        feature_image = selector.xpath('//img[contains(@class, "product-image-hero")]/@src').extract_first()
        mrp_value = selector.xpath('//span[contains(@class,"product-standard-price")]/text()').extract_first()
        mrp_value = mrp_value.replace("\n", "").strip()
        mrp = float(re.search(r'(\d+,\d+)', mrp_value).group(1).replace(',','.'))
        price = selector.xpath('//span[contains(@class,"product-sales-price")]/text()').extract_first()
        selling_price = float(re.search(r'(\d+,\d+)', price).group(1).replace(',','.'))
        pdp_images = selector.xpath('//img[contains(@class, "product-image-hero")]/@src').extract()


        items['product_name'] = name
        items['color'] = color
        items['description'] = description
        items['breadcrumbs'] = breadcrumbs_list
        items['feature_image'] = feature_image
        items['mrp'] = mrp
        items['selling_price'] = selling_price
        items['pdp_images'] = pdp_images
        yield items