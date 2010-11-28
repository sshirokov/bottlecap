import sys, os
from optparse import OptionParser
import bottlecap.server as server

def options_arguments_and_parser():
    parser = OptionParser()
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
    return options.__dict__, args, parser


def main():
    options, args, parser = options_arguments_and_parser()
    host, port = options.pop('addr'), options.pop('port')
    pretend = options.pop('pretend')

    import bottlecap.routes.static

    if not pretend:
        import bottle
        from bottlecap.application import app

        bottle.debug(options.pop('debug', True))
        app.config.update(media_root=options.pop('media'))

        server.run(host, port, **options)
    else:
        print "Would listen on %s:%s" % (host, port)
        print "-> Would mount / => %s" % options['media']
        print "Options:", options


if __name__ == '__main__': main()
