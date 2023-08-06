# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2019/11/12 21:49
# @author  : Mo
# @function:


import tornado.ioloop
import tornado.web


class calculate(tornado.web.RequestHandler):
    def post(self):
        a = self.get_argument('a')
        b = self.get_argument('b')
        c = int(a) + int(b)
        self.write("c=" + str(c))


application = tornado.web.Application([(r"/test", calculate), ])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()