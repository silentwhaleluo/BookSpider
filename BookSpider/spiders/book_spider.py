# -*- coding: utf-8 -*-
from BookSpider.utils.common import get_md5
import scrapy
import datetime
from scrapy.http import Request
from urllib import parse
from BookSpider.items import BookItem, BookItemFirstLoader


def parse_book_detail(response):
    # from item loader load data
    item_loader = BookItemFirstLoader(item=BookItem(), response=response)
    date = datetime.datetime.now().date()
    # url
    item_loader.add_value('url', response.url)
    item_loader.add_value('url_md5', get_md5(response.url))
    item_loader.add_value('process_date', date)
    # image
    img_url = response.xpath('//*[@id="product_gallery"]/div/div/div/img/@src').getall()
    img_url = [parse.urljoin(response.url, url) for url in img_url]
    item_loader.add_value('img_url', img_url)
    # book info
    item_loader.add_xpath('title', '//*[@id="content_inner"]/article/div[1]/div[2]/h1/text()')
    item_loader.add_xpath('description', '//*[@id="content_inner"]/article/p/text()')
    item_loader.add_xpath('star_rating', '//*[@id="content_inner"]/article/div[1]/div[2]/p[3]/@class')
    table = response.xpath('//td/text()').getall()
    item_loader.add_value('upc', table[0])
    item_loader.add_value('product_type', table[1])
    item_loader.add_value('currency', table[2][0])
    item_loader.add_value('price_exceltax', table[2])
    item_loader.add_value('price_incltax', table[3])
    item_loader.add_value('tax', table[4])
    item_loader.add_value('availability', table[5])
    item_loader.add_value('n_reviews', table[6])

    book_item = item_loader.load_item()

    yield book_item


class BookSpiderSpider(scrapy.Spider):
    name = 'book_spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        # extract the url of each book and get the url of next page
        book_urls = response.xpath("//article[@class='product_pod']/h3/a/@href").getall()
        for book_url in book_urls:
            yield Request(url=parse.urljoin(response.url, book_url), callback=parse_book_detail)

        # next page
        next_url = response.xpath('//li[@class="next"]/a/@href').extract_first('')
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
