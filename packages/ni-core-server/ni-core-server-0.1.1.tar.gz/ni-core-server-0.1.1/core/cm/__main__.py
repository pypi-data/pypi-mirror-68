import coloredlogs
import tornado

from core.cm.commandLine import Application

coloredlogs.install(level='DEBUG')

sockets = tornado.netutil.bind_sockets(8888, '')
server = tornado.httpserver.HTTPServer(Application())
server.add_sockets(sockets)

for s in sockets:
    print('Listening on %s, port %d' % s.getsockname()[:2])

tornado.ioloop.IOLoop.instance().start()