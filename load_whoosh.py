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
  
  code = NUMERIC(stored = True, sortable=True, field_boost=5.0,decimal_places=0) # "EPSG:4326" #coord_ref_sys_code
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
cur.execute('SELECT coord_ref_sys_code, coord_ref_sys_name,crs_scope, remarks, information_source, revision_date,area_of_use_code,coord_ref_sys_kind,show_crs  FROM epsg_Coordinatereferencesystem;')

for code, name, crs_scope, remarks, information_source, revision_date, area_of_use_code,coord_ref_sys_kind,show_crs in cur.fetchall():
  
  ref = osr.SpatialReference()
  try:
    name = name.encode('LATIN1').decode('utf-8')
  except:
    print "NOT POSIBLE TO DECODE:", code, name
    continue

  ref.ImportFromEPSG(int(code))
  
  text = ref.ExportToWkt().decode('utf-8')
  words = text.split()
  print text
  #pprint (words)
  scope = crs_scope
  remarks = remarks
  information_source = information_source
  revision_date = revision_date
  area=area_of_use_code
  type = coord_ref_sys_kind
  
  if show_crs == 1:
    status = u'Valid'
  else:
    status = u'Invalid'

  # get boundingbox and area of use
  cur.execute('SELECT area_of_use,area_north_bound_lat,area_west_bound_lon,area_south_bound_lat,area_east_bound_lon FROM epsg_area WHERE area_code = %s;', (area,))
  area_of_use = cur.fetchall()

  for area_of_use, area_north_bound_lat, area_west_bound_lon, area_south_bound_lat, area_east_bound_lon in area_of_use:
    area = area_of_use
    bbox = area_north_bound_lat,area_west_bound_lon,area_south_bound_lat,area_east_bound_lon
  
  

  cur.execute('SELECT coord_op_code, coord_op_name, area_of_use_code, coord_op_accuracy FROM epsg_coordoperation WHERE source_crs_code = %s and target_crs_code = 4326',(code,))
  towgs84 = cur.fetchall()
  if len(towgs84) == 1:
    #print "Just one transformation"
    for op_code, op_name, op_area, op_accuracy in towgs84:
      cur.execute('SELECT area_code, area_of_use FROM epsg_area WHERE area_code = %s', (op_area,))
      area_of_use = cur.fetchall()      
      for a_code, area in area_of_use:
        if op_accuracy == None:
          trans = area + u" (unknown accuracy)"
          print trans
        else:
          trans = area + u" " + str(op_accuracy) + u"m accuracy"
  # 0 or more transformation to wgs
  else:
    trans = None
"""
  with ix.writer() as writer:
    
    writer.add_document(code = code,
                        name = name,
                        area = area,
                        wkt = text,
                        bbox = bbox,
                        scope = scope,
                        remarks = remarks,
                        information_source = information_source,
                        revision_date = revision_date,
                        trans = trans,
                        status = status,
                        type = type)
"""