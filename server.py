#!/usr/bin/env python
# -*- coding:utf-8 -*-

from src.common import *
import src.tools as Tool
from tornado import ioloop, web, httpserver
import os

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")


def main():
    parse_command_line()
    app = tornado.web.Application([
        (r"/api/get_domain", DomainListHandler),
        (r"/api/get_record", RecordListHandler),
        (r"/api/create_record", RecordCreateHandler),
        (r"/api/remove_record", RecordRemoveHandler),
        (r"/api/update_record", RecordUpdateHandler),
    ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=False,
        debug=options.debug,
    )
    server = httpserver.HTTPServer(app)
    server.bind(options.port)
    server.start(1)
    print('%s Godaddy server start listening at: %s' % (Tool.current_time(), options.port))
    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
