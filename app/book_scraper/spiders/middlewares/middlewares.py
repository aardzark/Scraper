# Define here the models for your spiders middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from typing import List, Iterable

import scrapy.exceptions
from scrapy import signals, Spider, Request
from scrapy.http import Response
from scrapy.utils.url import urlparse
from urllib.parse import urlsplit, ParseResult
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class TutorialSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spiders middleware does not modify the
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

        # Parse the response url
        url_parts: List[ParseResult] = urlparse(response.url)
        base_url: str = url_parts.scheme + '://' + url_parts.netloc + '/'
        url_paths: List[str] = url_parts.path.split('/')

        # Obtain the location of the next page
        next_page: str = response.css('.next a::attr(href)').get()

        # Build the url of the next page
        # None is the stop condition for the spiders
        next_page = base_url + url_paths[1] + '/' + next_page if next_page else None

        # Obtain the location of each book
        # Perform list comprehension to build the urls for each book
        books: List[str] = [base_url + url_paths[1] + '/' + book_loc for book_loc in response.css('.product_pod a::attr(href)').getall()]

        # Update the metadata for the response
        response.meta['next_page'] = next_page
        response.meta['books'] = books

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response: Response, result, spider):
        # Log the method name and response url to assist in visualizing Scrapy's logic flow
        spider.logger.debug(f'Inside process_spider_output for response: {response.url}')

        # Called with the results returned from the Spider, after
        # it has processed the response.
        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spiders or process_spider_input() method
        # (from other spiders middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spiders, and works
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
