# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PricecomparatorItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()

class ProductItem(scrapy.Item):
    retailer = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()
    rating = scrapy.Field()
    # number_ratings = scrapy.Field()
    # number_reviews = scrapy.Field()
    seller = scrapy.Field()
    seller_ratings = scrapy.Field()
    url = scrapy.Field()
