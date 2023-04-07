# Scraper

## Description

This is a web scraper model for a larger project. The scraper has been designed using best practices for Scrapy and 
follows its recommended design patterns. It scrapes the books from https://books.toscrape.com.
The book records are posted to a PostgreSQL database.

## Getting Started

### Installing PostgreSQL

To install PostgreSQL on Windows:

Use the [interactive installer](https://www.postgresql.org/download/windows/).

To install PostgreSQL on Linux:

`sudo apt-get install postgresql`

### Installing Python3

Check if Python3 is installed on your operating system.

`python3 --version`

To install Python3 on Linux:

`sudo apt update`

`sudo apt-get install python3`

To install Python3 on Windows:

Visit https://www.python.org/downloads/ and download the appropriate
installer for your operating system (32-bit or 64-bit).

### Installing Pip
Check if pip is installed on your operating system.

`pip --version`

To install pip on Linux:

`sudo apt update`

`sudo apt install python3-pip`

To install pip on Windows:

`curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`

`python3 get-pip.py`

### Installing Dependencies

Check if scrapy is installed.

`pip show scrapy`

Install scrapy if it's not installed.

`pip install scrapy`

Check if psycopg2 is installed.

### Running the Script

Clone the repository.

`git clone https://github.com/aardzark/Scraper.git`

Navigate to `Scraper/prototype/`.

Run the script.

`python3 main.py`

## Contributors

<a href = "https://github.com/aardzark/Scraper/graphs/contributors">
  <img src="https://github.com/aardzark.png?size=50">
</a>