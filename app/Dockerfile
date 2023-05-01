FROM python:3.9

COPY book_scraper /book_scraper
#RUN mkdir -p /scraper
#COPY requirements.txt /scraper
#COPY scrapy.cfg /scraper
COPY scrapy.cfg /scrapy.cfg
#WORKDIR /book_scraper
#RUN ls -al
RUN pip install -r book_scraper/requirements.txt

CMD ["python", "book_scraper/main.py"]