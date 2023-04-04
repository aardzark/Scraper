import scrapy
from typing import List, Dict, Generator
from scrapy import Request, Spider
from scrapy.http import Response
from prototype.items import BookItem


class BookSpider(Spider):
    name: str = "books"

    def start_requests(self) -> List[Request]:
        urls: List[str] = [
            'http://books.toscrape.com/catalogue/page-1.html',
        ]

        for url in urls:
            yield Request(url=url, callback=self.generate_requests)

    def generate_requests(self, response: Response) -> Generator[Request, None, None]:
        next_page: str = response.meta.get('next_page')

        # Generate requests for each book url
        # Parse each book
        for book in response.meta.get('books'):
            yield Request(url=book, callback=self.parse)

        # Generate a request for the next page
        # If None is yielded, the spider will receive a signal that scraping is finished and it will close
        yield Request(url=next_page, callback=self.generate_requests) if next_page else None

    def parse(self, response: Response) -> None:
        # Log the method name and response url to assist in visualizing Scrapy's logic flow
        self.log(f'Inside parse for response: {response.url}')

        book_item = BookItem()

        book_item['title'] = response.css('.product_page h1::text').get()
        book_item['description'] = response.css('#product_description + p::text').get()
        book_item['upc'] = response.css('th:contains("UPC") + td::text').get()
        book_item['price'] = response.css('th:contains("Price (excl. tax)") + td::text').get().split("£")[1]
        book_item['tax'] = response.css('th:contains("Tax") + td::text').get().split("£")[1]
        book_item['stock'] = response.css('th:contains("Availability") + td::text').get().split("(")[1].split(" ")[0]
        book_item['number_of_reviews'] = response.css('th:contains("Number of reviews") + td::text').get()

        yield book_item
