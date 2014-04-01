# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class DaftscrapedItem(Item):
    # define the fields for your item here like:
    # name = Field()
    address = Field()

    address0 = Field()
    address1 = Field()
    address2 = Field()
    address3 = Field()
    address4 = Field()

    county = Field()
    price = Field()
    type = Field()  #apartment
    beds = Field()
    baths = Field()
    description = Field()
    pass


class DaftscrapApiItem(Item):
    # define the fields for your item here like:
    # name = Field()
    area = Field()
    collection = Field()
    county = Field()
    id = Field()
    lat = Field()
    link = Field()
    long = Field()
    photo = Field()
    rent = Field()
    street = Field()
    summary = Field()
    pass

class ListingItem(Item):
    facilities = Field()
    property_description = Field()
    bedrooms = Field()
    baths = Field()
    lease = Field()
    page_description = Field()
    page_title = Field()
    category_name = Field()
    short_name = Field()
    long_name = Field()
    num_children = Field()
    pass
