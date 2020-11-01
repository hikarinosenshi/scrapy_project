from scrapy import Spider, Request
from rumratings.items import RumratingsItem
import math
import re

class RumratingsSpider(Spider):
    name = 'rumratings_spider'
    start_urls = ['https://rumratings.com/brands']
    allowed_urls = ['https://rumratings.com/']

    def parse(self, response):
        total_pages = int(response.xpath('//b/text()').extract()[1])
        num_pages = math.ceil(total_pages / 24)      # assuming 24 listings per page
        # print("-"*10,"START DEBUG","-"*20)
        # print('Number of pages: ', num_pages)
        # print("-"*10,"END DEBUG","-"*20)
        url_list = [f'https://rumratings.com/brands?page={i+1}' for i in range(num_pages)]
        for url in url_list:
            yield Request(url = url, callback = self.parse_result_page)

    def parse_result_page(self, response):
        # print("-"*10,"START DEBUG","-"*20)
        # print(response.url)
        # print("-"*10,"END DEBUG","-"*20)
        product_url_list = response.xpath('//div[contains(@class,"span1 width_")]//a/@href').extract()
        for product_url in product_url_list:
            yield Request(url = 'https://rumratings.com' + product_url, callback = self.parse_product_page)

    def parse_product_page(self, response):
        # print("-"*10,"START DEBUG","-"*20)
        # print(response.url)
        # print("-"*10,"END DEBUG","-"*20)
        try:
            name = response.xpath('//h1[@class="hero-title"]/span/text()').extract_first().strip()
        except:
            print('********* Could not find the name of the product. **********')
            print('Offending URL: {response.url}')
            name = ''

        try:
            list_ct = response.xpath('//a[@class="hero-edit-link"]//text()').extract()
            country = list_ct[0]
            rum_type = list_ct[1]
        except:
            print('********* Not able to read country and type **********')
            print('Offending URL: {response.url}')
            country = ''
            rum_type = ''

        try:
            list_description = response.xpath('//div[@class="description hero-description"]//text()').extract()
            description = ''
            for i in list_description:
                if len(i.strip()) > 0:
                    description += i + ' '
        except:
            print('********* Not able to read description **********')
            print('Offending URL: {response.url}')
            description = ''

        try:
            rating = float(response.xpath('//big[@style="font-size: 40px; font-weight: 900"]//text()').extract()[0])
        except:
            print('********* Not able to read rating **********')
            print('Offending URL: {response.url}')
            rating = 0.0

        try:
            n_r = re.search('\d+',response.xpath('//span[@style="white-space: nowrap"]//text()').extract()[0])
            num_ratings = int(n_r.group(0))
        except:
            print('********* Not able to read number of ratings **********')
            print('Offending URL: {response.url}')
            num_ratings = 0







        item = RumratingsItem()
        item['name'] = name
        item['description'] = description
        item['country'] = country
        item['rum_type'] = rum_type
        item['num_ratings'] = num_ratings
        item['rating'] = rating


        yield item





