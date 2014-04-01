from DaftScraper.items import DaftscrapApiItem
from DaftScraper.settings import CONN

__author__ = 'danmalone'


def map_to_item(cursor, items):
    result = cursor.fetchone()

    while result is not None:
        item = DaftscrapApiItem()
        item['id'] = result[0]
        item['area'] = result[2]
        item['collection'] = result[3]
        item['county'] = result[4]
        item['lat'] = result[6]
        item['long'] = result[7]
        item['link'] = result[8]
        item['photo'] = result[9]
        item['street'] = result[10]
        item['rent'] = result[11]
        item['summary'] = result[12]
        items.append(item)
        result = cursor.fetchone()


def select_by_county(data):
    cursor = CONN.cursor()
    area = data['area']
    try:
        cursor.execute("select * From Rentals where County=%s", (area,))

    except Exception, e:
        print e.message

    items = []
    map_to_item(cursor, items)

    return items


def distance_between_points(property1, property2):
    distance = 0
    distance += abs(property1['lat'] - property2['lat'])
    distance += abs(property1['long'] - property2['long'])
    distance += abs(property1['rent'] - property2['rent'])
    return distance








