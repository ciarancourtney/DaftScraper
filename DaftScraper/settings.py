# Scrapy settings for DaftScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import MySQLdb

LOG_LEVEL = 'INFO'
BOT_NAME = 'DaftScraper'
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36"

# MySQL DATABASE SETTINGS

CONN = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='DaftScraper')

DEBUG = False

EMAIL = {
    'enabled': False,
    'from': '',
    'to': '',
    'smtp_server': 'smtp.gmail.com:587',
    'username': '',
    'password': ''
}


SPIDER_MODULES = ['DaftScraper.spiders']
NEWSPIDER_MODULE = 'DaftScraper.spiders'

ITEM_PIPELINES = {'DaftScraper.pipelines.DaftScraperPipeline': 300}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'DaftScraper (+http://www.yourdomain.com)'


