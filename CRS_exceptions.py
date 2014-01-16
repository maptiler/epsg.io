#!/usr/bin/env python
# -*- coding: utf-8 -*-
CRS_EXCEPTATIONS = 'CRS_exceptions.csv'
INDEX = 'index'

import sys
import whoosh.index
import whoosh.qparser
import whoosh.fields
import csv

###############################################################################
print "INICIALIZING"
###############################################################################
crs_ex_line = {}
try:
  with open(CRS_EXCEPTATIONS) as crs_ex:
    text = csv.reader(crs_ex, delimiter = ',')
    # skip the header
    next(text, None)    
    for row in text:
      crs_ex_line[row[0]] = row
    #print crs_ex_line['4326'][2]
    #print crs_ex_line
except:
  print "!!! FAILED: NO CRS_EXCEPTATIONS !!!"
  sys.exit(1)

try:
  ix = whoosh.index.open_dir(INDEX)
except:
  print "!!! FAILED: Connection to Index !!!"
  sys.exit(1)    

###############################################################################
print "UPDATING INDEX"
###############################################################################
for item in crs_ex_line:
  alt_code = crs_ex_line[item][3].split(",")
  doc = {}
  # alt_code = []
  # try:
  #   alt_code.append(str(crs_ex_line[item][3]))
  # except:
  #   if crs_ex_line[item][3] != '':
  #     alt_code = [str(x) for x in crs_ex_line[item][3].split(",")]
  # #if alt_code == []:
  # #  alt_code = None
  with ix.searcher() as searcher:
    parser = whoosh.qparser.QueryParser("code", ix.schema)

    code_query = parser.parse(str(item) + " kind:CRS")
    code_result = searcher.search(code_query)
    if not code_result:
      deprecated = 0
      if "deprecated" in crs_ex_line[item][2]:
        deprecated = 1
      
      doc = {
      'code':item.decode('utf-8'),
      'code_id':item.decode('utf-8'),
      'name': crs_ex_line[item][2].decode('utf-8'),
      'alt_title': u"",
      'alt_description' : crs_ex_line[item][4].decode('utf-8'),
      'alt_code' : alt_code,
      'code_trans' : 0,
      'area_trans' : u"",
      'accuracy' : u"",
      'kind': u"CRS",
      'area': u"",
      'deprecated': deprecated,
      'trans' : 0,
      'primary' : 0,
      'wkt': u"",
      'tgrams': crs_ex_line[item][2].decode('utf-8'),
      'description': u"",
      
      'alt_name' : u"",
      'trans_alt_name' : u"",
      'trans_remarks': u"",
      'bbox': u"",
      'scope': u"",
      'remarks': u"",
      'information_source': u"",
      'revision_date': u"",
      'datum_code' : u"",
      'source_geogcrs': u"",
      'children_code' : u"",
      'data_source' : u"",
      'uom_code' : u"",
      'uom' : u"",
      'target_uom': u"",
      'prime_meridian' : u"",
      'greenwich_longitude' : u"",
      'concatop' : u"",
      'method' : u"",
      'files' : u"",
      'reverse' : u"",
      'orientation' : u"",
      'abbreviation' : u"",
      'order' : u"",
      'area_code' : u"",
      'area_trans_code': u""

      }
      with ix.writer() as writer:
        writer.add_document(**doc)
      
    elif code_result:  
      for result in code_result:
        if 'alt_title' in result:
          if str(result['name']) != str(result['alt_title']) and str(result['name']) != str(crs_ex_line[item][2].decode('utf-8')):
            alt_title = crs_ex_line[item][2].decode('utf-8')
            
          else:
            alt_title = u""
          
        area_trans_code = u""    
        if 'area_trans_code' in result:
          area_trans_code = result['area_trans_code']
        
        doc = {
          'code': result['code'],
          'code_id':result['code_id'],
          'code_trans' : result['code_trans'],
          'name': result['name'],
          'alt_title': alt_title ,
          'alt_name' : result['alt_name'],
          'kind': result['kind'],
          'area': result['area'],
          'deprecated': result['deprecated'],
          'trans' : result['trans'],
          'trans_alt_name' : result['trans_alt_name'],
          'trans_remarks': result['trans_remarks'],
          'area_trans' : result['area_trans'],
          'accuracy' : result['accuracy'],
          'wkt': result['wkt'],
          'bbox': result['bbox'],
          'scope': result['scope'],
          'remarks': result['remarks'],
          'information_source': result['information_source'],
          'revision_date': result['revision_date'],
          'datum_code' : result['datum_code'],
          'source_geogcrs': result['source_geogcrs'],
          'children_code' : result['children_code'],
          'data_source' : result['data_source'],
          'uom_code' : result['uom_code'],
          'uom' : result['uom'],
          'target_uom': result['target_uom'],
          'prime_meridian' : result['prime_meridian'],
          'greenwich_longitude' : result['greenwich_longitude'],
          'concatop' : result['concatop'],
          'method' : result['method'],
          'files' : result['files'],
          'reverse' : result['reverse'],
          'orientation' : result['orientation'],
          'abbreviation' : result['abbreviation'],
          'order' : result['order'],
          'description':result['description'],
          'primary' : result['primary'],
          'tgrams':result['name']+" "+result['area'],
          'code_id':item.decode('utf-8'),
          'alt_description' : crs_ex_line[item][4].decode('utf-8'),
          'alt_code' : alt_code,
          'area_code' : result['area_code'],
          'area_trans_code' : area_trans_code
        }  
        with ix.writer() as writer:
          writer.update_document(**doc)




###############################################################################
print "FINISH"
###############################################################################