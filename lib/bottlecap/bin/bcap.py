import sys, os, threading, webbrowser
from optparse import OptionParser
import bottlecap.server as server

def options_arguments_and_parser(usage=None, as_dict=True):
    parser = OptionParser(
        usage=usage and usage.format(default="Usage: %prog [options]")
    )
    parser.add_option("-p", "--port", dest="port", default=6969,
                      type="int",
                      help="PORT to listen on [default: %default]", metavar="PORT")
    parser.add_option("-a", "--addr", dest="addr", default='127.0.0.1',
                      type="string",
                      help="ADDR to listen on [default: %default]", metavar="ADDR")
    parser.add_option('-D', '--no-debug', dest="debug", default=True,
                      action="store_false",
                      help="Disable debug mode.")
    parser.add_option('-R', '--no-reload', dest="reload", default=True,
                      action="store_false",
                      help="Disable autoreloader")
    parser.add_option('-m', '--media', dest="media",
                      default=os.path.join(os.getcwd()),
                      action="store", type="string",
                      help="The root of the media [default: %default]")
    parser.add_option('-P', '--pretend',  default=False,
                      action="store_true",
                      help="Don't run the server, just process the arguments and report")
    (options, args) = parser.parse_args()
    return (options.__dict__ if as_dict else options,
            args,
            parser)


def main():
    import bottlecap.routes.static

    options, args, parser = options_arguments_and_parser("{default} [open_path_in_browser]")
    host, port = options.pop('addr'), options.pop('port')
    pretend = options.pop('pretend')

    if len(args) > 1: parser.error("Too many arguments")
    elif len(args):
        options['open'] = args[0].lstrip('/')
        sys.argv.pop() # Make sure the relaoder won't keep trying to open the URL
    else: options['open'] = False

    def self_url():
        if hasattr(self_url, 'url'): return self_url.url
        (lambda url: setattr(self_url, 'url', url))(
            options['open'] is not(False) and
            'http://{host}:{port}/{url}'.format(host=host, port=port, url=options['open'])
        )
        options.pop('open')
        return self_url()

    if not pretend:
        import bottle
        from bottlecap.application import app

        bottle.debug(options.pop('debug', True))
        app.config.update(media_root=options.pop('media'))

        if self_url():
            threading.Timer(1, lambda: webbrowser.open(self_url())).start()

        server.run(host, port, **options)
    else:
        print "Would listen on %s:%s" % (host, port)
        print "-> Would mount / => %s" % options['media']
        if self_url():
            print "-> Would open browser to", self_url()
        print "Options:", options


if __name__ == '__main__': main()
