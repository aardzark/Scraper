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
        self.log(f'Inside parse for response: {response.url}')
