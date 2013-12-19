#!/usr/bin/env python
# encoding: utf-8
"""
"""
INDEX = "./index"

facets_list = [
  ['CRS','CRS','','Coordinate reference systems',0,'http://'],
  ['CRS-PROJCRS','PROJCRS','&nbsp; &nbsp;', 'Projected',0,'http://'],
  ['CRS-GEOGCRS','GEOGCRS','&nbsp; &nbsp;', 'Geodetic',0,'http://'],
  ['CRS-GEOG3DCRS','GEOG3DCRS', '&nbsp; &nbsp;', 'Geodetic 3D',0,'http://'],
  ['CRS-GCENCRS','GCENCRS','&nbsp; &nbsp;', 'Geocentric',0,'http://'],
  ['CRS-VERTCRS','VERTCRS','&nbsp; &nbsp;', 'Vertical',0,'http://'],
  ['CRS-ENGCRS','ENGCRS','&nbsp; &nbsp;', 'Engineering',0,'http://'],
  ['CRS-COMPOUNDCRS','COMPOUNDCRS','&nbsp; &nbsp;', 'Compound',0,'http://'], 
  ['COORDOP','COORDOP','','Operation',0,'http://'],
  ['COORDOP-COPTRANS','COPTRANS','&nbsp; &nbsp;', 'Transformation',0,'http://'],
  ['COORDOP-COPCONOP','COPCONOP','&nbsp; &nbsp;', 'Compound',0,'http://'],
  ['COORDOP-COPCON','COPCON','&nbsp; &nbsp;', 'Conversion',0,'http://'],
  ['DATUM','DATUM','','Datum',0,'http://'],
  ['DATUM-VERTDAT','VERTDAT','&nbsp; &nbsp;', 'Vertical',0,'http://'],
  ['DATUM-ENGDAT','ENGDAT','&nbsp; &nbsp;', 'Engineering',0,'http://'],
  ['DATUM-GEODDAT','GEODDAT','&nbsp; &nbsp;', 'Geodetic',0,'http://'],
  ['ELLIPSOID','ELLIPSOID','', 'Ellipsoid',0,'http://'],
  ['PRIMEM','PRIMEM','', 'Prime meridian',0,'http://'],
  ['METHOD','METHOD','', 'Method',0,'http://'],
  ['CS','CS','', 'Coordinate systems',0,'http://'],
  ['CS-VERTCS','VERTCS','&nbsp; &nbsp;', 'Vertical',0,'http://'],
  ['CS-SPHERCS','SPHERCS','&nbsp; &nbsp;', 'Spherical',0,'http://'],
  ['CS-CARTESCS','CARTESCS','&nbsp; &nbsp;', 'Cartesian',0,'http://'],
  ['CS-ELLIPCS','ELLIPCS','&nbsp; &nbsp;', 'Ellipsoidal',0,'http://'],
  ['AXIS','AXIS','', 'Axis',0,'http://'],
  ['AREA','AREA','', 'Area',0,'http://'],
  ['UNIT','UNIT','', 'Units',0,'http://'],
  ['UNIT-ANGUNIT','ANGUNIT','&nbsp; &nbsp;', 'Angle',0,'http://'],
  ['UNIT-SCALEUNIT','SCALEUNIT','&nbsp; &nbsp;', 'Scale',0,'http://'],
  ['UNIT-LENUNIT','LENUNIT','&nbsp; &nbsp;', 'Length',0,'http://'],
]

# Index to the facets_list above - manual update on change!
f_crs_index = 0
f_op_index = 8
f_datum_index = 12
f_cs_index = 19
f_unit_index = 26

from bottle import route, run, template, request, response, static_file, redirect
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
from osgeo import gdal, osr, ogr
import time
import math
import json



re_kind = re.compile(r'kind:([\*\w-]+)')
re_deprecated = re.compile(r'deprecated:\d')

def getQueryParam(q, param):
  """Return value of a param in query"""
  if param == 'deprecated':
    if "deprecated:1" in q:
      return 1
    else:
      return 0 # default if not present
  if param == 'kind':
    m = re_kind.search(q)
    if m:
      return m.group(1)
    else:
      return "CRS" # default if not present
  m = re.search(param+r':(\S+)', q)
  if m:
    return m.group(1)
  else:
    return ''

def getVerboseQuery(q):
  verboseq = setQueryParam(q, 'deprecated', getQueryParam(q,'deprecated'), True)
  verboseq = setQueryParam(verboseq, 'kind', getQueryParam(verboseq,'kind'), True)
  return verboseq

def setQueryParam(q, param, value='', verbose=False):
  """Set in the query string the param to value"""
  if param == 'deprecated':
    if int(value) != 0:
      if 'deprecated' in q:
        q = re_deprecated.sub('deprecated:1', q)
      else:
        q += " deprecated:1"
    else: # default deprecated:0
      q = re_deprecated.sub('',q)
      if verbose:
        q += " deprecated:0"
  elif param == 'kind':
    if 'kind:' in q:
      q = re_kind.sub("kind:"+value,q)
    else:
      q += " kind:"+value
    if not verbose:
      q = q.replace('kind:CRS','') # default
  elif param in q:
    q = re.sub(param+r':(\S+)',param+":"+str(value), q)
  else:
    q += " "+param+":"+str(value)
  if value == '': # remove param if value is empty
    q = q.replace(param+":", q)
  return re.sub(r'\s+',' ', q).strip()

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
  url = "/?q=" + urllib.quote_plus(qarea[0].encode('utf-8'))
  
  return url

@route('/',method="GET")
def index():

  # Front page without parameters
  if (len(request.GET.keys()) == 0):
    print len(request.GET.keys())
    return template('./templates/search')
  
  class PopularityWeighting(scoring.BM25F):
     use_final = True
     def final(self, searcher, docnum, score):
       
       popularity = (searcher.stored_fields(docnum).get("popularity"))
       code = (searcher.stored_fields(docnum).get("code"))
       #print "code:",code," with score:", score
       return score #* popularity
  
  ix = open_dir(INDEX)
  result = []

  with ix.searcher(closereader=False, weighting=PopularityWeighting()) as searcher:
  #with ix.searcher(closereader=False, weighting=scoring.BM25F) as searcher:
  
    parser = MultifieldParser(["tgrams","code","name","trans","code_trans","kind","area"], ix.schema)
    query = request.GET.get('q')  # p43 - 1.9 The default query language
    pagenum = int(request.GET.get("page",1))
    format = request.GET.get('format',0)
    callback = request.GET.get('callback',False)
    
    kind = getQueryParam(query, 'kind')
    deprecated = getQueryParam(query, 'deprecated')
    
    # for count inverse deprecated (if it display valid, show me a number of deprecated records)
    statquery = setQueryParam(query, 'deprecated', not deprecated,True)
    url_facet_statquery ="/?q=" + urllib2.quote(statquery)
    # and through all kinds
    statquery = setQueryParam(statquery,'kind','*')
    
    # show query in all kinds
    catquery = setQueryParam(query,'kind','*')
    
    # parse and prepare for search
    myquery = parser.parse(getVerboseQuery(query))
    mycatquery = parser.parse(getVerboseQuery(catquery))
    mystatquery = parser.parse(getVerboseQuery(statquery))
    
    # how long, exactly, it will take 
    start = time.clock()
    
    # find a query in all categories
    res_facets = searcher.search(mycatquery , groupedby='kind',scored=False,sortedby=None,maptype=sorting.Count)
    # find a query in inverse deprecated
    res_facetss = searcher.search(mystatquery , groupedby="deprecated",scored=False,sortedby=None,maptype=sorting.Count)
    
    # result of query
    results = searcher.search(myquery, limit = None) #(pagenum*pagelen)
    
    # finish time
    elapsed = (time.clock() - start)
    
    # kind and count of result from catquery
    groups = res_facets.groups("kind")
    # deprecated or not deprecated with count of result from statquery
    status_groups = res_facetss.groups("deprecated")
    
    # number of results on one page. If change number, edit "paging"
    pagelen = 10
    # last document from result on page
    maxdoc = pagelen*pagenum
    json_str = []
    
    for r in results[(maxdoc-pagelen):maxdoc]:
      link = str(r['code'])
      result.append({'r':r, 'link':link})
      json_str.append({'code':r['code'], 'name':r['name'], 'wkt':r['wkt'],'default_trans':r['code_trans'],'alternatives_trans':r['trans'],'area_trans':r['area_trans'],'accuracy':r['accuracy'],'kind':r['kind']})
      
    
    # number of results from results
    num_results = len(results)
    
    # paging ala google
    pagemax = int(math.ceil(num_results / float(pagelen) ))
    paging = range(1, pagemax+1)[ max(0, pagenum-6) : (pagenum+4 if pagenum >= 10 else min(10,pagemax))]
    
    # set all facets_list counts to zero 
    for i in range(0,len(facets_list)):
      facets_list[i][4] = 0
    
    #make null index of chose kind  
    query_kind_index = None
    
    # update facets counters
    for key,value in groups.iteritems():
        
      # standard kinds
      for i in range(0,len(facets_list)):
        if facets_list[i][0] == key:
          facets_list[i][4] = int(value)
          catquery = setQueryParam(catquery, 'kind', facets_list[i][1])
          facets_list[i][5] = "/?q=" + urllib2.quote(catquery)
          
          # index of chose kind 
          if kind == facets_list[i][1]:
            query_kind_index = i

      # sum special kinds
      if key.startswith('CRS-'):
        facets_list[f_crs_index][4] += int(value)
        catquery = setQueryParam(catquery, 'kind', facets_list[f_crs_index][1])
        facets_list[f_crs_index][5] = "/?q=" + urllib2.quote(catquery)

      if key.startswith('DATUM-'):
        facets_list[f_datum_index][4] += int(value)
        catquery = setQueryParam(catquery, 'kind', facets_list[f_datum_index][1])
        facets_list[f_datum_index][5] = "/?q=" + urllib2.quote(catquery)
        
      if key.startswith('CS-'):
        facets_list[f_cs_index][4] += int(value)
        catquery = setQueryParam(catquery, 'kind', facets_list[f_cs_index][1])
        facets_list[f_cs_index][5] = "/?q=" + urllib2.quote(catquery)
        
      if key.startswith('UNIT-'):
        facets_list[f_unit_index][4] += int(value)
        catquery = setQueryParam(catquery, 'kind', facets_list[f_unit_index][1])
        facets_list[f_unit_index][5] = "/?q=" + urllib2.quote(catquery)

      if key.startswith('COORDOP-'):
        facets_list[f_op_index][4] += int(value)
        catquery = setQueryParam(catquery, 'kind', facets_list[f_op_index][1])
        facets_list[f_op_index][5] = "/?q=" + urllib2.quote(catquery)
    
    # show a clear query (e.g. without kind:CRS, deprecated:0)
    query = setQueryParam(query,'kind',kind)
    query = setQueryParam(query,'deprecated',deprecated)
    export = {}
    if str(format) == "json":
      export['number_result']= num_results
      export['results'] = json_str
      json_str = export
      response['Content-Type'] = "application/json"
      if callback:
        json_str = callback + "(" + str(json_str) + ")"
        response['Content-Type'] = "application/javascript"
        return json.dumps(json_str)
      
      return json.dumps(json_str)

  return template('./templates/results',query=query,deprecated=deprecated, num_results=num_results, elapsed=elapsed, facets_list=facets_list, status_groups=status_groups, url_facet_statquery=url_facet_statquery, result=result, pagenum=int(pagenum),paging=paging)



@route('/<id:re:[\d]+(-[\d]+)?>')
def index(id):
  class PopularityWeighting(scoring.BM25F):
     use_final = True
     def final(self, searcher, docnum, score):
       popularity = (searcher.stored_fields(docnum).get("popularity"))
       return score# * popularity
  ix = open_dir(INDEX)
   
  with ix.searcher(closereader=False, weighting=PopularityWeighting()) as searcher:
    parser = MultifieldParser(["code","code_trans"], ix.schema)
  
    code, code_trans = (id+'-0').split('-')[:2]
    
    query = "code:" + code + " kind:CRS OR kind:COORDOP" #1068-datum, 1068-area,1068 (transformation)
    myquery = parser.parse(query)
    results = searcher.search(myquery, limit=None) #default limit is 10 , reverse = True
    
    trans = []
    url_trans = []
    trans_item = []
    num_results = 0
    # item = None
    #wkt = None
    # default_trans = ""
    # url_method = ""
    url_format = ""
    export = ""
    # url_area_trans = ""
    # url_area = ""
    # g_coords = ""
    # center = 0,0
    trans_coords = ""
    # title = ""
    nadgrid = None
    
    for r in results:
      found = False
      item = r
      title = item['kind'] + ":" + item['code']
      url_area = area_to_url(item['area'])
      wkt = item['wkt']
      # for short link (5514, instead of 5514-15965)
      if int(code_trans) == 0 and int(r['code_trans']) != 0:
        code_trans = r['code_trans']
      #if it default transformation code or has some other transformations
      if int(code_trans) != 0 or r['trans']:
        # it is at least one code of transformation (min. defalut trans. code)
        for code_transformation in r['trans']:

          parser = MultifieldParser(["code","kind"], ix.schema)
          query = "code:"+str(code_transformation)+ " kind:COORDOP"
          myquery = parser.parse(query)
          transformation = searcher.search(myquery, limit=None)
          for hit in transformation:
            trans_item.append(hit)
            # if it active do not show a link
            if int(hit['code']) == int(code_trans):  
              link = ""
            else:
              link = str(r['code']) + u"-" + str(hit['code'])
            
            # if exist default trans code
            default = False
            if int(r['code_trans'])== int(hit['code']): 
              default = True
            
            # safe the main information about each transformation
            trans.append({
            'link':link,
            'code':hit['code'],
            'deprecated':hit['deprecated'],
            'area_trans':hit['area'],
            'accuracy':hit['accuracy'],
            'code_trans':hit['code'],
            'trans_remarks':hit['remarks'],
            'default':default})
      
      # if it has NOT default transformation code
      else:
        ref = osr.SpatialReference()
        ref.ImportFromEPSG(int(r['code']))
        if ref.GetTOWGS84() != None:
          found = True
          default_trans = item
      
      # if it has any transformation
      if found == False:
        
        # default trans is active transformation
        for i in range(0,len(trans_item)):
          found_dt = False
          if str(code_trans) == str(trans_item[i]['code']):
            default_trans = trans_item[i]
            found_dt = True
          elif str(code_trans) != str(trans_item[i]['code']) and not found:
            default_trans = trans_item[0]

        if trans_item and default_trans:
          
          # from values of TOWGS84 edit wkt of CRS
          values = default_trans['wkt']
          if re.findall(r'([a-zA-Z_])',values):
            nadgrid = default_trans['wkt']
          else:
            num =[]
            w = re.findall(r'(-?\d+\.?\d*)',values)
          
            for n in w:
              num.append(float(n))
            values = tuple(num)     
            #print values
            # do not change default TOWGS84
            if int(r['code_trans']) != int(default_trans['code']) :
            
              if (values != (0,0,0,0,0,0,0) and type(values) == tuple and values != (0,)):            
                ref = osr.SpatialReference()
                ref.ImportFromEPSG(int(r['code']))
                ref.SetTOWGS84(*values) 
                wkt = ref.ExportToWkt().decode('utf-8')
        # if do not have trans_item or default_trans    
        else:
          center = ((item['bbox'][0] - item['bbox'][2])/2.0)+item['bbox'][2],((item['bbox'][3] - item['bbox'][1])/2.0)+item['bbox'][1]
          g_coords = str(item['bbox'][2]) + "," + str(item['bbox'][1]) + "|" + str(item['bbox'][0]) + "," + str(item['bbox'][1]) + "|" + str(item['bbox'][0]) + "," + str(item['bbox'][3]) + "|" + str(item['bbox'][2]) + "," + str(item['bbox'][3]) + "|" + str(item['bbox'][2]) + "," + str(item['bbox'][1])
    
    # if it CRS (not transformation)
    if str(item['kind']).startswith('CRS'):
      if item['wkt']:
        url_format = "/"+str(item['code'])
        if int(default_trans['code']) != int(item['code']):
          url_format = "/"+str(item['code'])+"-"+str(default_trans['code'])
    
    # for activated transformation
    if default_trans:
      url_method ="/?q=" + urllib.quote_plus((default_trans['method']+ ' kind:METHOD').encode('utf-8'))
      url_area_trans = area_to_url(default_trans['area'])
      center = 0,0
      g_coords = ""
      if default_trans['bbox']:
        #(51.05, 12.09, 47.74, 22.56)
        center = ((default_trans['bbox'][0] - default_trans['bbox'][2])/2.0)+default_trans['bbox'][2],((default_trans['bbox'][3] - default_trans['bbox'][1])/2.0)+default_trans['bbox'][1]
        g_coords = str(default_trans['bbox'][2]) + "," + str(default_trans['bbox'][1]) + "|" + str(default_trans['bbox'][0]) + "," + str(default_trans['bbox'][1]) + "|" + str(default_trans['bbox'][0]) + "," + str(default_trans['bbox'][3]) + "|" + str(default_trans['bbox'][2]) + "," + str(default_trans['bbox'][3]) + "|" + str(default_trans['bbox'][2]) + "," + str(default_trans['bbox'][1])
    
    # if available wkt, default_trans and wkt has length minimum 100 characters (transformation has length maximum 100 (just a TOWGS84))
    if wkt and default_trans and len(wkt)>100:
      trans_coords = ""         
      ref = osr.SpatialReference()
      ref.ImportFromWkt(wkt.encode('utf-8'))
      
      wgs = osr.SpatialReference()
      wgs.ImportFromEPSG(4326)
      
      xform = osr.CoordinateTransformation(wgs,ref)

      try:
        trans_coords = xform.TransformPoint(center[0], center[1])
      except:
        trans_coords = "" 
      # color html of pretty wkt
      export = highlight(ref.ExportToPrettyWkt(), WKTLexer(), HtmlFormatter(cssclass='syntax',nobackground=True))
    # if the CRS has 
    url_concatop=[]
    if default_trans['concatop'] != []:
      for i in range(0,len(default_trans['concatop'])):
        url_concatop.append("/"+ str(default_trans['concatop'][i]) + "/")
  return template('./templates/detail', item=item, trans=trans,default_trans=default_trans, num_results=num_results, url_method=url_method, title=title, url_format=url_format, export=export, url_area_trans=url_area_trans, url_area=url_area, center=center, g_coords=g_coords, trans_coords=trans_coords,wkt=wkt,facets_list=facets_list,url_concatop=url_concatop, nadgrid=nadgrid )  


@route('/<id:re:[\d]+(-[\w]+)>')
def index(id):
  ix = open_dir(INDEX)
  with ix.searcher(closereader=False) as searcher:
    
    parser = QueryParser("code", ix.schema)
    myquery = parser.parse(id)
    results = searcher.search(myquery)
    url_axis = []
    detail = []
    url_uom = ""
    url_children = ""
    url_prime = ""
    # item = ""
    # url_area = ""

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
          if r['kind'].startswith("DATUM"):
            url_children = str(r['children_code']) + "-ellipsoid/"
          
          elif r['kind'] == "AXIS":
            url_children = str(r['children_code']) +"-coordsys/"
          
          elif r['kind'].startswith("CS"):
            for c in r['children_code']:
              url = str(c) + "-axis"
              url_axis.append(url)
              
      detail.append({'url_prime': url_prime, 'url_children':url_children,'url_axis':url_axis, 'url_uom':url_uom, 'url_area' : url_area})
      
 
  return template('./templates/detail_alt', item=item, detail=detail, facets_list=facets_list)  


@route('/<id:re:[\d]+(-[\d]+)?>/<format>')
def index(id, format):
  ix = open_dir(INDEX)
  result = []
  export = ""
  values = ""
  ref = osr.SpatialReference()
  
  with ix.searcher(closereader=False) as searcher:
    parser = QueryParser("code", ix.schema)

    code, code_trans = (id+'-0').split('-')[:2]

    code_query = parser.parse(str(code) + " kind:CRS OR kind:COORDOP")
    code_result = searcher.search(code_query, sortedby=False,scored=False)

    for r in code_result:
      rcode = r['code']
      wkt = r['wkt']
      rcode = r['code']
      def_trans = r['code_trans']
  
    if int(code_trans) != 0:
      trans_query = parser.parse(str(code_trans) + " kind:COORDOP")
      trans_result = searcher.search(trans_query,sortedby=False,scored=False)
      for t in trans_result:
        values = t['wkt']
        tcode = t['code']
        url_coords = rcode + "-" + tcode 
    else: 
      trans_result = code_result
      url_coords = rcode
    if not re.findall(r'([a-zA-Z_])',values):
      w = re.findall(r'(-?\d+\.?\d*)',values)
      num =[]
      for n in w:
        num.append(float(n))
      values = tuple(num)

      if int(def_trans) != int(tcode):
        if (values != (0,0,0,0,0,0,0) and type(values) == tuple and values != (0,)):
          ref.ImportFromEPSG(int(rcode))
          ref.SetTOWGS84(*values) 
          wkt = ref.ExportToWkt().decode('utf-8')
    
    ref.ImportFromWkt(wkt)

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
      return template('./templates/export', export = export, code=rcode)
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
      mswkt = ref.ExportToWkt()
      export = "wkt = '''%s'''\nm = mapObj('')\nm.setWKTProjection(mswkt)\nlyr = layerObj(m)\nlyr.setWKTProjection(mswkt)" % (mswkt) #from mapscript import mapObj,layerObj\n
    elif format == 'mapnikpython': 
      proj4 = ref.ExportToProj4().strip()
      export = "proj4 = '%s'\nm = Map(256,256,proj4)\nlyr = Layer('Name',proj4)" % (proj4) #from mapnik import Map, Layer\n
    elif format == 'geoserver':
      export = "%s=%s" % (code,ref.ExportToWkt()) # put this custom projection in the 'user_projections' file inside the GEOSERVER_DATA_DIR '\n' # You can further work with your projections via the web admin tool.\n
      # we'll assume Geotools has this SRS...
    elif format == 'postgis':                                              
      export = 'INSERT into spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext) values ( %s, \'%s\', %s, \'%s\', \'%s\');' % (rcode, "EPSG", rcode, ref.ExportToProj4(), ref.ExportToWkt())                                                  
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
      response['Content-disposition'] = "attachment; filename=%s.prj" % rcode 
    elif format == 'ogcwkt':
      export = ref.ExportToWkt()
  
  response['Content-Type'] = ct 
  return export
  

    
@route('/<id:re:[\d]+(-[\d]+)?>/coordinates/')
def index(id):
  ix = open_dir(INDEX)
  result = []
  values = None
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
    parser = QueryParser("code", ix.schema)

    code, code_trans = (id+'-0').split('-')[:2]

    code_query = parser.parse(str(code) + " kind:CRS OR kind:COORDOP")
    code_result = searcher.search(code_query, sortedby=False,scored=False)
    
    for r in code_result:
      def_trans = r['code_trans']
      wkt = r['wkt']
      rcode = r['code']
      rname = r['name']
    
    if int(def_trans) != 0:
      trans_query = parser.parse(str(code_trans) + " kind:COORDOP")
      trans_result = searcher.search(trans_query,sortedby=False,scored=False)
     
      for t in trans_result:
        values = t['wkt']
        tcode = t['code']
        url_coords = rcode + "-" + tcode 
    else: 
      trans_result = code_result
      url_coords = rcode
      
    if values != None:
      w = re.findall(r'(-?\d+\.?\d*)',values)
      num =[]
      for n in w:
        num.append(float(n))
      values = tuple(num) 
      
      if int(def_trans) != int(tcode):
        if (values != (0,0,0,0,0,0,0) and type(values) == tuple):
          ref = osr.SpatialReference()
          ref.ImportFromEPSG(int(rcode))
          ref.SetTOWGS84(*values) 
          wkt = ref.ExportToWkt().decode('utf-8')
        
    trans_wgs = "" 
    trans_other = ""
    
    ref = osr.SpatialReference()
    ref.ImportFromWkt(wkt.encode('utf-8'))

    wgs = osr.SpatialReference()
    wgs.ImportFromEPSG(4326)
    
    if coord_lat != None:
      xform = osr.CoordinateTransformation(wgs, ref)
      trans_wgs = xform.TransformPoint(coord_lat, coord_lon)
    elif coord_lat_other != None:
      xform = osr.CoordinateTransformation(ref, wgs)
      trans_other = xform.TransformPoint(coord_lat_other, coord_lon_other)
      
  return template ('./templates/coordinates', trans_wgs=trans_wgs, trans_other=trans_other, resultcrs=code_result[0], url_coords=url_coords, coord_lat=coord_lat,coord_lon=coord_lon,coord_lat_other=coord_lat_other,coord_lon_other=coord_lon_other)

@route('/trans')
def index():
  tcode_trans_values = None
  scode_trans_values = None
  ix = open_dir(INDEX)
  
  x = float(request.GET.get('x',0))
  y = float(request.GET.get('y',0))
  z = float(request.GET.get('z',0))
  s_srs = request.GET.get('s_srs',4326)
  t_srs = request.GET.get('t_srs',4326)
  callback = str(request.GET.get('callback',0))
  
  #print x,y,z,s_srs,t_srs,callback
  scode, scode_trans = (str(s_srs)+'-0').split('-')[:2]
  tcode, tcode_trans = (str(t_srs)+'-0').split('-')[:2]
    
  with ix.searcher(closereader=False) as searcher:
    parser = QueryParser("code", ix.schema)
    
    if int(scode_trans) == 0:
      scode_query = parser.parse(str(scode) + " kind:CRS")
      scode_result = searcher.search(scode_query, sortedby=False,scored=False)
    
      for r in scode_result:
        swkt = r['wkt']
        scode = r['code']
    
    if int(scode_trans) != 0:
      scode_trans_query = parser.parse(str(scode_trans) + " kind:COORDOP")
      scode_trans_result = searcher.search(scode_trans_query, sortedby=False,scored=False)
    
      for r in scode_trans_result:
        scode_trans_values = r['wkt']
      
      
    if int(tcode_trans) == 0:
      tcode_query = parser.parse(str(tcode) + " kind:CRS")
      tcode_result = searcher.search(tcode_query,sortedby=False,scored=False)
     
      for r in tcode_result:
        twkt = r['wkt']
    
    if int(tcode_trans) != 0:
      tcode_trans_query = parser.parse(str(tcode_trans) + " kind:COORDOP")
      tcode_trans_result = searcher.search(tcode_trans_query, sortedby=False,scored=False)
    
      for r in tcode_trans_result:
        tcode_trans_values = r['wkt']
        
    if scode_trans != 0 and scode_trans_values != None:
      w = re.findall(r'(-?\d+\.?\d*)', scode_trans_values)
      num =[]
      for n in w:
        num.append(float(n))
      values = tuple(num) 
      
      if (values != (0,0,0,0,0,0,0) and type(values) == tuple and values != (0,)):
        ref = osr.SpatialReference()
        ref.ImportFromEPSG(int(scode))
        ref.SetTOWGS84(*values) 
        swkt = ref.ExportToWkt().decode('utf-8')

    
    if int(tcode_trans) != 0 and tcode_trans_values != None:
      w = re.findall(r'(-?\d+\.?\d*)', tcode_trans_values)
      num =[]
      for n in w:
        num.append(float(n))
      values = tuple(num) 

      if (values != (0,0,0,0,0,0,0) and type(values) == tuple and values != (0,)):
        ref = osr.SpatialReference()
        ref.ImportFromEPSG(int(tcode))
        ref.SetTOWGS84(*values) 
        twkt = ref.ExportToWkt().decode('utf-8')

    s_srs = osr.SpatialReference()
    s_srs.ImportFromWkt(swkt.encode('utf-8'))

    t_srs = osr.SpatialReference()
    t_srs.ImportFromWkt(twkt.encode('utf-8'))
    
    
    xform = osr.CoordinateTransformation(s_srs, t_srs)
    transformation = xform.TransformPoint(x, y, z)
    export = {}
    export["x"] = transformation[0]
    export["y"] = transformation[1]
    export["z"] = transformation[2]
    response['Content-Type'] = "text/json"
    
    if callback != str(0):
      export = str(callback) + "(" + str(export) + ")"
      response['Content-Type'] = "application/javascript"
      
    return export

@route('/<id:re:.+[\d]+.+?>/')
def index(id):
  redirect('/%s' % id)
  
@route('/about')
def index():
  return template('./templates/about')

@route('/css/<filename>')
def server_static(filename):
    return static_file(filename, root='./css/')

@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='/')

if __name__ == "__main__":
  #run(host='0.0.0.0', port=82)
  run(host='0.0.0.0', port=8080, server='gunicorn', workers=4)
  