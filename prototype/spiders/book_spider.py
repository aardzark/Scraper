import scrapy
from typing import List, Dict, Generator
from scrapy import Request, Spider
from scrapy.http import Response

class BookSpider(Spider):
    name: str = "books"

    def start_requests(self) -> List[Request]:
        urls: List[str] = [
            'http://books.toscrape.com/catalogue/page-1.html',
        ]

        for url in urls:
            yield Request(url=url, callback=self.generate_requests)

    def generate_requests(self, response: Response) -> Generator[Request, Request, None]:
        next_page_url: str = response.meta.get('next_page_url')

        for book in response.meta.get('books'):
            yield Request(url=book, callback=self.parse)

        yield Request(url=next_page_url, callback=self.generate_requests) if next_page_url else None

    def parse(self, response: Response) -> None:
        # Log the method name and response url to assist in visualizing Scrapy's logic flow
        self.logger.debug(f'Inside page_parse for response: {response.url}')

        #requests: List[Request] = []

        # Extract the URL of the catalogue path
        #url_parts: List[str] = response.url.rpartition('/')
        #catalogue_path: str = url_parts[0] + '/'
        # Extract the next page location
        #next_page: str = response.xpath('''
                                           #//*[@id="default"]/div/div/div/div/
                                           #section/div[2]/div/ul/li[@class="next"]/a/@href
                                           #''').get()

        # Check if we have reached the end of pagination and
        # join the catalogue path and next page location, and if we haven't,
        # set the next_page_url to None to signal to the spider to close
        #next_page_url: str = catalogue_path + next_page if next_page else None

        #page_request = Request(next_page_url, callback=self.page_parse)
        #requests.append(page_request)
        #yield iter(requests)
        '''
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
        '''

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
