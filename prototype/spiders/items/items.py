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
