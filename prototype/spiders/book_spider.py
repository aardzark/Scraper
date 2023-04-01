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
        print(f'Page url: {response.url}')

        try:
            yield scrapy.Request(url=response.meta.get('book urls')[0],
                                 callback=self.book_parse,
                                 meta={'parse_method': 'book_parse',
                                       'book urls': response.meta.get('book urls')})

            yield scrapy.Request(url=response.meta.get('next_page_url'),
                                 callback=self.page_parse,
                                 meta={'parse_method': 'page_parse'})

        except TypeError:
            print("\x1b[31mOUT OF BOOKS\x1b[0m")
            pass

    def closed(self, reason: str) -> None:
        self.logger.critical('Spider closed: %s', reason)

    def book_parse(self, response: scrapy.http.Response) -> None:
        print(f'Book url: {response.url}')
        book_urls: List[str] = response.meta.get('book urls')

        if book_urls.index(response.url) + 1 < len(book_urls):
            yield scrapy.Request(
                url=book_urls[book_urls.index(response.url) + 1],
                callback=self.book_parse,
                meta={'parse_method': 'book_parse',
                      'book urls': response.meta.get('book urls')})
        else:
            return None
