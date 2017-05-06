# -*- coding: utf-8 -*-
from flask import Flask
from eventregistry import *
from datetime import datetime
app = Flask(__name__)

def receiveNews():
    er = EventRegistry(apiKey = "7f142189-e6b0-43b0-b66e-f2850b866caf")
    q = QueryArticles(conceptUri = er.getConceptUri("Violencia de género"))
    q.addRequestedResult(RequestArticlesInfo(returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(bodyLen = -1, image = True))))
    return er.execQuery(q)

@app.route('/')
def hello_world():
  return jsonify(receiveNews())    


if __name__ == '__main__':
  app.run()
