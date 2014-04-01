# Scrapy settings for DaftScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import MySQLdb

LOG_LEVEL = 'DEBUG'
BOT_NAME = 'DaftScraper'
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36"

# SQL DATABASE SETTING
SQL_DB = 'DaftDB'
SQL_TABLE = 'Houses'
SQL_HOST = '127.0.0.1'
SQL_PORT = 8889
SQL_USER = 'root'
SQL_PASSWD = 'root'

# connect to the MySQL server
try:
    CONN = MySQLdb.connect(host=SQL_HOST,
                           port=SQL_PORT,
                           user=SQL_USER,
                           passwd=SQL_PASSWD,
                           db=SQL_DB)
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    # sys.exit(1)

SPIDER_MODULES = ['DaftScraper.spiders']
NEWSPIDER_MODULE = 'DaftScraper.spiders'

ITEM_PIPELINES = {'DaftScraper.pipelines.DaftScraperPipeline': 300}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'DaftScraper (+http://www.yourdomain.com)'


