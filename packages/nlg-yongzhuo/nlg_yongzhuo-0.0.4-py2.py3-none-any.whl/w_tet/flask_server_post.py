# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/10/12 11:11
# @author   :Mo
# @function :service of flask


# # flask
# from flask import Flask, request, jsonify
#
# app = Flask(__name__)
#
# @app.route('/test', methods=["POST"])
# def calculate():
#     params = request.form if request.form else request.json
#     print(params)
#     a = params.get("a", 0)
#     b = params.get("b", 0)
#     c = a + b
#     res = {"result": c}
#     return jsonify(content_type='application/json;charset=utf-8',
#                    reason='success',
#                    charset='utf-8',
#                    status='200',
#                    content=res)
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0',
#             threaded=True,
#             debug=True,
#             port=8080)




import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        """get请求"""
        a = self.get_argument('a')
        b = self.get_argument('b')
        c  = int(a) + int(b)
        self.write("c=" + str(c))

application = tornado.web.Application([(r"/add", MainHandler), ])

if __name__ == "__main__":
    application.listen(8868)
    tornado.ioloop.IOLoop.instance().start()