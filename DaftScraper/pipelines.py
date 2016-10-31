# Define your item pipelines here
#
# Dont forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback
import logging
import json
from DaftScraper import mailer
from DaftScraper import settings


class DaftScraperPipeline(object):
    def __init__(self):
        if settings.DEBUG:
            self.file = open('items.json', 'wb')

    def process_item(self, item, spider):
        try:
            if settings.DEBUG:
                print('')
                line = json.dumps(dict(item)) + '\n'
                self.file.write(line)
            insert_json_row(item)

        except Exception as e:
            logging.error('Exception pipeline: ' + str(e))

        return item


def insert_scraped_row(data):
    cursor = settings.CONN.cursor()  # important MySQLdb Cursor object

    try:
        if not checkForDuplicate(data):
            return
        else:
            cursor.execute(
                "insert into {0} (Address,Address_1, Address_2, Address_3, County, Baths, Beds, Price) values (%s,%s,%s,%s,%s,%s,%s,%s)".format(
                    data['type']),
                (data['address'], data['address0'], data['address1'], data['address2'], data['county'],
                 data['baths'], data['beds'], data['price']))

            settings.CONN.commit()

    except Exception as e:
        logging.error('Exception inserting scraped row: ' + str(e))
    finally:
        cursor.close()


def insert_json_row(item):
    cursor = settings.CONN.cursor()  # important MySQLdb Cursor object
    settings.CONN.set_character_set('utf8')  # Ensure no 'latin-1' mysqlDB encoding issues

    try:
        if not checkForDuplicate_rental(item):
            return
        else:
            cursor.execute(
                "insert into Rentals (Area, Collection, County, Listing_id, Lat, Longitude, Link,Photo_url,Street,Rent,Summary) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (item['area'], item['collection'], item['county'], item['id'], item['lat'], item['long'], item['link'],
                 item['photo'], item['street'], item['rent'], item['summary']))

            settings.CONN.commit()
            if settings.EMAIL['enabled']:
                mailer.sendemail(item)

    except Exception as e:
        logging.error('Exception inserting json: ' + str(e))
        logging.error(traceback.format_exc())
    finally:
        cursor.close()


def checkForDuplicate(data):
    cursor = settings.CONN.cursor()
    cursor.execute(
        'select * From {} WHERE Address={}'.format(data['type'], data['address'])
    )

    duplicate = cursor.fetchone()

    if duplicate:
        return False
    else:
        return True


def checkForDuplicate_rental(data):
    cursor = settings.CONN.cursor()
    cursor.execute(
        'select * From {} WHERE Listing_id={}'.format('Rentals', data['id'])
    )

    duplicate = cursor.fetchone()

    if duplicate:
        return False
    else:
        return True
