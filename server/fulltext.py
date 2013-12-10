#!/usr/bin/env python
# encoding: utf-8
"""
"""
INDEX = "../index"

from bottle import route, run, template, request, response,static_file
import urllib2
import urllib


import sys
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.query import *
from whoosh import sorting, qparser, scoring,index, highlight,sorting,collectors
import re
from pprint import pprint

from pygments.lexer import RegexLexer
from pygments.token import *
from pygments import highlight
from pygments.formatters import HtmlFormatter

from osgeo import osr

import time


class WKTLexer(RegexLexer):
    name = 'wkt'
    aliases = ['wkt']
    filenames = ['*.wkt']

    tokens = {
        'root': [
            (r'\s+', Text),
            (r'[{}\[\]();,-.]+', Punctuation),
            (r'(PROJCS)\b', Generic.Heading),
            (r'(PARAMETER|PROJECTION|SPHEROID|DATUM|GEOGCS|AXIS)\b', Keyword),
            (r'(PRIMEM|UNIT|TOWGS84)\b', Keyword.Constant),
            (r'(AUTHORITY)\b', Name.Builtin), 
            (r'[$a-zA-Z_][a-zA-Z0-9_]*', Name.Other),
            (r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+', Number.Integer),
            (r'"(\\\\|\\"|[^"])*"', String.Double),
            (r"'(\\\\|\\'|[^'])*'", String.Single),
        ]
    }
    
def area_to_url(area):
  if area.rfind("-"):
    qarea = area.split(" -")[:1]
  elif area.rfind(";"):
    qarea = area.split(";")
  else:
    qarea = area
  url = "/?q=" + urllib.quote_plus(qarea[0].encode('utf-8')) + "&valid=0" +"&kind=*"
  
  return url

@route('/',method="GET")
def index():
  
  # Front page without parameters
  if (len(request.GET.keys()) == 0):
    print len(request.GET.keys())
    return template('search')
  
  class PopularityWeighting(scoring.BM25F):
     use_final = True
     def final(self, searcher, docnum, score):
       
       popularity = (searcher.stored_fields(docnum).get("popularity"))
       #print score, popularity
       return score * popularity
  
  ix = open_dir(INDEX)
  result = []
  
  with ix.searcher(closereader=False, weighting=PopularityWeighting()) as searcher:
  #with ix.searcher(closereader=False) as searcher:

         
    parser = MultifieldParser(["tgrams","code","name","trans","code_trans","kind","area","alt_name","wkt"], ix.schema) #,"wkt"
    parser.add_plugin(qparser.FuzzyTermPlugin()) #jtss~ #jtks~2 #page 40
    query = request.GET.get('q') # p43 - 1.9 The default query language
    #query = query.replace("EPSG::","").replace("EPSG:","").replace("::"," ").replace("."," ").replace(":"," ").replace("-"," ").replace(",,"," ").replace(","," ").replace("   "," ").replace("  ", " ")
    #select = request.GET.get('kind')
    #status = request.GET.get('valid')

    """
    if status == None or status == "1":
      advance_query = query + " kind:" + select + " deprecated:1" #only invalid
      catquery = query + " kind:*" + " deprecated:1"
      
      # able to show number of opposite results group by status
      statquery = query + " kind:*" + " deprecated:0"
    else:
      advance_query = query + " kind:" + select + " deprecated:" + status # only valid
      catquery = query + " kind:*" + " deprecated:0"
      statquery = query + " kind:*" + " deprecated:1"
    """
    deprecated = 0

    if "deprecated:1" in query:
     deprecated = 1
     statquery = re.sub(r'deprecated:1','deprecated:0',query)
     statquery = re.sub(r'kind:([\*\w-]+)',"kind:*",query) 
        
    elif "deprecated:0" in query:
      statquery = re.sub(r'deprecated:0','deprecated:1',query)
      statquery = re.sub(r'kind:([\*\w-]+)',"kind:*",query) 
      
    if not "deprecated" in query:
     query = query + " deprecated:0"
     statquery = re.sub(r'deprecated:0','deprecated:1',query)
     statquery = re.sub(r'kind:([\*\w-]+)',"kind:*",query) 
     

    if not "kind" in query:
      query = query + " kind:*"
      catquery = query + " kind=*"
      statquery = statquery + " kind:*"
    
    catquery = re.sub(r'kind:([\*\w-]+)',"kind:*",query)
    print statquery
    
    
    kind = ""
    p = re.findall(r'kind:([\*\w-]+)',query)
    kind = p[0]
    print "kind"
    print kind

    
    
    only_query = query.split(' ')[:1]
    url_only_query = urllib2.quote(only_query[0])
    
   # if query != "":
  #    query = query + "~"

    #pagenum = int(1)
    # = int(10)
    pagenum = int(request.GET.get("page",1))
    #pagelen = int(request.GET.get("perpage",10))
    
    
    myquery = parser.parse(query)

    mycatquery = parser.parse(catquery)
    mystatquery = parser.parse(statquery)
    url_query = urllib2.quote(query)
    
    facets = sorting.Facets()
    facets.add_field("kind",maptype=sorting.Count)
    facets.add_field("deprecated",maptype=sorting.Count)
    
    start = time.clock()
#####    # first method for all 2.2s
    res_facets = searcher.search(mycatquery , limit = 1, groupedby="kind",scored=False,sortedby=None,maptype=sorting.Count)   # ,limit = 50
    res_facetss = searcher.search(mystatquery , limit = 1, groupedby="deprecated",scored=False,sortedby=None,maptype=sorting.Count)   # ,limit = 50
    
#####   # second method    for all 11s
    #uc = collectors.UnlimitedCollector()
    #fc = collectors.FacetCollector(uc, facets)
    #res_facets = searcher.search_with_collector(mycatquery, fc)
    #print(fc.facetmaps)

####    # third method for all 11s
    #uc = collectors.TopCollector(limit=50000)
    #fc = collectors.FacetCollector(uc, facets)
    #res_facets = searcher.search_with_collector(mycatquery, fc)
    #print(fc.facetmaps)
####    # fourth method



    

#### results of documents

    results = searcher.search_page(myquery, pagenum, pagelen=10)
    #print results
    #print("Showing results %d-%d of %d" % (results.offset +1, results.offset + results.pagelen + 1, len(results))) 
    #categories = searcher.search(mycatquery, groupedby="kind" ,maptype=sorting.Count)   # ,limit = 50
    #print categories
    #status_group = searcher.search(mystatquery, groupedby="status" ,maptype=sorting.Count)   # ,limit = 50
    #print status_group
    #groups = categories.groups("kind")
    #status_groups = status_group.groups("status")
    elapsed = (time.clock() - start)
    #print elapsed
    groups = res_facets.groups("kind")
    #print groups
    status_groups = res_facetss.groups("deprecated")
    #print status_groups
    num_results = len(results) #results.estimated_length()
    

#    print results
    for r in results: #[:20]
      if r['primary'] == 0 and r['code_trans'] !=0:
        link = str(r['code']) + "-" + str(r['code_trans'])
    
      elif r['primary'] == 1 or r['code_trans'] == 0:
        link = str(r['code'])

      
      result.append({'r':r, 'link':link})
      
        
  return template('results',result=result,res_facets=res_facets, groups = groups, num_results=num_results, url_query=url_query, status_groups=status_groups, query=query, url_only_query=url_only_query, pagenum=pagenum,elapsed=elapsed,deprecated=deprecated,kind=kind)#,,,,pagelen=pagelen


@route('/<id:re:[\d]+(-[\d]+)?>/')
def index(id):
  class PopularityWeighting(scoring.BM25F):
     use_final = True
     def final(self, searcher, docnum, score):
       
       popularity = (searcher.stored_fields(docnum).get("popularity"))
       #print score, popularity
       return score * popularity
  
  ix = open_dir(INDEX)
   
  with ix.searcher(closereader=False, weighting=PopularityWeighting()) as searcher:
  
  
  #ix = open_dir(INDEX)
  
  #with ix.searcher(closereader=False) as searcher:
    parser = MultifieldParser(["code","code_trans"], ix.schema)
    
    code, code_trans = (id+'-0').split('-')[:2]
    query = "code:" + code
    myquery = parser.parse(query)
    
    results = searcher.search(myquery, limit=None) #default limit is 10 , reverse = True
    #print results
    item = ""
    trans = []
    num_results = 0
        
    for r in results:
      #print r
      if code_trans == str(0) and r['primary']==1:
        code_trans = r['code_trans']
     
      default = False
      if r['primary']==1: default = True
      
      if r['code_trans'] == int(code_trans):  
        item = r
        link = ""
        url_format = "/"+code+"-"+str(code_trans)
        
      
      else:
        link = str(r['code']) + u"-" + str(r['code_trans'])

      trans.append({
        'link':link,
        'deprecated':r['deprecated'],
        'area_trans':r['area_trans'],
        'accuracy':r['accuracy'],
        'code_trans':r['code_trans'],
        'trans_remarks':r['trans_remarks'],
        'default':default})
      num_results = len(trans)
    
    #print item
    url_method = "/?q=" + urllib.quote_plus(item['method'].encode('utf-8')) + " deprecated=0 kind:METHOD"
    title = item['kind'] + ":" + item['code']
    center = 0,0
    g_coords = ""
    #print item['bbox']
    if item['bbox']:
        #(51.05, 12.09, 47.74, 22.56)
      center = ((item['bbox'][0] - item['bbox'][2])/2.0)+item['bbox'][2],((item['bbox'][3] - item['bbox'][1])/2.0)+item['bbox'][1]
      g_coords = str(item['bbox'][2]) + "," + str(item['bbox'][1]) + "|" + str(item['bbox'][0]) + "," + str(item['bbox'][1]) + "|" + str(item['bbox'][0]) + "," + str(item['bbox'][3]) + "|" + str(item['bbox'][2]) + "," + str(item['bbox'][3]) + "|" + str(item['bbox'][2]) + "," + str(item['bbox'][1])
      #print center
      #print item['bbox'][0]
      #print item['bbox'][2]
      #print ((item['bbox'][0] - item['bbox'][2])/2.0)+item['bbox'][2]
      
     # print item['bbox'][1]
     # print item['bbox'][3]
     # print ((item['bbox'][3] - item['bbox'][1])/2.0)+item['bbox'][1]
    url_area = area_to_url(item['area'])
    url_area_trans = area_to_url(item['area_trans'])
    
    trans_coords = "" 
    if item['wkt'] != None:

      #print '!!!!%s!!!!' % item['wkt'], type(item['wkt'])

      ref = osr.SpatialReference()
      #ref.ImportFromEPSG(5513)
      ref.ImportFromWkt(item['wkt'].encode('utf-8'))
      #ref.ImportFromEPSG(5514)
      #ref.SetAuthority("PROJCS","EPSG","5514")
      #ref.SetFromUserInput(item['wkt'].encode('utf-8'))
      
      
      wgs = osr.SpatialReference()
      wgs.ImportFromEPSG(4326)
     # print ref, type(ref)
      xform = osr.CoordinateTransformation(wgs,ref)
      
      
      #print center[0], type(center[0]), center[1], type(center[1])
      try:
        trans_coords = xform.TransformPoint(center[0], center[1])
      except:
        trans_coords = "" 
        
      export = highlight(ref.ExportToPrettyWkt(), WKTLexer(), HtmlFormatter(cssclass='syntax',nobackground=True))
       
  return template('detailed', item=item, trans=trans, num_results=num_results, url_method=url_method, title=title, url_format=url_format, export=export, url_area_trans=url_area_trans, url_area=url_area, center=center, g_coords=g_coords,trans_coords=trans_coords )  


@route('/<id:re:[\d]+(-[\w]+)>/')
def index(id):
  ix = open_dir(INDEX)

  with ix.searcher(closereader=False) as searcher:
    parser = QueryParser("code", ix.schema)
    myquery = parser.parse(id)
    results = searcher.search(myquery)
    item = ""
    detail = []
    url_area = ""
    url_uom = ""
    url_children = ""
    url_prime = ""
    url_axis = []
    
    
    for r in results:
      item = r

      url_area = area_to_url(item['area'])

      if 'target_uom' in r:
        if r['target_uom'] != 0:
          if r['target_uom'] == 9102:
            url_uom = "/9101-units/"
          elif r['target_uom'] == 9101:
            url_uom = "/9101-units/"
          elif r['target_uom'] == 9001:
            url_uom = "/9001-units/"
          elif r['target_uom'] == 9201:
            url_uom = "/9201-units/"
     
      if 'prime_meridian' in r:
        if r['prime_meridian'] !=0:
          url_prime = str(r['prime_meridian'])+ "-primemeridian/"

      if 'children_code' in r:
        if r['children_code'] != 0:
          if r['kind'].startswith("Datum-"):
            url_children = str(r['children_code']) + "-ellipsoid/"
          elif r['kind'] == "Axis":
            url_children = str(r['children_code']) +"-coordsys/"
          elif r['kind'].startswith("CoordSys-"):
            for c in r['children_code']:
              url = str(c) + "-axis"
              url_axis.append(url)
              
      detail.append({'url_prime': url_prime, 'url_children':url_children,'url_axis':url_axis, 'url_uom':url_uom, 'url_area' : url_area})
      
 
  return template('detailed_word', item=item, detail=detail)  


@route('/<id:re:[\d]+(-[\d]+)?>/<format>')
def index(id, format):
  #print id
  ix = open_dir(INDEX)
  result = []
  export = ""

  with ix.searcher(closereader=False) as searcher:
    parser = MultifieldParser(["code","code_trans"], ix.schema)

    code, code_trans = (id+'-0').split('-')[:2]
    query = "code:"+ code +" code_trans:" + code_trans
    myquery = parser.parse(query)
    result = searcher.search(myquery)[0]
    type = "EPSG"
    
    from osgeo import gdal, osr, ogr
    ref = osr.SpatialReference()
    ref.ImportFromWkt(result['wkt'])


    ct = "text/plain" 
    if format == "esriwkt":
      ref.MorphToESRI()
      export = ref.ExportToWkt()
      ct = "text/x-esriwkt"
    elif format == "prettywkt":
      export = ref.ExportToPrettyWkt()
    elif format == "usgs":
      export = str(ref.ExportToUSGS())
    elif format == "wkt":
      export = ref.ExportToWkt()
    elif format == "proj4":
      export = ref.ExportToProj4()
    elif format == 'html':
      out = ref.ExportToPrettyWkt()
      export = highlight(out, WKTLexer(), HtmlFormatter(cssclass='syntax',nobackground=True))
      response.content_type = 'text/html; charset=UTF-8'
      return template('export', export = export,code=code)
    elif format == 'gml':
      export = ref.ExportToXML()
      ct = "text/gml" 
    elif format == 'usgs':
      export = str(ref.ExportToUSGS())
    elif format == 'mapfile':
      export = 'PROJECTION\n\t'+'\n\t'.join(['"'+l.lstrip('+')+'"' for l in ref.ExportToProj4().split()])+'\nEND' ### CSS: white-space: pre-wrap
    elif format == 'mapnik': 
      proj4 = ref.ExportToProj4().strip()
      export = '<?xml version="1.0" encoding="utf-8"?>\n<Map srs="%s">\n\t<Layer srs="%s">\n\t</Layer>\n</Map>' % (proj4,proj4)
      ct = "application/xml" 
    elif format == 'mapserverpython':
      wkt = ref.ExportToWkt()
      export = "wkt = '''%s'''\nm = mapObj('')\nm.setWKTProjection(wkt)\nlyr = layerObj(m)\nlyr.setWKTProjection(wkt)" % (wkt) #from mapscript import mapObj,layerObj\n
    elif format == 'mapnikpython': 
      proj4 = ref.ExportToProj4().strip()
      export = "proj4 = '%s'\nm = Map(256,256,proj4)\nlyr = Layer('Name',proj4)" % (proj4) #from mapnik import Map, Layer\n
    elif format == 'geoserver':
      export = "%s=%s" % (code,ref.ExportToWkt()) # put this custom projection in the 'user_projections' file inside the GEOSERVER_DATA_DIR '\n' # You can further work with your projections via the web admin tool.\n
      # we'll assume Geotools has this SRS...
    elif format == 'postgis':                                              
      export = 'INSERT into spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext) values ( %s, \'%s\', %s, \'%s\', \'%s\');' % (code, type, code, ref.ExportToProj4(), ref.ExportToWkt())                                                  
    elif format == 'json':
      if ref.IsGeographic():
        code = ref.GetAuthorityCode("GEOGCS")
      else:
        code = ref.GetAuthorityCode("PROJCS")
      export = {}
      if code:
        export['type'] = 'EPSG'
      export['properties'] = {'code':code}
      ct = "application/json" 
    elif format == 'prj':
      ref.MorphToESRI()
      export = ref.ExportToWkt()
      response['Content-disposition'] = "attachment; filename=%s.prj" % code 
    elif format == 'ogcwkt':
      export = ref.ExportToWkt()
  
  response['Content-Type'] = ct 
  return export
  
@route('/about')
def index():
  return template('about')

@route('/css/<filename>')
def server_static(filename):
    return static_file(filename, root='./css/')

    
@route('/<id:re:[\d]+(-[\d]+)?>/coordinates/')
def index(id):
  
  ix = open_dir(INDEX)
  result = []
  try:
    wgs = request.GET.get('wgs')
    w = re.findall(r'(-?\d+\.?\d*)',wgs)

    coord_lat = float(w[0])
    coord_lon = float(w[1])

  except:
    coord_lat = None
    coord_lon = None

  
  
  try:
    other = request.GET.get('other')
    o = re.findall(r'(-?\d+\.?\d*)',other)

    coord_lat_other = float(o[0])

    coord_lon_other = float(o[1])
  except:
    coord_lat_other = None
    coord_lon_other = None
  
  with ix.searcher(closereader=False) as searcher:
    parser = MultifieldParser(["code","code_trans"], ix.schema)

    code, code_trans = (id+'-0').split('-')[:2]
    query = "code:"+ code +" code_trans:" + code_trans
    myquery = parser.parse(query)
    result = searcher.search(myquery)[0]
    trans_wgs = "" 
    trans_other = ""
    from osgeo import gdal, osr, ogr
    ref = osr.SpatialReference()

    ref.ImportFromWkt(result['wkt'].encode('utf-8'))

    wgs = osr.SpatialReference()
    wgs.ImportFromEPSG(4326)
    if coord_lat != None:
      xform = osr.CoordinateTransformation(wgs, ref)
      trans_wgs = xform.TransformPoint(coord_lat, coord_lon)
    elif coord_lat_other != None:
      xform = osr.CoordinateTransformation(ref, wgs)
      trans_other = xform.TransformPoint(coord_lat_other, coord_lon_other)
      
  
  return template ('coordinates', trans_wgs=trans_wgs, trans_other=trans_other, result=result,coord_lat=coord_lat,coord_lon=coord_lon,coord_lat_other=coord_lat_other,coord_lon_other=coord_lon_other)

run(host='0.0.0.0', port=82)
  