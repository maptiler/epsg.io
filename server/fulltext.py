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
from whoosh import sorting, qparser, scoring,index, highlight
import re
from pprint import pprint

@route('/',method="GET")
def index():
  
  # Front page without parameters
  if (len(request.GET.keys()) == 0):
    return template('search')
  
  class PopularityWeighting(scoring.BM25F):
     use_final = True
     def final(self, searcher, docnum, score):
       
       popularity = (searcher.stored_fields(docnum).get("popularity"))
       #print score, popularity
       return score * popularity
  
  ix = open_dir("../index")
  result = []
  
  with ix.searcher(closereader=False, weighting=PopularityWeighting()) as searcher:
  #with ix.searcher(closereader=False) as searcher:

         
    parser = MultifieldParser(["code","name","trans","wkt","code_trans","kind","area"], ix.schema) #
    parser.add_plugin(qparser.FuzzyTermPlugin()) #jtss~ #jtks~2 #page 40
    
    
    
    query = request.GET.get('q') # p43 - 1.9 The default query language
    
    select = request.GET.get('kind')
    status = request.GET.get('valid')
    print status
    
    if status == None:
      advance_query = query + " kind:" + select
    else:
      advance_query = query + " kind:" + select + " status:" + status
      
       
   # if query != "":
  #    query = query + "~"
      
    myquery = parser.parse(advance_query)

                             
    results = searcher.search(myquery, limit = 50, groupedby="kind", maptype=sorting.Count)   
    groups = results.groups()
    #print groups
    

    
    
    #if query == "" or query == "*":
    #  query = "All records"
    
    num_results = len(results)
    
    for r in results[:20]:
      result.append(r)
      #print r['code']
      
  return template('results',result=result, groups = groups, query=query,num_results=num_results, advance_query=advance_query, kind=select,status=status)


@route('/<id:re:[\d]+(-[\w]+)?>/')
def index(id):
  ix = open_dir("../index")
  result = []
  
  with ix.searcher(closereader=False) as searcher:
    parser = MultifieldParser(["code","code_trans"], ix.schema)
    
    code, trans_code = (id+'-0').split('-')[:2]
    
    if trans_code == 0:
      query = "code:"+ code +" code_trans:" + trans_code
    else:
      query = "code:"+ code
    
    myquery = parser.parse(query)
            
    results = searcher.search(myquery)
    
    for r in results:
      result.append(r)
      
      #print text

  return template('detailed',result=result)#,XML=XML)  

@route('/<id:re:[\d]+(-[\d]+)?>/<format>')
def index(id, format):
  ix = open_dir("../index")
  result = []
  export = ""

  with ix.searcher(closereader=False) as searcher:
    parser = MultifieldParser(["code","code_trans"], ix.schema)

    code, trans_code = (id+'-0').split('-')[:2]
    query = "code:"+ code +" code_trans:" + trans_code

    myquery = parser.parse(query)

    result = searcher.search(myquery)[0]

    from osgeo import gdal, osr, ogr
    ref = osr.SpatialReference()
    ref.ImportFromWkt(result['wkt'])

    if format == "esriwkt":
      export = ref.MorphToESRI().ExportToPrettyWkt()
    elif format == "prettywkt":
      export = ref.ExportToPrettyWkt()
    elif format == "usgs":
      export = str(ref.ExportToUSGS())
    elif format == "wkt":
      export = ref.ExportToWkt()
    elif format == "proj4":
      export = ref.ExportToProj4()

  return export

run(host='localhost', port=8080)
  