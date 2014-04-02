from math import sqrt
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
    try:
        cursor.execute("select * From Rentals where County=%s AND Collection=%s",
                       (data['county'], 'monthly'))

    except Exception, e:
        print e.message

    items = []
    map_to_item(cursor, items)

    return items


def compute_nearest_neighbour(property1, properties):
    euc_distances = []

    for property2 in properties:
        distance = normalise(property1, property2)

        euc_distances.append(((distance, property2['rent'])))
    euc_distances.sort()

    return euc_distances


def normalise(property1, property2):
    weight1 = 0
    weight2 = 12

    distance = sqrt(
        weight1 * (float(property1['lat']) - float(property2['lat'])) ** 2 +
        weight2 * (float(property1['long']) - float(property2['long'])) ** 2)

    return distance


