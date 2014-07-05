# Define your item pipelines here
#
# Dont forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from smtplib import SMTPException
import traceback
import smtplib
import secrets

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

    except Exception, e:
        print('Exception inserting scraped row: ' + e.message)
    finally:
        cursor.close()


def insert_json_row(item):
    cursor = CONN.cursor()  # important MySQLdb Cursor object

    try:
        if not checkForDuplicate_rental(item):
            return
        else:
            cursor.execute(
                "insert into Rentals (Area, Collection, County, Listing_id, Lat, Longitude, Link,Photo_url,Street,Rent,Summary) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (item['area'], item['collection'], item['county'], item['id'], item['lat'], item['long'], item['link'],
                 item['photo'], item['street'], item['rent'], item['summary']))

            CONN.commit()
            # sendemail(item)

    except Exception, e:
        print 'Exception inserting json: ' + e.message
        print traceback.format_exc()
    finally:
        cursor.close()


def checkForDuplicate(data):
    cursor = CONN.cursor()
    cursor.execute(
        "select * From {0} WHERE Address=%s".format(data['type']),
        (data['address'],))

    duplicate = cursor.fetchone()

    if duplicate:
        return False
    else:
        return True


def checkForDuplicate_rental(data):
    cursor = CONN.cursor()
    cursor.execute(
        "select * From {0} WHERE Listing_id=%s".format('Rentals'),
        (data['id'],))

    duplicate = cursor.fetchone()

    if duplicate:
        return False
    else:
        return True


def sendemail(item):
    fromaddr = 'aruthar72@gmail.com'
    toaddrs = 'daft@vadimck.com'
    if 'Monthly' in item['collection'] and 'Dublin' in item['county'] and item['rent'] < 2200 and '3' in item[
        'summary']:
        msg = 'New Property:' + item['area'], item['collection'], item['county'], item['id'], item['lat'], item['long'], \
              item['link'], item['photo'], item['street'], item['rent'], item['summary']

        # Credentials (if needed)
        username = secrets.user
        password = secrets.passW

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
        # SELECT * FROM `Rentals` WHERE `Collection` like '%Monthly%'  and `County` like '%Dublin%'  and `Rent` between 0 and 2200 and `Summary` like '%3%';
