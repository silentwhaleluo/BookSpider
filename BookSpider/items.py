# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
# from BookSpider.utils.common import get_md5


class BookItemFirstLoader(ItemLoader):
    # default to take first
    default_output_processor = TakeFirst()


def extract_numbers(text):
    number_match = re.match('.*?([0-9.]+).*', text)
    if number_match:
        nums = number_match.group(1)
        if '.' in nums:
            nums = float(nums)
        else:
            nums = int(nums)
    else:
        nums = 0
    return nums


def return_value(value):
    return value


def delate_quote(text):
    return text[1:-1]

def work_to_int(text):
    word_num = re.match(r'.*(zero|one|two|three|four|five).*', text, flags=re.IGNORECASE)
    if word_num:
        word_num = word_num.group(1)
    num_dict = {
        'Zero': 0,
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    return num_dict[word_num]


# text = 'star-rating Three'
# print(extract_wordnumbers_toint(text))

class BookItem(scrapy.Item):
    # url
    url = scrapy.Field()
    url_md5 = scrapy.Field()
    #     input_prcessor=MapCompose(get_md5)
    # )
    process_date = scrapy.Field()

    #
    img_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    img_path = scrapy.Field()

    # book info
    title = scrapy.Field()
    description = scrapy.Field()
    #     input_processor=MapCompose(delate_quote)
    # )

    star_rating = scrapy.Field(
        input_processor=MapCompose(work_to_int)
    )
    upc = scrapy.Field()
    product_type = scrapy.Field()
    currency = scrapy.Field()
    price_exceltax = scrapy.Field(
        input_processor=MapCompose(extract_numbers)
    )
    price_incltax = scrapy.Field(
        input_processor=MapCompose(extract_numbers)
    )
    tax = scrapy.Field(
        input_processor=MapCompose(extract_numbers)
    )
    availability = scrapy.Field(
        input_processor=MapCompose(extract_numbers)
    )
    n_reviews = scrapy.Field(
        input_processor=MapCompose(int)
    )
