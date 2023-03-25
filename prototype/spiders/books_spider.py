import scrapy
import logging


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

        '''
        This is a recursive call to the book_parsing method. 
        It will parse all books and then return control to the page_parsing method when finished.
        '''
        # yield scrapy.Request(url=current_url, callback=self.book_parse)

        print(f'Current url: {current_url}')
        catalogue_path = current_url[: current_url.rfind('/') + 1]
        next_page = response.xpath('''//*[@id="default"]/div/div/div/div/
                                    section/div[2]/div/ul/li[@class="next"]/a/@href''').get()

        try:
            next_url = catalogue_path + next_page
            yield scrapy.Request(url=next_url, callback=self.page_parse)
        except TypeError:
            logging.getLogger('scrapy.crawler').error('Out of pages')
            self.crawler.stop()


    # def book_parse(self, response: scrapy.http.Response):
        # current_url = response.url
        # ...
        # try:
            # yield scrapy.Request(url=next_url, callback=self.book_parse)
        # except TypeError:
            # logging.getLogger('scrapy.crawler').info('Out of books')
            # pass

