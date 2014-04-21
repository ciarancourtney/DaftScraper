# coding=utf-8
import json
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
from DaftScraper.items import DaftscrapedItem, DaftscrapApiItem

__author__ = 'danmalone'


class EtsySpider(CrawlSpider):
    name = "daft"
    # allowed_domains = ["daft.ie"]
    DEFAULT_CHARSET = 'utf-8'

    def __init__(self, category=None, category2=None, *args, **kwargs):
        super(EtsySpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            "http://www.daft.ie/searchrental.daft?s%5Bcc_id%5D=&s%5Broute_id%5D=&s%5Ba_id_transport%5D=0&s%5Bstreet_name%5D=&s%5Btxt%5D=&s%5Bmnp%5D=&s%5Bmxp%5D=&s%5Bmnb%5D=&s%5Bmxb%5D=&s%5Bmnbt%5D=&s%5Bmxbt%5D=&s%5Bpt_id%5D=&s%5Bmove_in_date%5D=0&s%5Bmin_lease%5D=&s%5Bmax_lease%5D=&s%5Bfurn%5D=0&s%5Bnpt_id%5D=&s%5Bdays_old%5D=&s%5Bsingle_beds%5D=&s%5Bdouble_beds%5D=&s%5Btwin_beds%5D=&s%5Bagreed%5D=&more=&tab=&search=1&s%5Bsearch_type%5D=rental&s%5Btransport%5D=&s%5Badvanced%5D=&s%5Bprice_per_room%5D=",
        ]


    def parse_scrape(self, response):
        self.log("Visited %s" % response.url)

        sel = Selector(response)
        sites = sel.css('.box')
        items = []

        for site in sites:

            try:
                ad = site.css('.sponsored-box')
                if ad:
                    continue

                ad = site.css('script')
                if ad:
                    continue

                # //*[@id="sr_content"]/tbody/tr/td[1]/div[13]
                # //*[@id="sr_content"]/tbody/tr/td[1]/div[14]

                item = DaftscrapedItem()
                address = site.css(' h2 > a::text')
                if len(address) > 0:
                    address = address.extract()[0].replace('\n', '').strip().encode('utf8')

                if '- House to let' in address:
                    item['address'] = address.replace('- House to let', '').strip()
                elif "- Apartment to let" in address:
                    item['address'] = address.replace('- Apartment to let', '').strip()
                elif '- Flat to let' in address:
                    item['address'] = address.replace('- Flat to let', '').strip()
                elif "- Studio to let" in address:
                    item['address'] = address.replace('- Studio to let', '').strip()
                elif '- Studio apartment to let' in address:
                    item['address'] = address.replace('- Studio apartment to let', '').strip()
                else:
                    item['address'] = address

                address_list = item['address'].split(',')
                if len(address_list) >= 0:
                    for i in range(0, len(address_list)):
                        if i == 5: break
                        item['address' + `i`] = address_list[i]

                    item['county'] = address_list[len(address_list) - 1]
                    if len(address_list) <= 2:
                        item['address2'] = ' '

                item['price'] = site.css('.info-box').xpath('strong/text()').extract()

                if len(item['price']) > 0:
                    item['price'] = item['price'][0].replace(u'\u20ac', '')
                    item['price'] = item['price'].replace(u"\u00a3", '')

                if 'Weekly' in item['price']:
                    item['price'] = (item['price'].replace('Weekly', ''))

                if "Monthly" in item['price']:
                    item['price'] = (item['price'].replace('Monthly', ''))

                item['price'] = int(item['price'].replace(',', ''))

                item['type'] = site.css('.info li:nth-child(1)::text')
                if len(item['type']) > 0:
                    type = item['type'].extract()[0].replace('\n', '').strip().decode('utf8')
                    if 'House' in type:
                        item['type'] = 'House'
                    elif "Studio" in type:
                        item['type'] = 'Studio'
                    elif "Flat" in type:
                        item['type'] = 'Flat'
                    elif "Apartment" in type:
                        item['type'] = 'Apartment'
                    else:
                        item['type'] = 'House'

                item['beds'] = site.css('.info li:nth-child(2)::text').extract()
                if len(item['beds']) > 0:
                    item['beds'] = item['beds'][0].replace('\n', '').strip().replace('Beds', '').decode('utf8')
                    item['beds'] = int(item['beds'].replace('\n', '').strip().replace('Bed', '').decode('utf8'))
                else:
                    item['beds'] = 0

                item['baths'] = site.css('.info li:nth-child(3)::text').extract()
                if len(item['baths']) > 0:
                    item['baths'] = item['baths'][0].replace('\n', '').strip().replace('Baths', '').decode('utf8')
                    item['baths'] = int(item['baths'].replace('\n', '').strip().replace('Bath', ''))
                else:
                    item['baths'] = 0
                # lines = site.css('.text-block p').xpath('text()').extract()
                # lines = [l.strip() for l in lines if l.strip()]
                #
                # item['description'] = lines.pop(0).replace('\n', '').strip().encode('utf8')
                items.append(item)
                # break
                yield item

            except Exception, e:
                print 'Oops! EXCEPTION \n' + response.url + '\n' + e.message

        url = sel.css('li.next_page > a::attr(href)')
        if len(url) > 0:
            url = url.extract()[0]
            url = 'http://www.daft.ie/searchrental.daft' + url

            request = Request(url, callback=self.parse)
            yield request

            # yield self.items

    def parse(self, response):
        try:
            request = Request(
                url="http://www.daft.ie/ajax_endpoint.php?action=map_nearby_properties&type=rental&sw=(50.21403564497616%2C+-10.571344023437527)&ne=(60.479977662240046%2C+-0.947095976562528)&extra_params=%7B%22price%22%3A%5B0%2C50000000%5D%2C%22beds%22%3A%5B0%2C20%5D%7D",
                method="POST", callback=self.parse_categories)
            # ,headers={'Content-Length':   11151})
            yield request
        except Exception, e:
            print e.message

    def parse_categories(self, response):

        items = json.loads(response.body_as_unicode())

        resultItems = []
        for result in items:

            item = DaftscrapApiItem()
            item['area'] = result['area'].encode('utf-8')
            item['collection'] = result['collection'].encode('utf-8')
            item['county'] = result['county'].encode('utf-8')
            item['id'] = result['id']
            item['lat'] = result['lat']
            item['long'] = result['long']
            item['link'] = result['link'].encode('utf-8')
            item['photo'] = result['photo'].encode('utf-8')
            item['rent'] = result['rent'].replace(',', '').encode('utf-8')
            item['street'] = result['street'].encode('utf-8')
            item['summary'] = result['summary'].encode('utf-8')

            resultItems.append(item)
            yield item


    def parse_listings(self, response):
        self.log("Visited %s" % response.url)

        sel = Selector(response)
        sites = sel.css('#smi-summary-items .header_text')

        items = []

        for site in sites:
            item = DaftscrapedItem()

            item['beds'] = site.xpath('//*/span[3]/text()').extract()
            if len(item['beds']) > 0:
                item['beds'] = item['beds'][0].replace('\n', '').strip().replace('Beds', '').decode('utf8')
                item['beds'] = item['beds'].replace('\n', '').strip().replace('Bed', '').decode('utf8')
            else:
                item['beds'] = 0

            item['baths'] = site.xpath('//*/span[5]/text()').extract()
            if len(item['baths']) > 0:
                item['baths'] = item['baths'][0].replace('\n', '').strip().replace('Baths', '').decode('utf8')
                item['baths'] = item['baths'].replace('\n', '').strip().replace('Bath', '')
            else:
                item['baths'] = 0

            items.append(item)

        return items
