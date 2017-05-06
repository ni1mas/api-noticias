# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from eventregistry import *
from datetime import datetime
app = Flask(__name__)

def receiveNews():
  er = EventRegistry(apiKey = "7f142189-e6b0-43b0-b66e-f2850b866caf")
  q = QueryArticles(conceptUri = er.getConceptUri("Violencia de género"))
  q.addRequestedResult(RequestArticlesInfo(returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(bodyLen = -1, image = True))))
  return er.execQuery(q)

last_date = datetime.now()
res = receiveNews()
@app.route('/')
def hello_world():
  global last_date, res
  current_date = datetime.now()
  if (current_date - last_date).total_seconds() > 60*60:
    last_date = current_date
    res = receiveNews()
  return jsonify(res)


if __name__ == '__main__':
  app.run()
