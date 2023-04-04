# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from typing import List, Iterable

import scrapy.exceptions
from scrapy import signals, Spider, Request
from scrapy.http import Response
from scrapy.utils.url import urlparse
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class TutorialSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response: Response, spider: Spider) -> None:
        # Log the method name and response url to assist in visualizing Scrapy's logic flow
        spider.logger.debug(f'Inside process_spider_input for response: {response.url}')

        url_parts: List[str] = response.url.rpartition('/')
        catalogue_path: str = url_parts[0] + '/'
        next_page: str = response.xpath('''
                                            //*[@id="default"]/div/div/div/div/
                                            section/div[2]/div/ul/li[@class="next"]/a/@href
                                            ''').get()

        next_page_url = catalogue_path + next_page if next_page else None
        response.meta['next_page_url'] = next_page_url
        books = [catalogue_path + book_url for book_url in response.css('.product_pod a::attr(href)').getall()]


        '''
        # Check for no depth, e.g. start request, and if page_parse is the callback method for the response
        if response.meta.get('depth') is None or response.meta['parse_method'] == 'page_parse':
            # Extract the URL of the catalogue path
            url_parts = response.url.rpartition('/')
            catalogue_path = url_parts[0] + '/'
            # Extract the next page location
            next_page = response.xpath('
                                        //*[@id="default"]/div/div/div/div/
                                        section/div[2]/div/ul/li[@class="next"]/a/@href
                                        ').get()

            # Check if we have reached the end of pagination and
            # join the catalogue path and next page location, and if we haven't,
            # set the next_page_url to None to signal to the spider to close
            next_page_url = catalogue_path + next_page if next_page else None

            # Return the count of book listings on the current page
            book_count = len(response.xpath('//*[@id="default"]/div/div/div/div/section/div[2]/ol/li'))

            book_urls = []
            for i in range(book_count):
                # Extract the location of the specified book on the current page
                book = response.xpath(f'
                                        /html/body/div/div/div/div/section/
                                        div[2]/ol/li[{i + 1}]/article/h3/a/@href
                                        ').get()
                # Join the catalogue path and book location
                book_url = catalogue_path + book
                book_urls.append(book_url)

            # Update the response metadata
            response.meta.update({
                'next_page_url': next_page_url,
                'book_index': 1,
                'book urls': book_urls
            })
 
        elif response.meta.get('parse_method') == 'book_parse':
            pass
        '''
        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response: Response, result, spider):
        # Log the method name and response url to assist in visualizing Scrapy's logic flow
        spider.logger.debug(f'Inside process_spider_output for response: {response.url}')


        '''
        # Check if book_parse is the callback method for the response
        #if response.meta.get('parse_method') == 'book_parse':
            #book_urls: List[str] = response.meta.get('book urls')
            # Check if the current url is within range of the list length of book urls
            #if book_urls.index(response.url) + 1 < len(book_urls):
                # Assign the next book url in the list
                #next_book_url = book_urls[book_urls.index(response.url) + 1]
            #else:
                #next_book_url = None

            # Update the response metadata
            #response.meta.update({'next_book_url': next_book_url,
                                  #'book urls': book_urls})
        '''

        # Called with the results returned from the Spider, after
        # it has processed the response.
        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class TutorialDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
