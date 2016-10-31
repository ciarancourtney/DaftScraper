#!/usr/bin/env bash

source bin/build_db.sh

# If using python <3.3, use virtualenv instead

echo 'Creating virtual env...'
python3 -m venv venv/ --clear

echo 'Installing requirements into virtual env...'
venv/bin/pip install -r requirements.txt

echo 'Install Complete. Execute a crawl using'
echo "    $ venv/bin/scrapy crawl daft"
