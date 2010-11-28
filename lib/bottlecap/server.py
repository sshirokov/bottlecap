import bottle
from bottlecap.application import app

def run(addr, port, **kwargs):
    bottle.run(app=app, host=addr, port=port,
               **dict({'reloader': kwargs.pop('reload', True), 
                       'interval': kwargs.pop('reload_interval', 1)},
                      **kwargs))

