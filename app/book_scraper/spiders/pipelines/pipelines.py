import psycopg2
from scrapy import Request
from psycopg2 import extensions
import logging
from psycopg2.errors import Error
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class PostgreSQLPipeline:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('POSTGRESQL_HOST'),
            port=crawler.settings.get('POSTGRESQL_PORT'),
            user=crawler.settings.get('POSTGRESQL_USER'),
            password=crawler.settings.get('POSTGRESQL_PASSWORD'),
            database=crawler.settings.get('POSTGRESQL_DATABASE'),
        )

    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        cursor = self.conn.cursor()
        # @TODO Fix description format
        query = f'INSERT INTO books (title, description, upc, price, tax, stock, number_of_reviews) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        values = (item['title'], (item['description']), item['upc'], item['price'],
                  item['tax'], item['stock'], item['number_of_reviews'])

        try:
            cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            logging.error(f"Error executing query: {query} with values: {values}")
            logging.error(e)
        finally:
            cursor.close()
            return item


class BookImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['images'] = image_paths
        return item
