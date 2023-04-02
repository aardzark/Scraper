import scrapy
from typing import List, Dict


class BookSpider(scrapy.Spider):
    name: str = "books"

    def start_requests(self) -> List[scrapy.Request]:
        urls: List[str] = [
            'http://books.toscrape.com/catalogue/page-1.html',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.page_parse)

    def page_parse(self, response: scrapy.http.Response) -> None:
        # Log the method name and response url to assist in visualizing Scrapy's logic flow
        self.logger.debug(f'Inside page_parse for response: {response.url}')

        # Make an initial request to book_parse and pass the book urls as metadata
        yield scrapy.Request(url=response.meta.get('book urls')[0],
                             callback=self.book_parse,
                             meta={'parse_method': 'book_parse',
                                   'book urls': response.meta.get('book urls')})  # @TODO Handle this metadata better.

        # If next_page_url is None we have reached the end of pagination
        # and this will signal the spider to close naturally
        if response.meta.get('next_page_url') is None:
            return None

        # Make recursive requests to page_parse and set the parse_method
        # and pass the parse method as metadata
        yield scrapy.Request(url=response.meta.get('next_page_url'),
                             callback=self.page_parse,
                             meta={'parse_method': 'page_parse'})

    def closed(self, reason: str) -> None:
        self.logger.critical('Spider closed: %s', reason)

    def book_parse(self, response: scrapy.http.Response) -> None:
        # Log the method name and response url to assist in visualizing Scrapy's logic flow
        self.log(f'Inside book_parse for response: {response.url}')

        if response.meta.get('next_book_url') is None:
            return None

        # Make recursive requests to page_parse and set the parse_method
        yield scrapy.Request(
            url=response.meta.get('next_book_url'),
            callback=self.book_parse,
            meta={'parse_method': 'book_parse',
                  'book urls': response.meta.get('book urls')})  # @TODO Handle this metadata better.
