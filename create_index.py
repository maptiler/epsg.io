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
from whoosh import fields, columns
from whoosh.analysis import StemmingAnalyzer

kind_list = {
  'vertical' : "CRS-VERTCRS",
  'geocentric' : "CRS-GCENCRS",
  'engineering' : "CRS-ENGCRS",
  'geographic 3D' : "CRS-GEOG3DCRS",
  'geographic 2D' : "CRS-GEOGCRS",
  'compound' : "CRS-COMPOUNDCRS",
  'projected' : "CRS-PROJCRS",
  'transformation':  "COORDOP-COPTRANS",
  'concatenated operation' : "COORDOP-COPCONOP",
  'conversion' : "COORDOP-COPCON",            
  'UNIT-angle' : "UNIT-ANGUNIT",
  'UNIT-scale' : "UNIT-SCALEUNIT",
  'UNIT-length' : "UNIT-LENUNIT",
  'DATUM-vertical' : "DATUM-VERTDAT",
  'DATUM-engineering' : "DATUM-ENGDAT",
  'DATUM-geodetic' : "DATUM-GEODDAT",
  'ELLIPSOID' : "ELLIPSOID",
  'PRIMEM' : "PRIMEM",
  'METHOD' : "METHOD",
  'CS' : "CS",
  'CS-vertical' : "CS-VERTCS",
  'CS-spherical' : "CS-SPHERCS",
	'CS-Cartesian' : "CS-CARTESCS",
	'CS-ellipsoidal':"CS-ELLIPCS",
  'AXIS' : "AXIS",
  'AREA' : "AREA"
}
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
  code_trans = NUMERIC(stored = True, sortable = True) #, field_boost = 5.0
  name = TEXT(stored = True, sortable=True, spelling=True, field_boost=3.0, analyzer=StemmingAnalyzer()) # Name "WGS 84" #coord_ref_sys_name
  alt_name = TEXT (stored = True)
  kind = TEXT(stored = True, sortable=True) # "ProjectedCRS" | "GeodeticCRS" #coord_ref_sys_kind
  area = TEXT(stored = True, sortable=True, spelling=True) #epsg_area/area_of_use
  area_trans = TEXT(stored = True, sortable=True, spelling=True)
  deprecated = BOOLEAN(stored = True) # "1 = Valid", "0 - Invalid"
  popularity = STORED  # number [0..1] - our featured = 1

  # Description of used transformation - "", "Czech republic (accuracy 1 meter)"
  trans = NUMERIC(stored = True) # area of used towgs transformation + (accuracy) else ""
  trans_alt_name = TEXT(stored = True)
  trans_remarks = STORED
  accuracy = STORED
  
  # Specific fields for all coordinate systems
  wkt = TEXT(stored = True)
  bbox = STORED # [area_north_bound_lat,area_west_bound_lon,area_south_bound_lat,area_east_bound_lon]

  scope = STORED # crs_scope
  remarks = STORED # remarks
  information_source = STORED # information_source
  revision_date = STORED # revision_date

  # Advanced with additional types such as "Elipsoid" | "Area" | ...
  datum_code = NUMERIC(stored=True) 
  source_geogcrs = STORED
  target_crs = STORED
  children_code = STORED
  data_source = STORED
  uom = STORED
  target_uom = STORED
  prime_meridian = STORED
  greenwich_longitude = NUMERIC(stored=True)
  concatop = STORED
  method = STORED
  files = STORED
  reverse = STORED
  orientation = STORED
  abbreviation = STORED
  order = STORED
  description = STORED
  primary = STORED
  uom_code = STORED
  
  tgrams = NGRAM(minsize=2, maxsize=4, stored=False)
  #datum_name = TEXT(stored = True, sortable=True, spelling=True, field_boost=3.0, analyzer=stem_ana)
  #datum_deprecated = BOOLEAN(stored = True)
  #towgs = ID(stored = True) # epsg code for transformation used in wkt or empty
  #geogcs = ID(stored = True) # 
  #ellipsoid_code = NUMERIC(stored = True, field_boost=5.0) 
  #ellipsoid_name = TEXT(stored = True, sortable=True, spelling=True, field_boost=3.0 ,analyzer=stem_ana)
  #ellipsoid_deprecated = BOOLEAN(stored = True)
  
  # Specific for projected coordinate systems
  #projection = ID(stored = True)

# MAKE DIRECTORY AND CREATE INDEX
if not os.path.exists(INDEX):
    os.mkdir(INDEX)

ix = create_in(INDEX, EPSGSchema)

###############################################################################
print " - SELECT EPSG FROM COORDINATE REFERENCE SYSTEM AND TRANSFORMATION"
###############################################################################

cur.execute('SELECT coord_ref_sys_code, coord_ref_sys_name,crs_scope, remarks, information_source, revision_date, datum_code, area_of_use_code,coord_ref_sys_kind,deprecated,source_geogcrs_code,data_source,coord_sys_code  FROM epsg_coordinatereferencesystem') #  WHERE coord_ref_sys_code > 5513 and coord_ref_sys_code < 5600 or coord_ref_sys_code = 4156  #WHERE coord_ref_sys_code > 5513 and coord_ref_sys_code < 5600'
for code, name, scope, remarks, information_source, revision_date,datum_code, area_code, coord_ref_sys_kind, deprecated, source_geogcrs_code,data_source,coord_sys_code in cur.fetchall():
  if source_geogcrs_code == None:
    source_geogcrs_code = code
  try:
    name = name.encode('LATIN1').decode('utf-8')
  except:
    print "NOT POSIBLE TO DECODE:", code, name
    continue
  
  #Load WKT from GDAL
  ref = osr.SpatialReference()
  ref.ImportFromEPSG(int(code))  
  text = ref.ExportToWkt().decode('utf-8')
  
  # Get boundingbox and area of use
  cur.execute('SELECT area_of_use, area_north_bound_lat, area_west_bound_lon, area_south_bound_lat, area_east_bound_lon FROM epsg_area WHERE area_code = %s;', (area_code,))
  area_of_use = cur.fetchall()
  for area, area_north_bound_lat, area_west_bound_lon, area_south_bound_lat, area_east_bound_lon in area_of_use:
    bbox = area_north_bound_lat,area_west_bound_lon,area_south_bound_lat,area_east_bound_lon

  alt_name = u""
  # Get alias of name
  cur.execute('SELECT alias, object_code FROM epsg_alias WHERE object_table_name = %s and object_code = %s', ("epsg_coordinatereferencesystem", code,))
  for alt_name, object_code in cur.fetchall():
    pass
  
  # Get Datum code from source geogcs
  cur.execute('SELECT source_geogcrs_code, datum_code FROM epsg_coordinatereferencesystem WHERE coord_ref_sys_code = %s', (source_geogcrs_code,))
  for source_geogcrs, datum_code in cur.fetchall():
    pass
    
  popularity = 1.0
  deprecated = int(deprecated)
  code = str(code).decode('utf-8')
  
  if kind_list.has_key(coord_ref_sys_kind):
    kind = kind_list[coord_ref_sys_kind].decode('utf-8')
  doc = {
    'code': code,
    'code_trans' : 0,
    'name': name,
    'alt_name' : alt_name,
    'kind': kind,
    'area': area,
    'deprecated': deprecated,
    'popularity': popularity,
    'trans' : u"",
    'trans_alt_name' : u"",
    'trans_remarks': u"",
    'area_trans' : u"",
    'accuracy' : u"",
    'wkt': text,
    'bbox': bbox,
    'scope': scope,
    'remarks': remarks,
    'information_source': information_source,
    'revision_date': revision_date,
    'datum_code' : datum_code,
    'source_geogcrs': source_geogcrs_code,
    'children_code' : coord_sys_code,
    'data_source' : data_source,
    'uom_code' : 0,
    'uom' : u"",
    'target_uom': u"",
    'prime_meridian' : 0,
    'greenwich_longitude' : 0,
    'concatop' : u"",
    'method' : u"",
    'files' : u"",
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description':u"",
    'primary' : 0,
    'tgrams':name.lower()+" "+area.lower()
    }  

# transofrmation to wgs84
  cur.execute('SELECT epsg_coordoperation.coord_op_code, epsg_coordoperation.coord_op_accuracy, epsg_coordoperation.coord_op_type, epsg_coordoperation.deprecated, epsg_coordoperation.coord_op_scope, epsg_coordoperation.remarks, epsg_coordoperation.information_source, epsg_coordoperation.revision_date, epsg_coordoperation.uom_code_source_coord_diff,epsg_coordoperation.coord_op_method_code, epsg_area.area_of_use, epsg_area.area_north_bound_lat, epsg_area.area_west_bound_lon, epsg_area.area_south_bound_lat, epsg_area.area_east_bound_lon FROM epsg_coordoperation LEFT JOIN epsg_area ON area_of_use_code = area_code  WHERE source_crs_code = %s and target_crs_code = 4326',(source_geogcrs_code,))
  towgs84 = cur.fetchall()  
  op_code_original = 0
  op_code_trans = {}
  towgs84_original = ref.GetTOWGS84()
  transformations = []
  if len(towgs84) != 0:
    for op_code, op_accuracy,coord_op_type, opdeprecated, coord_op_scope, remarks, information_source, revision_date,uom_code, coord_op_method_code, area, area_north_bound_lat, area_west_bound_lon, area_south_bound_lat, area_east_bound_lon in towgs84:
      cur.execute('SELECT parameter_value, param_value_file_ref FROM epsg_coordoperationparamvalue WHERE coord_op_code = %s', (op_code, ))
      values = cur.fetchall()
      if len(values) == 7:
        v = tuple( map(lambda x: float(x[0]), values) ) # tuple of 7 floats
      elif len(values) == 3:
        v = tuple( map(lambda x: float(x[0]), values) + [0.0]*4 ) # tuple of 3+4 floats
      elif len(values) == 1 and values[0][1] != '': 
        v = values[0][1] # nadgrid file
      else:
        v=0
      
      if op_accuracy == None or op_accuracy == 0.0:
        op_accuracy = u'unknown'
        popularity_acc = -1
      else:
        popularity_acc = 1
        
      op_code_trans[op_code] = v
      if towgs84_original == v:
        op_code_original = op_code
        doc['area_trans'] = area
        doc['accuracy'] = op_accuracy
        doc['wkt'] = text
        doc['primary'] = 1
        doc['code_trans'] = op_code
        doc['popularity'] = 5 + popularity_acc
      
      transformations.append(op_code)
    
    if op_code == op_code_original:    
      doc['trans'] = transformations
      with ix.writer() as writer:
        writer.add_document(**doc)
    else:
      # CRS has transformation to wgs84, but any transformation is not default 
      doc['trans'] = transformations
      doc['primary'] = 0
      doc['popularity'] = 2 
      with ix.writer() as writer:
        writer.add_document(**doc)
  else:
    #print code, "without transformation"
    doc['popularity'] = 1
    with ix.writer() as writer:
      writer.add_document(**doc)

###############################################################################
print " - SELECT EPSG FROM OPERATIONS"
###############################################################################
cur.execute('SELECT epsg_coordoperation.coord_op_code,epsg_coordoperation.coord_op_name,epsg_coordoperation.coord_op_accuracy, epsg_coordoperation.coord_op_type,epsg_coordoperation.source_crs_code,epsg_coordoperation.target_crs_code, epsg_coordoperation.deprecated, epsg_coordoperation.coord_op_scope, epsg_coordoperation.remarks, epsg_coordoperation.information_source, epsg_coordoperation.revision_date, epsg_coordoperation.uom_code_source_coord_diff,epsg_coordoperation.coord_op_method_code, epsg_area.area_of_use, epsg_area.area_north_bound_lat, epsg_area.area_west_bound_lon, epsg_area.area_south_bound_lat, epsg_area.area_east_bound_lon FROM epsg_coordoperation LEFT JOIN epsg_area ON area_of_use_code = area_code ')
for op_code,op_name, op_accuracy, coord_op_type, source_crs, target_crs, deprecated, scope, remarks, information_source, revision_date, uom_code, method, area, area_north_bound_lat, area_west_bound_lon, area_south_bound_lat, area_east_bound_lon in cur.fetchall():
  op_code = str(op_code).decode('utf-8')
  
  kind = kind_list[coord_op_type].decode('utf-8')
  bbox = area_north_bound_lat,area_west_bound_lon,area_south_bound_lat,area_east_bound_lon
  
  if op_accuracy == None or op_accuracy == 0.0:
    op_accuracy = u'unknown'  
      
  uom_name = u""
  uom_code = 0
  cur.execute('SELECT unit_of_meas_name, uom_code FROM epsg_unitofmeasure WHERE uom_code = %s ', (uom_code, ))
  for uom_name, uom_code in cur.fetchall():
    pass
    
  step_codes = []
  if coord_op_type == "concatenated operation":
    cur.execute('SELECT single_operation_code,op_path_step FROM epsg_coordoperationpath WHERE concat_operation_code = %s ', (op_code,))
    for single_op, step in cur.fetchall():
      step_codes.append(single_op)
    doc['concatop'] = step_codes, # STEP [1235,5678,4234] , codes of transformation
  
  method_code = 0
  method_name = u""
  cur.execute('SELECT coord_op_method_code,coord_op_method_name FROM epsg_coordoperationmethod WHERE coord_op_method_code = %s', (coord_op_method_code,))
  for method_code, method_name in cur.fetchall():
    pass
  values = 0
  cur.execute('SELECT parameter_value, param_value_file_ref FROM epsg_coordoperationparamvalue WHERE coord_op_code = %s', (op_code, ))
  values = cur.fetchall()
  if len(values) == 7:
    v = tuple( map(lambda x: float(x[0]), values) ) # tuple of 7 floats
  elif len(values) == 3:
    v = tuple( map(lambda x: float(x[0]), values) + [0]*4 ) # tuple of 3+4 floats
  elif len(values) == 1 and values[0][1] != '': 
    v = values[0][1] # nadgrid file
  else:
    v=0
  text = str(v).decode('utf-8')
  print text 
  doc = {
    'code': op_code,
    'code_trans' : 0,
    'name': op_name,
    'alt_name' : u"",
    'kind': kind,
    'area': area,
    'deprecated': deprecated,
    'popularity': 1,
    'trans' : u"",
    'trans_alt_name' : u"",
    'trans_remarks': u"",
    'area_trans' : u"",
    'accuracy' : op_accuracy,
    'wkt': text,
    'bbox': bbox,
    'scope': scope,
    'remarks': remarks,
    'information_source': information_source,
    'revision_date': revision_date,
    'datum_code' : 0,
    'source_geogcrs': source_crs,
    'target_crs' : target_crs,
    'children_code' : 0,
    'data_source' : data_source,
    'uom_code' : uom_code,
    'uom' : uom_name,
    'target_uom': u"",
    'prime_meridian' : 0,
    'greenwich_longitude' : 0,
    'concatop' : step_codes,
    'method' : method_name,
    'files' : u"",
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description':u"",
    'primary' : 0,
    'tgrams':name.lower()+" "+area.lower()
    }
  with ix.writer() as writer:
    writer.add_document(**doc)

###############################################################################
print " - SELECT EPSG FROM DATUM"
###############################################################################
prime_meridian_code = 0
cur.execute('SELECT datum_code, datum_name, datum_type, ellipsoid_code, area_of_use_code, datum_scope, remarks, information_source, revision_date, data_source, deprecated, prime_meridian_code  FROM epsg_datum') #  LIMIT 10
for code, name, kind, ellipsoid_code, area_code,scope,remarks,information_source,revision_date,data_source, deprecated, prime_meridian_code in cur.fetchall():
  code = str(code)
    
  kind = kind_list[u"DATUM-"+kind].decode('utf-8')
  
  #if not prime_meridian_code:
  #  prime_meridian_code = 0
  #if not ellipsoid_code:
  #  ellipsoid_code = 0
  
  cur.execute('SELECT area_of_use, area_north_bound_lat, area_west_bound_lon, area_south_bound_lat, area_east_bound_lon FROM epsg_area WHERE area_code = %s;', (area_code,))
  area_of_use = cur.fetchall()
  for area, area_north_bound_lat, area_west_bound_lon, area_south_bound_lat, area_east_bound_lon in area_of_use:
    bbox = area_north_bound_lat,area_west_bound_lon,area_south_bound_lat,area_east_bound_lon
  
  cur.execute('SELECT alias, object_code FROM epsg_alias WHERE object_table_name = %s and object_code = %s', ("epsg_datum",code,))
  for alt_name, object_code in cur.fetchall():
    pass
    
  doc = {
          'code': code + u"-datum",
          'code_trans' : 0,
          'name': name,
          'alt_name' : alt_name,
          'kind': kind,
          'area': area,
          'deprecated': deprecated,
          'popularity': 1.0,
          'trans' : u"",
          'trans_alt_name' : u"",
          'trans_remarks': u"",
          'accuracy' : u"",
          'wkt': u"",
          'bbox': bbox,
          'scope': scope,
          'remarks': remarks,
          'information_source': information_source,
          'revision_date': revision_date,
          'datum_code' : 0,
          'children_code' : ellipsoid_code,
          'data_source' : data_source,
          'uom_code' : 0,
          'uom' : u"",
          'target_uom': u"",
          'prime_meridian' : prime_meridian_code,
          'greenwich_longitude' : 0,
          'concatop' : u"",
          'method' : u"",
          'files' : u"",
          'reverse' : 0,
          'orientation' : u"",
          'abbreviation' : u"",
          'order' : u"",
          'description':u"",
          'primary' : 1,
          'tgrams': name.lower() 
          
          
          
          
    
    }
   
  with ix.writer() as writer:
    writer.add_document(**doc)


###############################################################################
print " - SELECT EPSG FROM ELLIPSOID"
###############################################################################

cur.execute('SELECT ellipsoid_code, ellipsoid_name, uom_code, remarks, information_source, revision_date, data_source, deprecated FROM epsg_ellipsoid') #  LIMIT 10
for code, name, uom_code,remarks,information_source,revision_date,data_source, deprecated in cur.fetchall():
  code = str(code)
  
  cur.execute('SELECT alias, alias_code FROM epsg_alias WHERE object_table_name = %s and object_code = %s', ("epsg_ellipsoid", code, ))
  for alt_name, alias_code in cur.fetchall():
    pass
  
  cur.execute('SELECT unit_of_meas_name, uom_code FROM epsg_unitofmeasure WHERE uom_code = %s ', (uom_code, ))
  for unit_name, uom_code in cur.fetchall():
    pass
  
  doc = {
    'code': code + u"-ellipsoid",
    'code_trans' : 0,
    'name': name,
    'alt_name' : alt_name,
    'area': u"",
    'wkt': u"",
    'bbox': bbox,
    'scope': u"",
    'remarks': remarks,
    'trans_remarks': u"",
    'accuracy' : u"",
    'information_source': information_source,
    'revision_date': revision_date,
    'deprecated': int(deprecated),
    'trans' : u"",
    'trans_alt_name' : u"",
    'datum_code' : 0,
    'uom_code' : uom_code,
    'uom' : unit_name,
    'target_uom': u"",
    'kind': u"ELLIPSOID",
    'popularity': 1.0,
    'children_code' : 0,
    'data_source' : data_source,
    'prime_meridian' : 0,
    'greenwich_longitude' : 0,
    'concatop' : u"",
    'method' : u"",
    'files' : u"",
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description':u"",
    'primary' : 1,
    'tgrams': name.lower()     
    }
    
  with ix.writer() as writer:
    writer.add_document(**doc)
    
###############################################################################
print " - SELECT EPSG FROM PRIME MERIDIAN"
###############################################################################

cur.execute('SELECT prime_meridian_code, prime_meridian_name,greenwich_longitude, uom_code, remarks, information_source, revision_date, data_source, deprecated FROM epsg_primemeridian') # LIMIT 10
for code, name, greenwich_longitude, uom_code,remarks,information_source,revision_date,data_source, deprecated in cur.fetchall():
  code = str(code)

  cur.execute('SELECT unit_of_meas_name,uom_code FROM epsg_unitofmeasure WHERE uom_code = %s ', (uom_code, ))
  for unit_name,uom_code in cur.fetchall():
    pass
 
  doc = {
    'code': code + u"-primemeridian",
    'code_trans' : 0,
    'name': name,
    'alt_name' : u"",
    'area': u"",
    'wkt': u"",
    'bbox': 0,
    'scope': u"",
    'remarks': remarks,
    'trans_remarks': u"",
    'accuracy' : u"",
    'information_source': information_source,
    'revision_date': revision_date,
    'deprecated': int(deprecated),
    'trans' : u"",
    'trans_alt_name' : u"",
    'datum_code' : 0,
    'uom_code' : uom_code,
    'uom' : unit_name,
    'target_uom': u"",
    'kind': u"PRIMEM",
    'popularity': 1.0,
    'children_code' : 0,
    'data_source' : data_source,
    'prime_meridian' : 0,
    'greenwich_longitude' : greenwich_longitude,
    'concatop' : u"",
    'method' : u"",
    'files' : u"",
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description':u"",
    'primary' : 1,
    'tgrams': name.lower()       
    
    

    }
    
    
  with ix.writer() as writer:
    writer.add_document(**doc)

###############################################################################
print " - SELECT EPSG FROM METHOD"
###############################################################################

cur.execute('SELECT coord_op_method_code, coord_op_method_name,reverse_op, remarks, information_source, revision_date, data_source, deprecated FROM epsg_coordoperationmethod') # LIMIT 10
for code, name, reverse, remarks, information_source, revision_date, data_source, deprecated in cur.fetchall():
  code = str(code)


  cur.execute('SELECT alias, alias_code FROM epsg_alias WHERE object_table_name = %s and object_code = %s', ("epsg_coordoperationmethod", code, ))
  for alt_name, alias_code in cur.fetchall():
    pass
    
    
  doc = {
    'code': code + u"-method",
    'code_trans' : 0,
    'name': name,
    'alt_name' : alt_name,
    'area': u"",
    'wkt': u"",
    'bbox': 0,
    'scope': u"",
    'remarks': remarks,
    'trans_remarks': u"",
    'accuracy' : u"",
    'information_source': information_source,
    'revision_date': revision_date,
    'deprecated': int(deprecated),
    'trans' : u"",
    'trans_alt_name' : u"",
    'datum_code' : 0,
    'uom_code' : 0,
    'uom' : u"",
    'target_uom': u"",
    'kind': u"METHOD",
    'popularity': 1.0,
    'children_code' : 0,
    'data_source' : data_source,
    'prime_meridian' : 0,
    'greenwich_longitude' : u"",
    'concatop' : u"",
    'method' : u"",
    'files' : u"",
    'reverse' : reverse,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description':u"",
    'primary' : 1,
    'tgrams': name.lower()       
    
    

    }
  with ix.writer() as writer:
    writer.add_document(**doc)

###############################################################################
print " - SELECT EPSG FROM COORDINATE SYSTEMS"
###############################################################################

cur.execute('SELECT coord_sys_code, coord_sys_name, coord_sys_type, remarks, information_source, revision_date, data_source, deprecated FROM epsg_coordinatesystem') # LIMIT 10
for code, name, kind, remarks, information_source, revision_date, data_source, deprecated in cur.fetchall():
  code = str(code)
  axis_code = []
  cur.execute('SELECT coord_axis_code,coord_axis_name_code FROM epsg_coordinateaxis WHERE coord_sys_code = %s', (code,))
  for axis_codes,axis_name in cur.fetchall():
    axis_code.append(axis_codes)
  
  kind = kind_list["CS-"+kind].decode('utf-8')
  
  
  
  doc = {
    'code': code + u"-coordsys",
    'code_trans' : 0,
    'name': name,
    'alt_name' : u"",
    'area': u"",
    'wkt': u"",
    'bbox': 0,
    'scope': u"",
    'remarks': remarks,
    'trans_remarks': u"",
    'accuracy' : u"",
    'information_source': information_source,
    'revision_date': revision_date,
    'deprecated': int(deprecated),
    'trans' : u"",
    'trans_alt_name' : u"",
    'datum_code' : 0,
    'uom_code' : 0,
    'uom' : u"",
    'target_uom': u"",
    'kind': kind,
    'popularity': 1.0,
    'children_code' : axis_code,
    'data_source' : data_source,
    'prime_meridian' : 0,
    'greenwich_longitude' : u"",
    'concatop' : u"",
    'method' : u"",
    'files' : u"",
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description':u"",
    'primary' : 1,
    'tgrams': name.lower()       

    }
    
  with ix.writer() as writer:
    writer.add_document(**doc)

###############################################################################
print " - SELECT EPSG FROM COORDINATE AXIS"
###############################################################################

cur.execute('SELECT epsg_coordinateaxis.coord_axis_code, epsg_coordinateaxis.coord_sys_code, epsg_coordinateaxis.coord_axis_orientation, epsg_coordinateaxis.coord_axis_abbreviation, epsg_coordinateaxis.uom_code, epsg_coordinateaxis.coord_axis_order, epsg_coordinateaxisname.coord_axis_name, epsg_coordinateaxisname.description, epsg_coordinateaxisname.remarks, epsg_coordinateaxisname.information_source, epsg_coordinateaxisname.data_source, epsg_coordinateaxisname.revision_date, epsg_coordinateaxisname.deprecated FROM epsg_coordinateaxis LEFT JOIN epsg_coordinateaxisname ON epsg_coordinateaxis.coord_axis_name_code=epsg_coordinateaxisname.coord_axis_name_code') # LIMIT 10 
for code, sys_code, orientation, abbreviation, uom_code, order, axis_name, description, remarks, information_source, data_source, revision_date, deprecated  in cur.fetchall():
  code = str(code)
  cur.execute('SELECT unit_of_meas_name,uom_code FROM epsg_unitofmeasure WHERE uom_code = %s ', (uom_code, ))
  for unit_name,uom_code in cur.fetchall():
    pass
   
  doc = {
    'code': code + u"-axis",
    'code_trans' : 0,
    'name': axis_name,
    'alt_name' : u"",
    'area': u"",
    'wkt': u"",
    'bbox': 0,
    'scope': u"",
    'remarks': remarks,
    'trans_remarks': u"",
    'accuracy' : u"",
    'information_source': information_source,
    'revision_date': revision_date,
    'deprecated': int(deprecated),
    'trans' : u"",
    'trans_alt_name' : u"",
    'datum_code' : 0,
    'uom_code' : uom_code,
    'uom' : unit_name,
    'target_uom': u"",
    'kind': u"AXIS",
    'popularity': 1.0,
    'children_code' : sys_code, #for connect to coordinate system
    'data_source' : data_source,
    'prime_meridian' : 0,
    'greenwich_longitude' : u"",
    'concatop' : u"",
    'method' : u"",
    'files' : u"",
    'reverse' : 0,
    'orientation' : orientation,
    'abbreviation' : abbreviation,
    'order' : order,
    'description': description,
    'primary' : 1,
    'tgrams': name.lower()       
    

    }





  with ix.writer() as writer:
    writer.add_document(**doc)

###############################################################################
print " - SELECT EPSG FROM AREA"
###############################################################################

cur.execute('SELECT area_code, area_name, area_of_use, area_south_bound_lat, area_north_bound_lat, area_west_bound_lon, area_east_bound_lon, area_polygon_file_ref, remarks,information_source,data_source,revision_date,deprecated FROM epsg_area') # LIMIT 10
for code, name, area,area_south_bound_lat,area_north_bound_lat,area_west_bound_lon,area_east_bound_lon,area_polygon_file_ref,remarks,information_source,data_source,revision_date, deprecated in cur.fetchall():
  code = str(code)
  bbox = area_north_bound_lat,area_west_bound_lon,area_south_bound_lat,area_east_bound_lon
  
  cur.execute('SELECT alias, alias_code FROM epsg_alias WHERE object_table_name = %s and object_code = %s', ("epsg_area", code, ))
  for alt_name, alias_code in cur.fetchall():
    pass
    

  doc = {
    'code': code + u"-area",
    'code_trans' : 0,
    'name': name,
    'alt_name' : alt_name,
    'area': area,
    'wkt': u"",
    'bbox': bbox,
    'scope': u"",
    'remarks': remarks,
    'trans_remarks': u"",
    'accuracy' : u"",
    'information_source': information_source,
    'revision_date': revision_date,
    'deprecated': int(deprecated),
    'trans' : u"",
    'trans_alt_name' : u"",
    'datum_code' : 0,
    'uom_code' : 0,
    'uom' : u"",
    'target_uom': u"",
    'kind': u"AREA",
    'popularity': 1.0,
    'children_code' : 0,
    'data_source' : data_source,
    'prime_meridian' : 0,
    'greenwich_longitude' : u"",
    'concatop' : u"",
    'method' : u"",
    'files': area_polygon_file_ref,
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description': u"",
    'primary' : 1,
    'tgrams': name.lower()    
    }




  with ix.writer() as writer:
    writer.add_document(**doc)


###############################################################################
print " - SELECT EPSG FROM UNIT OF MEASURE"
###############################################################################

cur.execute('SELECT uom_code, unit_of_meas_name, unit_of_meas_type, target_uom_code, remarks, information_source, data_source, revision_date, deprecated FROM epsg_unitofmeasure') #  LIMIT 10
for code, name, kind, target_uom, remarks, information_source, data_source, revision_date, deprecated in cur.fetchall():
  code = str(code)
  
  cur.execute('SELECT alias, alias_code FROM epsg_alias WHERE object_table_name = %s and object_code = %s', ("epsg_unitofmeasure", code, ))
  for alt_name, alias_code in cur.fetchall():
    pass
  kind = kind_list[u"UNIT-"+kind].decode('utf-8')
  
  doc = {
    'code': code + u"-units",
    'code_trans' : 0,
    'name': name,
    'alt_name' : alt_name,
    'area': u"",
    'wkt': u"",
    'bbox': u"",
    'scope': u"",
    'remarks': remarks,
    'trans_remarks': u"",
    'accuracy' : u"",
    'information_source': information_source,
    'revision_date': revision_date,
    'deprecated': int(deprecated),
    'trans' : u"",
    'trans_alt_name' : u"",
    'datum_code' : 0,
    'uom_code' : 0,
    'uom' : u"",
    'target_uom': target_uom,
    'kind': kind,
    'popularity': 1.0,
    'children_code' : 0,
    'data_source' : data_source,
    'prime_meridian' : 0,
    'greenwich_longitude' : u"",
    'concatop' : u"",
    'method' : u"",
    'files': u"",
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description': u"",
    'primary' : 1,
    'tgrams':name.lower()    
    }
    

  with ix.writer() as writer:
    writer.add_document(**doc)
      