#!/usr/bin/env python
# encoding: utf-8
"""
"""
INDEX = "../index"
"""
facets_index = {'CRS' :0,
  'CRS-PROJCRS':1,
  'CRS-GEOGCRS':2,
  'CRS-GCENCRS':3,
  'CRS-VERTCRS':4,
  'CRS-ENGCRS':5,
  'CRS-COMPOUNDCRS':6,
  'DATUM':7,
  'DATUM-VERTDAT':8,
  'DATUM-ENGDAT':9,
  'DATUM-GEODDAT':10,
  'ELLIPSOID':11,
  'PRIMEM':12,
  'METHOD':13,
  'CS':14,
  'CS-VERTCS':15,
  'CS-SPHERCS':16,
  'CS-CARTESCS':17,
  'CS-ELLIPCS':18,
  'AXIS':19,
  'AREA':20,
  'UNIT':21,
  'UNIT-ANGUNIT':22,
  'UNIT-SCALEUNIT':23,
  'UNIT-LENUNIT':24
}
"""
facets_list = [
  ['CRS','CRS','Coordinate reference systems',0,'http://'],
  ['CRS-PROJCRS','PROJCRS','&nbsp; &nbsp; Projected',0,'http://'],
  ['CRS-GEOGCRS','GEOGCRS','&nbsp; &nbsp; Geodetic',0,'http://'],
  ['CRS-GCENCRS','GCENCRS','&nbsp; &nbsp; Geocentric',0,'http://'],
  ['CRS-VERTCRS','VERTCRS','&nbsp; &nbsp; Vertical',0,'http://'],
  ['CRS-ENGCRS','ENGCRS','&nbsp; &nbsp; Engineering',0,'http://'],
  ['CRS-COMPOUNDCRS','COMPOUNDCRS','&nbsp; &nbsp; Compound',0,'http://'], 
  ['COORDOP','COORDOP','Operation',0,'http://'],
  ['COORDOP-COPTRANS','COPTRANS','&nbsp; &nbsp; Transformation',0,'http://'],
  ['COORDOP-COPCONOP','COPCONOP','&nbsp; &nbsp; Compound',0,'http://'],
  ['COORDOP-COPCON','COPCON','&nbsp; &nbsp; Conversion',0,'http://'],
  ['DATUM','DATUM','Datum',0,'http://'],
  ['DATUM-VERTDAT','VERTDAT','&nbsp; &nbsp; Vertical',0,'http://'],
  ['DATUM-ENGDAT','ENGDAT','&nbsp; &nbsp; Engineering',0,'http://'],
  ['DATUM-GEODDAT','GEODDAT','&nbsp; &nbsp; Geodetic',0,'http://'],
  ['ELLIPSOID','ELLIPSOID','Ellipsoid',0,'http://'],
  ['PRIMEM','PRIMEM','Prime meridian',0,'http://'],
  ['METHOD','METHOD','Method',0,'http://'],
  ['CS','CS','Coordinate systems',0,'http://'],
  ['CS-VERTCS','VERTCS','&nbsp; &nbsp; Vertical',0,'http://'],
  ['CS-SPHERCS','SPHERCS','&nbsp; &nbsp; Spherical',0,'http://'],
  ['CS-CARTESCS','CARTESCS','&nbsp; &nbsp; Cartesian',0,'http://'],
  ['CS-ELLIPCS','ELLIPCS','&nbsp; &nbsp; Ellipsoidal',0,'http://'],
  ['AXIS','AXIS','Axis',0,'http://'],
  ['AREA','AREA','Area',0,'http://'],
  ['UNIT','UNIT','Units',0,'http://'],
  ['UNIT-ANGUNIT','ANGUNIT','&nbsp; &nbsp; Angle',0,'http://'],
  ['UNIT-SCALEUNIT','SCALEUNIT','&nbsp; &nbsp; Scale',0,'http://'],
  ['UNIT-LENUNIT','LENUNIT','&nbsp; &nbsp; Length',0,'http://'],
]

# Index to the facets_list above - manual update on change!
f_crs_index = 0
f_op_index = 7
f_datum_index = 11
f_cs_index = 18
f_unit_index = 25

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

import itertools

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
    parser = MultifieldParser(["tgrams","code","name","trans","code_trans","kind","area","alt_name","wkt"], ix.schema) #,"wkt"
    query = request.GET.get('q') # p43 - 1.9 The default query language
    pagenum = int(request.GET.get("page",1))
    print pagenum
    kind = getQueryParam(query, 'kind')
    deprecated = getQueryParam(query, 'deprecated')
    
    #print deprecated, 'deprecated', type(deprecated) ,"not deprecated:", not deprecated
    #print kind, 'kind'
    
    statquery = setQueryParam(query, 'deprecated', not deprecated,True)
    #print statquery, 'statquery1'
    
    url_facet_statquery ="/?q=" + urllib2.quote(statquery)
    #print url_facet_statquery
    statquery = setQueryParam(statquery,'kind','*')
    #print statquery, 'statquery2'
    
    

    catquery = setQueryParam(query,'kind','*')
    #print catquery, 'catquery'
    myquery = parser.parse(getVerboseQuery(query))
    mycatquery = parser.parse(getVerboseQuery(catquery))
    mystatquery = parser.parse(getVerboseQuery(statquery))
    #print mystatquery
    #facets = sorting.Facets()
    #facets.add_field("kind",maptype=sorting.Count)#,allow_overlap=False
    #facets.add_field("deprecated",maptype=sorting.Count)#,allow_overlap=False

    start = time.clock()
#####    # first method for all 2.2s
    res_facets = searcher.search(mycatquery , groupedby='kind',scored=False,sortedby=None,maptype=sorting.Count)   # ,limit = 50
    res_facetss = searcher.search(mystatquery , groupedby="deprecated",scored=False,sortedby=None,maptype=sorting.Count)   # ,limit = 50  
    elapsed = (time.clock() - start)
    print elapsed , 'facets'
#### results of documents
    start = time.clock()
    
    
    #results = searcher.search_page(myquery, pagenum, pagelen, terms=True)
    results = searcher.search(myquery, limit = None) #(pagenum*pagelen)
    elapsed = (time.clock() - start)
    print elapsed, "results"

    
    
    groups = res_facets.groups("kind")
    status_groups = res_facetss.groups("deprecated")
    
    pagelen = 10
    maxdoc = pagelen*pagenum
    
    for r in results[(maxdoc-pagelen):maxdoc]: #
      #if r['primary'] == 0 and r['code_trans'] !=0:
      #  link = str(r['code']) + "-" + str(r['code_trans'])
  #  
      #elif r['primary'] == 1 or r['code_trans'] == 0:
      link = str(r['code'])
     
      result.append({'r':r, 'link':link})
    
    num_results = len(results) #results.estimated_length()
 
    pagemax = round((num_results/10.0) + 0.5)

    # TODO REPLACE with verbose
    #statquery = setQueryParam(statquery, ' kind', getQueryParam(query,'kind'),True)  
    #print statquery,'statquery3'      
    
    # set all to zero
    for i in range(0,len(facets_list)):
      facets_list[i][3] = 0
      
    query_kind_index = None
    # update facets counters
    
    for key,value in groups.iteritems():
        
      # standard kinds
      for i in range(0,len(facets_list)):
        if facets_list[i][0] == key:
          facets_list[i][3] = int(value)
          catquery = setQueryParam(catquery, 'kind', facets_list[i][1])
          facets_list[i][4] = "/?q=" + urllib2.quote(catquery)
          # num_results
          if kind == facets_list[i][1]:
            query_kind_index = i

      # sum kinds
      if key.startswith('CRS-'):
        facets_list[f_crs_index][3] += int(value)
        catquery = setQueryParam(catquery, 'kind', facets_list[f_crs_index][1])
        facets_list[f_crs_index][4] = "/?q=" + urllib2.quote(catquery)
        #query_kind_index = f_crs_index
      if key.startswith('DATUM-'):
        facets_list[f_datum_index][3] += int(value)
        catquery = setQueryParam(catquery, 'kind', facets_list[f_datum_index][1])
        facets_list[f_datum_index][4] = "/?q=" + urllib2.quote(catquery)
        #query_kind_index = f_datum_index
        
      if key.startswith('CS-'):
        facets_list[f_cs_index][3] += int(value)
        catquery = setQueryParam(catquery, 'kind', facets_list[f_cs_index][1])
        facets_list[f_cs_index][4] = "/?q=" + urllib2.quote(catquery)
        #query_kind_index = f_cs_index
        
      if key.startswith('UNIT-'):
        facets_list[f_unit_index][3] += int(value)
        catquery = setQueryParam(catquery, 'kind', facets_list[f_unit_index][1])
        facets_list[f_unit_index][4] = "/?q=" + urllib2.quote(catquery)
        #query_kind_index = f_unit_index
      if key.startswith('COORDOP-'):
        facets_list[f_op_index][3] += int(value)
        catquery = setQueryParam(catquery, 'kind', facets_list[f_op_index][1])
        facets_list[f_op_index][4] = "/?q=" + urllib2.quote(catquery)
        
            



      
    # num_results update by kind for all records from facet
    #num_results = 0
    #print query_kind_index
    #try:
    #  num_results = facets_list[query_kind_index][3]
    #except: # unknown kind: in query
    #  pass
    #  print 'neni query_kind_index'
    query = setQueryParam(query,'kind',kind)
    query = setQueryParam(query,'deprecated',deprecated)
    

    
    
  return template('results',result=result,facets_list=facets_list,res_facets=res_facets, groups = groups, num_results=num_results, url_facet_statquery=url_facet_statquery, status_groups=status_groups, query=query, pagenum=int(pagenum),elapsed=elapsed,deprecated=deprecated,kind=kind,pagemax=int(pagemax))



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
    item = None
    trans = []
    num_results = 0
    url_trans = []
    trans_item = []
    wkt = None
    default_trans = ""
    url_method = ""
    url_format = ""
    export = ""
    url_area_trans = ""
    url_area = ""
    g_coords = ""
    center = 0,0
    trans_coords = ""
    """
    start = time.clock()
    parser = QueryParser("code_trans", ix.schema) #,"wkt"
    myquery = parser.parse(code_trans)
    defulttransform = searcher.search(myquery, limit = 1,scored=False,sortedby=None) #(pagenum*pagelen)
    elapsed = (time.clock() - start)
    print elapsed , 'trans'
    print defulttransform
    """
    
    for r in results:
      item = r
      title = item['kind'] + ":" + item['code']
      url_area = area_to_url(item['area'])
      
      
      print r['trans']
      if code_trans == str(0) and r['primary']==1:
        code_trans = r['code_trans']
      
      if code_trans != 0:
        for code_transformation in r['trans']:
          #query = "code:" + str(code_transformation)
          parser = MultifieldParser(["code","kind"], ix.schema)
          query = "code:"+str(code_transformation)
          myquery = parser.parse(query)
          transformation = searcher.search(myquery, limit=None)
          for hit in transformation:
            trans_item.append(hit)
            
            if hit['code'] == int(code_trans):  
              link = ""
            else:
              link = str(r['code']) + u"-" + str(hit['code'])
            
            default = False
            if r['code_trans']== hit['code']: 
              default = True
            print default
            trans.append({
            'link':link,
            'code':hit['code'],
            'deprecated':hit['deprecated'],
            'area_trans':hit['area'],
            'accuracy':hit['accuracy'],
            'code_trans':hit['code'],
            'trans_remarks':hit['remarks'],
            'default':default})
                
      default_trans = ''
      for i in range(0,len(trans_item)):
        if str(code_trans) == str(trans_item[i]['code']):
          print 'yes'
          default_trans = trans_item[i] #information about 
      if trans_item:
        url_format = "/"+str(item['code'])+"-"+str(default_trans['code'])
      
        values = default_trans['wkt']
        num =[]
        w = re.findall(r'(-?\d+\.?\d*)',values)
      
        for n in w:
          num.append(float(n))
        values = tuple(num)     

        if int(r['code_trans']) != int(default_trans['code']):
          if (values != (0,0,0,0,0,0,0) and type(values) == tuple):
            ref = osr.SpatialReference()
            ref.ImportFromEPSG(int(r['code']))
            ref.SetTOWGS84(*values) 
            wkt = ref.ExportToWkt().decode('utf-8')
        else: 
          wkt = r['wkt']
      else:
        center = ((item['bbox'][0] - item['bbox'][2])/2.0)+item['bbox'][2],((item['bbox'][3] - item['bbox'][1])/2.0)+item['bbox'][1]
        g_coords = str(item['bbox'][2]) + "," + str(item['bbox'][1]) + "|" + str(item['bbox'][0]) + "," + str(item['bbox'][1]) + "|" + str(item['bbox'][0]) + "," + str(item['bbox'][3]) + "|" + str(item['bbox'][2]) + "," + str(item['bbox'][3]) + "|" + str(item['bbox'][2]) + "," + str(item['bbox'][1])
        
    if wkt:    
      url_method ="/?q=" + urllib.quote_plus((default_trans['method']+ ' kind:METHOD').encode('utf-8'))
      center = 0,0
      g_coords = ""
      if default_trans['bbox']:
          #(51.05, 12.09, 47.74, 22.56)
        center = ((default_trans['bbox'][0] - default_trans['bbox'][2])/2.0)+default_trans['bbox'][2],((default_trans['bbox'][3] - default_trans['bbox'][1])/2.0)+default_trans['bbox'][1]
        g_coords = str(default_trans['bbox'][2]) + "," + str(default_trans['bbox'][1]) + "|" + str(default_trans['bbox'][0]) + "," + str(default_trans['bbox'][1]) + "|" + str(default_trans['bbox'][0]) + "," + str(default_trans['bbox'][3]) + "|" + str(default_trans['bbox'][2]) + "," + str(default_trans['bbox'][3]) + "|" + str(default_trans['bbox'][2]) + "," + str(default_trans['bbox'][1])

      url_area_trans = area_to_url(default_trans['area'])
    
      trans_coords = "" 
      if wkt != None:
        ref = osr.SpatialReference()
        #ref.ImportFromEPSG(5513)
        ref.ImportFromWkt(wkt.encode('utf-8'))
        #ref.ImportFromEPSG(5514)
        #ref.SetAuthority("PROJCS","EPSG","5514")
        #ref.SetFromUserInput(item['wkt'].encode('utf-8'))
      
        wgs = osr.SpatialReference()
        wgs.ImportFromEPSG(4326)
        xform = osr.CoordinateTransformation(wgs,ref)
      
      
        #print center[0], type(center[0]), center[1], type(center[1])
        try:
          trans_coords = xform.TransformPoint(center[0], center[1])
        except:
          trans_coords = "" 
        
        export = highlight(ref.ExportToPrettyWkt(), WKTLexer(), HtmlFormatter(cssclass='syntax',nobackground=True))
       
  return template('detailed', item=item, trans=trans,default_trans=default_trans, num_results=num_results, url_method=url_method, title=title, url_format=url_format, export=export, url_area_trans=url_area_trans, url_area=url_area, center=center, g_coords=g_coords, trans_coords=trans_coords,wkt=wkt )  


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
  from osgeo import gdal, osr, ogr
  ref = osr.SpatialReference()
  with ix.searcher(closereader=False) as searcher:
    parser = QueryParser("code", ix.schema)

    code, code_trans = (id+'-0').split('-')[:2]
    
    code_query = parser.parse(code)
    code_result = searcher.search(code_query, sortedby=False,scored=False)
    
    trans_query = parser.parse(code_trans)
    trans_result = searcher.search(trans_query,sortedby=False,scored=False)
    for t in trans_result:
      values = t['wkt']
      tcode = t['code']
    for r in code_result:
      code_trans = r['code_trans']
      rwkt = r['wkt']
      rcode = r['code']

    w = re.findall(r'(-?\d+\.?\d*)',values)
    num =[]
    for n in w:
      num.append(float(n))
    values = tuple(num)

    if int(code_trans) != int(tcode):
      if (values != (0,0,0,0,0,0,0) and type(values) == tuple):
        ref.ImportFromEPSG(int(rcode))
        ref.SetTOWGS84(*values) 
        wkt = ref.ExportToWkt().decode('utf-8')
    else: 
      wkt = rwkt
  
    
    
    
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
      return template('export', export = export, code=rcode)
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
      export = "wkt = '''%s'''\nm = mapObj('')\nm.setWKTProjection(wkt)\nlyr = layerObj(m)\nlyr.setWKTProjection(mswkt)" % (mswkt) #from mapscript import mapObj,layerObj\n
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
    parser = QueryParser("code", ix.schema)

    code, code_trans = (id+'-0').split('-')[:2]

    type = "EPSG"

    code_query = parser.parse(code)
    code_result = searcher.search(code_query, sortedby=False,scored=False)
    #print code_result[0]
    trans_query = parser.parse(code_trans)
    trans_result = searcher.search(trans_query,sortedby=False,scored=False)
    
    for t in trans_result:
      #print t
      values = t['wkt']
      tcode = t['code']

    for r in code_result:
      code_trans = r['code_trans']
      rwkt = r['wkt']
      rcode = r['code']
      rname = r['name']

    w = re.findall(r'(-?\d+\.?\d*)',values)
    num =[]
    for n in w:
      num.append(float(n))
    values = tuple(num)     

    if int(code_trans) != int(tcode):
      if (values != (0,0,0,0,0,0,0) and type(values) == tuple):
        ref = osr.SpatialReference()
        ref.ImportFromEPSG(int(rcode))
        ref.SetTOWGS84(*values) 
        wkt = ref.ExportToWkt().decode('utf-8')
    else: 
      wkt = rwkt
      
      
    trans_wgs = "" 
    trans_other = ""
    
    from osgeo import gdal, osr, ogr
    
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
      
  
  return template ('coordinates', trans_wgs=trans_wgs, trans_other=trans_other, result=code_result[0],coord_lat=coord_lat,coord_lon=coord_lon,coord_lat_other=coord_lat_other,coord_lon_other=coord_lon_other)

if __name__ == "__main__":
  #run(host='0.0.0.0', port=82)
  run(host='0.0.0.0', port=8080, server='gunicorn', workers=4)
  