import os
from Cherry.Miner.DataMiner import select_by_county
from DaftScraper.items import DaftscrapedItem, DaftscrapApiItem

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
def rentals():
    item = DaftscrapApiItem()
    item['area'] = 'Dublin'
    items = select_by_county(item)
    return str(len(items)) + ' Length'

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
        'tools.staticdir.dir': os.path.join(PATH, 'static'),
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