#!/usr/bin/env python
# -*- coding: utf-8 -*-
DATABASE = ('dbname=epsg82 user=tompohys host=localhost')
INDEX = "index"

import os,sys
import psycopg2
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.query import *
from whoosh.qparser import QueryParser
from osgeo import gdal, osr, ogr
from pprint import pprint

###############################################################################
print "INICIALIZING"
###############################################################################
print " - DATABASE"
con = psycopg2.connect(DATABASE)
if not con:
  print "Connection to Postgres FAILED"
  sys.exit(1)
con.set_client_encoding('utf-8')
cur = con.cursor()


print " - WHOOSH!"

class EPSGSchema(SchemaClass):
  
  code = TEXT(stored = True, sortable=True, field_boost=5.0) # "EPSG:4326" #coord_ref_sys_code
  name = TEXT(stored = True, sortable=True, spelling=True, field_boost=2.0) # Name "WGS 84" #coord_ref_sys_name
  type = ID(stored = True) # "ProjectedCRS" | "GeodeticCRS" #coord_ref_sys_kind
  area = TEXT(stored = True, sortable=True, spelling=True) #epsg_area/area_of_use
  status = BOOLEAN(stored = True) # "1 = Valid", "0 - Invalid"
  popularity = NUMERIC(stored = True) # number [0..1] - our featured = 1

  # Description of used transformation - "", "Czech republic (accuracy 1 meter)"
  trans = TEXT(stored = True, sortable=True, spelling=True, field_boost=1.5) # area of used towgs transformation + (accuracy) else ""

  # Specific fields for all coordinate systems
  wkt = TEXT
  bbox = NUMERIC # [area_north_bound_lat,area_west_bound_lon,area_south_bound_lat,area_east_bound_lon]

  scope = STORED # crs_scope
  remarks = STORED # remarks
  information_source = STORED # information_source
  revision_date = STORED # revision_date

  # Advanced with additional types such as "Elipsoid" | "Area" | ...
  #datum = ID(stored = True) # epsg code for stored CRS
  #towgs = ID(stored = True) # epsg code for transformation used in wkt or empty
  #geogcs = ID(stored = True) # 
  #ellipsoid = ID(stored = True) #
  
  # Specific for projected coordinate systems
  #projection = ID(stored = True)

#if not os.path.exists(INDEX):
#    os.mkdir(INDEX)

#ix = create_in(INDEX, EPSGSchema)

print " - SELECT ALL EPSG"
cur.execute('SELECT coord_ref_sys_code, coord_ref_sys_name,crs_scope, remarks, information_source, revision_date,area_of_use_code,coord_ref_sys_kind,show_crs,source_geogcrs_code  FROM epsg_Coordinatereferencesystem WHERE coord_ref_sys_code > 5500 and coord_ref_sys_code < 6000')

for code, name, scope, remarks, information_source, revision_date, area_code, coord_ref_sys_kind, show_crs, source_geogcrs_code in cur.fetchall():
  
  ref = osr.SpatialReference()
  try:
    name = name.encode('LATIN1').decode('utf-8')
  except:
    print "NOT POSIBLE TO DECODE:", code, name
    continue

  ref.ImportFromEPSG(int(code))
  code = str(code).decode('utf-8')
  text = ref.ExportToWkt().decode('utf-8')
  type = coord_ref_sys_kind
  
  status = int(show_crs)
  
  # get boundingbox and area of use
  cur.execute('SELECT area_of_use, area_north_bound_lat, area_west_bound_lon, area_south_bound_lat, area_east_bound_lon FROM epsg_area WHERE area_code = %s;', (area_code,))
  area_of_use = cur.fetchall()

  for area, area_north_bound_lat, area_west_bound_lon, area_south_bound_lat, area_east_bound_lon in area_of_use:
    
    bbox = area_north_bound_lat,area_west_bound_lon,area_south_bound_lat,area_east_bound_lon
  
  trans = u"None"

  doc = {
    'code': code,
    'name': name,
    'area': area,
    'wkt': text,
    'bbox': bbox,
    'scope': scope,
    'remarks': remarks,
    'information_source': information_source,
    'revision_date': revision_date,
    'status': status,
    'trans' : trans,
    'type': type
  }
  
# transofrmation to wgs84
  cur.execute('SELECT coord_op_code, coord_op_accuracy,area_of_use FROM epsg_coordoperation LEFT JOIN epsg_area ON area_of_use_code = area_code  WHERE source_crs_code = %s and target_crs_code = 4326',(source_geogcrs_code,))
  towgs84 = cur.fetchall()

  if len(towgs84) != 1:
     with ix.writer() as writer:
       writer.add_document(**doc)
       
  for op_code, op_accuracy, area in towgs84:
    if op_accuracy == None:
      trans = area + u" "+ u"(unknown accuracy)"
    else:
      trans = area + u" " + str(op_accuracy) + u"m accuracy"      
    
    code_op = str(code).decode('utf-8') + u"-" + str(op_code).decode('utf-8')
    text_op = text + "TOWGS(asdfghjkliuytrew)"

    doc['trans'] = trans
    if len(towgs84) != 1:
      doc['code'] = code_op
      doc['wkt'] = text_op
  
    with ix.writer() as writer:
      writer.add_document(**doc)   