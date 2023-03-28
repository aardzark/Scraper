import scrapy


class BooksSpider(scrapy.Spider):
    name: str = "quotes"

    def start_requests(self):
        urls: list[str] = [
            'http://books.toscrape.com/catalogue/page-1.html',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.page_parse)

    def page_parse(self, response: scrapy.http.Response):
        current_url = response.url
        print(f'Page url: {current_url}')
        catalogue_path = current_url[: current_url.rfind('/') + 1]
        books_remaining = len(response.xpath('//*[@id="default"]/div/div/div/div/section/div[2]/ol/li'))

        for i in range(books_remaining):
            book = response.xpath(f'''
                                    /html/body/div/div/div/div/section/
                                    div[2]/ol/li[{i + 1}]/article/h3/a/@href
                                    ''').get()

            book_url = catalogue_path + book

            yield scrapy.Request(url=book_url, callback=self.book_parse)

        next_page = response.xpath('''
                                    //*[@id="default"]/div/div/div/div/
                                    section/div[2]/div/ul/li[@class="next"]/a/@href
                                    ''').get()

        try:
            next_url = catalogue_path + next_page
            yield scrapy.Request(url=next_url, callback=self.page_parse)
        except TypeError:
            raise scrapy.exceptions.CloseSpider('OUT OF BOOKS')

    def closed(self, reason):
        self.logger.critical('Spider closed: %s', reason)

    def book_parse(self, response: scrapy.http.Response):
        book_url = response.url
        print(f'Book url: {book_url}')
