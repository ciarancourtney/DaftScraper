import json
import os
from Cherry.Miner.DataMiner import select_by_county, compute_nearest_neighbour
from DaftScraper.items import DaftscrapApiItem

__author__ = 'danmalone'
import cherrypy
from mako.lookup import TemplateLookup

lookup = TemplateLookup(directories=['html'])


class Root(object):
    @cherrypy.expose
    def index(self):
        tmpl = lookup.get_template("index.html")
        return tmpl.render()


class Api(object):
    @cherrypy.expose
    def api(self):
        print 'hi api'


@cherrypy.expose
def rentals(lat =None, long=None, county=None, beds= None):
    item = DaftscrapApiItem()
    # item['area'] = 'Malahide'
    item['county'] = 'Dublin'
    item['lat'] = lat
    item['long'] = long

    items = select_by_county(item, beds)
    neighbours = compute_nearest_neighbour(item, items)
    nearest = []
    if len(neighbours) > 5:
        for item in neighbours[:5]:
            nearest.append(item)
        return json.dumps(nearest)

    else:
        return json.dumps('[]')


@cherrypy.expose
def reports():
    tmpl = lookup.get_template("reports.html")
    return tmpl.render()


@cherrypy.expose
def export():
    tmpl = lookup.get_template("export.html")
    return tmpl.render()


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Set up site-wide config first so we get a log if errors occur.
    cherrypy.config.update({'environment': 'production',
                            'log.error_file': 'site.log',
                            'log.screen': True})

    PATH = os.path.abspath(os.path.dirname(__file__))

    conf = {'/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(PATH, 'html/static'),
        'log.screen': True

    }}

    root = Root()
    root.export = export
    root.reports = reports
    api = Api()
    api.rentals = rentals

    cherrypy.tree.mount(root, '/', config=conf)
    cherrypy.tree.mount(api, '/api')

    cherrypy.engine.start()
    cherrypy.engine.block()