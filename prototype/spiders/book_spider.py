import scrapy


class BookSpider(scrapy.Spider):
    name: str = "books"

    def start_requests(self):
        urls: list[str] = [
            'http://books.toscrape.com/catalogue/page-1.html',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.page_parse)

    def page_parse(self, response: scrapy.http.Response):
        print(f'Page url: {response.url}')

        for i in range(1, response.meta['books_on_page']):
            book_url = response.meta['catalogue_path'] + response.meta['books'][i]
            yield scrapy.Request(url=book_url, callback=self.book_parse, meta={'parse_method': 'book_parse',
                                                                               'page_response': response})

        try:
            yield scrapy.Request(url=response.meta.get('next_page_url'), callback=self.page_parse,
                                 meta={'parse_method': 'page_parse'})
        except TypeError:
            raise scrapy.exceptions.CloseSpider('OUT OF BOOKS')

    def closed(self, reason):
        self.logger.critical('Spider closed: %s', reason)

    def book_parse(self, response: scrapy.http.Response):
        # book = response.meta['page_response']['meta']['book_index'] =
        for i in range(1, response.meta.get('page_response').meta.get('books_on_page')):
            response.meta['page_response'].meta['book_index'] = i + 1
            book_url = response.meta['page_response'].meta['catalogue_path'] \
                       + response.meta['page_response'].meta['books'][i]
            #print(book_url)
            #print(response.meta['page_response'].meta['book_index'])
        book_url = response.url
        print(f'Book url: {book_url}')
