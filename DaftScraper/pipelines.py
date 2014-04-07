# Define your item pipelines here
#
# Dont forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import traceback
from DaftScraper.settings import CONN


class DaftScraperPipeline(object):
    def __init__(self):
        self.file = open('items.json', 'wb')

    def process_item(self, item, spider):
        try:
            # print ''
            # line = json.dumps(dict(item)) + '\n'
            # self.file.write(line)
            # insert_row(item)
            insert_json_row(item)

        except Exception, e:
            print('Exception pipeline: ' + e.message)
        return item


def insert_scraped_row(data):
    cursor = CONN.cursor()  # important MySQLdb Cursor object

    try:
        if not checkForDuplicate(data):
            return
        else:
            cursor.execute(
                "insert into {0} (Address,Address_1, Address_2, Address_3, County, Baths, Beds, Price) values (%s,%s,%s,%s,%s,%s,%s,%s)".format(
                    data['type']),
                (data['address'], data['address0'], data['address1'], data['address2'], data['county'],
                 data['baths'], data['beds'], data['price']))

            CONN.commit()
            #     print Inserted
            cursor.close()

    except Exception, e:
        print('Exception inserting scraped row: ' + e.message)


def insert_json_row(item):
    cursor = CONN.cursor()  # important MySQLdb Cursor object

    try:
        if not checkForDuplicate(item):
            return
        else:
            cursor.execute(
                "insert into Rentals (Area, Collection, County, Listing_id, Lat, Longitude, Link,Photo_url,Street,Rent,Summary) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (item['area'], item['collection'], item['county'], item['id'], item['lat'], item['long'], item['link'],
                 item['photo'], item['street'], item['rent'], item['summary']))

            CONN.commit()
        #     print Inserted
        cursor.close()

    except Exception, e:
        print 'Exception inserting json: ' + e.message
        print traceback.format_exc()


def checkForDuplicate(data):
    cursor = CONN.cursor()
    cursor.execute(
        "select * From {0} WHERE Address=%s".format(data['type']),
        (data['address'],))

    duplicate = cursor.fetchone()
    cursor.close()
    if duplicate:
        return False
    else:
        return True


def checkForDuplicate_rental(data):
    cursor = CONN.cursor()
    cursor.execute(
        "select * From {0} WHERE Listing_id=%s".format('rentals'),
        (data['item'],))

    duplicate = cursor.fetchone()
    cursor.close()
    if duplicate:
        return False
    else:
        return True

