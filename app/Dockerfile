FROM python:3.9

COPY book_scraper /book_scraper
COPY scrapy.cfg /scrapy.cfg
RUN mv -f /book_scraper/.env.docker /book_scraper/.env
RUN pip install -r book_scraper/requirements.txt

CMD ["python", "book_scraper/main.py"]
EXPOSE 5432