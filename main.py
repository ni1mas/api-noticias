# -*- coding: utf-8 -*-
from flask import Flask, jsonify, make_response, request, current_app
from eventregistry import *
from datetime import datetime, timedelta
from functools import update_wrapper
app = Flask(__name__)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def receiveNews():
    er = EventRegistry(apiKey = "7f142189-e6b0-43b0-b66e-f2850b866caf")
    q = QueryArticles(conceptUri = er.getConceptUri("Violencia de género"))
    q.addRequestedResult(RequestArticlesInfo(returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(bodyLen = -1, image = True, location = True, socialScore = True))))
    return er.execQuery(q)

last_date = datetime.now()
res = receiveNews()
@app.route('/')
@crossdomain(origin='*')
def hello_world():
    global last_date, res
    current_date = datetime.now()
    if (current_date - last_date).total_seconds() > 60*60:
        last_date = current_date
        res = receiveNews()
    return jsonify(res)


if __name__ == '__main__':
    app.run()
