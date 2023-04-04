# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item


class BookItem(Item):
    title: Field = Field()
    description: Field = Field()
    upc: Field = Field()
    price: Field = Field()
    tax: Field = Field()
    stock: Field = Field()
    number_of_reviews: Field = Field()
    pass
