FROM python:3.9

# Install dependencies required to download and extract dockerize
RUN apt-get update && apt-get install -y wget tar

RUN wget -O dockerize.tar.gz https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar -C /usr/local/bin -xzvf dockerize.tar.gz && \
    rm dockerize.tar.gz

COPY book_scraper /book_scraper
COPY scrapy.cfg /scrapy.cfg
RUN mv -f /book_scraper/.env.docker /book_scraper/.env
RUN pip install -r book_scraper/requirements.txt

CMD ["python", "book_scraper/main.py"]
EXPOSE 5432