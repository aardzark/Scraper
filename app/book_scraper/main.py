from spiders.book_spider import BookSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    process = CrawlerProcess(get_project_settings())
    process.crawl(BookSpider)
    process.start()