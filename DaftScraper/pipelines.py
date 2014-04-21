# Define your item pipelines here
#
# Dont forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from smtplib import SMTPException
import traceback
import smtplib

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
            sendemail(item)

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
    fromaddr = 'ashaman@redbrick.dcu.ie'
    toaddrs = 'daft@vadimck.com'
    if 'monthly' in item['collection'].lower():
        if 'dublin' in item['county'].lower():
            if int(item['rent']) <= 2200:
                if '3' in item['summary']:
                    msg = "From: <ashaman@redbrick.dcu.ie>\nTo: <daft@vadimck.com>\nSubject: " + item[
                        'summary'] + " " + str(item['rent'] + "\n\n")

                    msg2 = "Area:{0}\nrent:{1},\nCollection:{2}\nStreet:{3},\nCounty:{4},\nLatitude:{5},\nLongitude:{6}\nlink:www.daft.ie{7}\nphoto:{8}".format(
                        item['area'], str(item['rent']),
                        item['collection'],
                        item['street'], item['county'],
                        str(item['lat']), str(item['long']),
                        item['link'], item['photo'])

                    # Credentials (if needed)
                    username = 'ashaman'

                    email = msg + msg2
                    # The actual mail send
                    try:
                        server = smtplib.SMTP()
                        server.connect()
                        # server.starttls()
                        # server.login(username, password)
                        server.sendmail(fromaddr, toaddrs, email)
                        server.quit()
                    except SMTPException, e:
                        print "Error: unable to send email" + e.message

                        # SELECT * FROM `Rentals` WHERE `Collection` like '%Monthly%'  and `County` like '%Dublin%'  and `Rent` between 0 and 2200 and `Summary` like '%3%';