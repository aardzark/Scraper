#!/usr/bin/env bash

# Scrapy is not able to communicate with the target when this script is ran on WSL
# Running the commands individually does work on WSL

echo "Installing the python venv module..."
sudo apt install python3.8-venv

echo "Creating python virtual environment..."
python3 -m venv .venv

echo "Activating the python virtual environment..."
source .venv/bin/activate

echo "Installing required packages..."
pip install -r book_scraper/requirements.txt

echo "Running book scraper..."
python3 book_scraper/main.py

echo "Deactivating python virtual environment..."
deactivate
