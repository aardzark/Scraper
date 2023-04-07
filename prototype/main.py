from prototype.spiders.book_spider import BookSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(BookSpider)
    process.start()