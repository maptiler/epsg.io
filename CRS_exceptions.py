#!/usr/bin/python3 
# -*- coding: utf-8 -*-
CRS_EXCEPTATIONS = 'CRS_exceptions.csv'
INDEX = 'index'

import sys
import whoosh.index
import whoosh.qparser
import whoosh.fields
import csv
import os.path
import time
import json

exceptations_mod_time=time.gmtime(os.path.getmtime(CRS_EXCEPTATIONS))
# exceptations_create_time=time.gmtime(os.path.getctime(CRS_EXCEPTATIONS))
index_mod_time=time.gmtime(os.path.getmtime(INDEX))
index_create_time=time.gmtime(os.path.getctime(INDEX))

# print "create CRS_ex: %s" % exceptations_create_time
# print "create index: %s" % index_create_time
# print
# print "last modified CRS_ex: %s" % exceptations_mod_time
# print "last modified index: %s" % index_mod_time
do_it = True
if exceptations_mod_time>=index_mod_time or index_mod_time!=index_create_time: # index is OLDER then exceptations
  do_it = True
  

if do_it == True:
  
  ###############################################################################
  print("INITIALIZING")
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
    print("!!! FAILED: NO CRS_EXCEPTATIONS !!!")
    sys.exit(1)

  try:
    ix = whoosh.index.open_dir(INDEX)
  except Exception as e:
    print("!!! FAILED: Connection to Index !!!")
    print(e)
    sys.exit(1)    

  ###############################################################################
  print("UPDATING INDEX")
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


    if(alt_code == ['']):
        alt_code = None

    with ix.searcher() as searcher:
      parser = whoosh.qparser.QueryParser("code", ix.schema)

      code_query = parser.parse(str(item) + " kind:CRS")
      code_result = searcher.search(code_query)
      if not code_result:
        deprecated = 0
        if "deprecated" in crs_ex_line[item][2]:
          deprecated = 1
      
        doc = {
        'code':item,
        'code_id':item,
        'name': crs_ex_line[item][2],
        'alt_title': "",
        'alt_description' : crs_ex_line[item][4],
        'alt_code' : alt_code,
        'code_trans' : 0,
        'area_trans' : "",
        'accuracy' : "",
        'kind': "CRS",
        'area': "",
        'deprecated': deprecated,
        'trans' : [],
        'primary' : 0,
        'description': "",
      
        'alt_name' : "",
        'trans_alt_name' : "",
        'trans_remarks': "",
        'bbox': "",
        'scope': "",
        'remarks': "",
        'information_source': "",
        'revision_date': "",
        'datum' : "",
        'geogcrs': "",
        #'children_code' : u"",
        'data_source' : "",
        'uom_code' : "",
        'uom' : "",
        'target_uom': "",
        'primem' : "",
        'greenwich_longitude' : "",
        'concatop' : "",
        'method' : "",
        'files' : "",
        'reverse' : "",
        'orientation' : "",
        'abbreviation' : "",
        'order' : "",
        'area_code' : None,
        'area_trans_code': None,
        'ellipsoid' : "",

        'cs': "",
        }
        with ix.writer() as writer:
          writer.add_document(**doc)
      
      elif code_result:  
        alt_title = ""
        for result in code_result:
          if 'alt_title' in result:
            if str(result['name']) != str(result['alt_title']) and str(result['name']) != str(crs_ex_line[item][2]):
              alt_title = crs_ex_line[item][2]
            
            else:
              alt_title = ""
          
          area_trans_code = None  
          if 'area_trans_code' in result:
            area_trans_code = result['area_trans_code']
        
          boost = 0
          if result['kind'] == "CRS-PROJCRS":
            boost = 0.2
          if result['kind'] == "CRS-GEOGCRS" or result['kind'] == "CRS-GEOG3DCRS":
            boost = 0.05
          # boost by code from csv file
          importance = 0
          try:
            importance = crs_ex_line[item][1]
            if importance == "":
              importance = 0
          except:
            pass
          
          score = float((1 + boost) * (1 + float(importance)*4))
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
            'bbox': result['bbox'],
            'scope': result['scope'],
            'remarks': result['remarks'],
            'information_source': result['information_source'],
            'revision_date': result['revision_date'],
            'datum' : result['datum'],
            'geogcrs': result['geogcrs'],
            #'children_code' : result['children_code'],
            'data_source' : result['data_source'],
            'uom_code' : result['uom_code'],
            'uom' : result['uom'],
            'target_uom': result['target_uom'],
            'primem' : result['primem'],
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
            'code_id':item,
            'alt_description' : crs_ex_line[item][4],
            'alt_code' : alt_code,
            'area_code' : result['area_code'] if 'area_code' in result else None,
            'area_trans_code' : area_trans_code,
            'ellipsoid' : result['ellipsoid'],
            'cs': result['cs'],
            '_boost': score
          }  
          with ix.writer() as writer:

            try:
              writer.update_document(**doc)
            except Exception as e:
              print(e)
              print(json.dumps(doc))
              exit()




###############################################################################
  print("FINISH")
###############################################################################

else:
###############################################################################
  print("NOT NECESSARY TO UPDATE DATABASE!")
###############################################################################
