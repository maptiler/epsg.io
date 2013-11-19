#!/usr/bin/env python
# encoding: utf-8
"""
"""
from bottle import route, run, template, request
import urllib2
import urllib


import sys
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.query import *


@route('/')
def index():
  return template('search')
  
@route('/epsg',method="POST")
def index():
  ix = open_dir("../index")
  result = []
  with ix.searcher(closereader=False) as searcher:
    parser = MultifieldParser(["code","name","area","type"], ix.schema)
    query = request.POST.get('fulltext').strip()
    select = request.POST.get('type').strip()
    status = request.POST.get('invalid')
    print status, "status"
    if status == None:
      status = u"Valid"
    print status, "status2"
    
    query = query + " type:" + select + " status:" + status # change status from id tu text
    print query
    myquery = parser.parse(query)
        
    results = searcher.search(myquery, limit = 600)
    
    num_results = len(results)
    
    for r in results:
      result.append(r)    
    
  return template('results',result=result, query=query,num_results=num_results)
  
run(host='localhost', port=8080)
  