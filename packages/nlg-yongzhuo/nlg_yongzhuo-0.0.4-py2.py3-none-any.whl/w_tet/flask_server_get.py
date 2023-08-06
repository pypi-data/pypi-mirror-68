# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/10/12 11:11
# @author   :Mo
# @function :service of flask


# flask
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/test', methods=["GET"])
def calculate():
    a = request.args.get("a", 0)
    b = request.args.get("b", 0)
    c = int(a) + int(b)
    res = {"result": c}
    return jsonify(content_type='application/json;charset=utf-8',
                   reason='success',
                   charset='utf-8',
                   status='200',
                   content=res)

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            threaded=True,
            debug=False,
            port=8080,)
