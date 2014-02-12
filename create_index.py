#!/usr/bin/env python
# -*- coding: utf-8 -*-
DATABASE = ('dbname=epsg83 user=tompohys host=localhost')
INDEX = "index"
CRS_EXCEPTIONS = 'CRS_exceptions.csv'

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
from whoosh.analysis import StemmingAnalyzer # removing suffixes (and sometimes prefixes)
import csv
from whoosh.writing import BufferedWriter

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
  'UNIT-time' : "UNIT-TIMEUNIT",
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

print " - CRS_EXCEPTIONS"
crs_ex_line = {}
try:
  with open(CRS_EXCEPTIONS) as crs_ex:
    text = csv.reader(crs_ex, delimiter = ',')
    # skip the header
    next(text, None)    
    for row in text:
      crs_ex_line[row[0]] = row
    #print crs_ex_line['4326'][2]
    #print crs_ex_line
except:
  print "!!! FAILED: NO CRS_EXCEPTIONS !!!"
  sys.exit(1)

print " - WHOOSH!"
class EPSGSchema(SchemaClass):
  
  code = TEXT(stored = True, field_boost=5.0) # "EPSG:4326" #coord_ref_sys_code
  code_trans = NUMERIC(stored = True) #, field_boost = 5.0
  name = TEXT(stored = True, field_boost=3.0) # Name "WGS 84" #coord_ref_sys_name
  alt_name = TEXT (stored = True)
  kind = TEXT(stored = True, sortable=True) # "ProjectedCRS" | "GeodeticCRS" #coord_ref_sys_kind
  area = TEXT(stored = True) #epsg_area/area_of_use
  area_trans = TEXT(stored = True)
  deprecated = BOOLEAN(stored = True) # "1 = Valid", "0 - Invalid"
  # popularity = STORED  # number [0..1] - our featured = 1

  # Description of used transformation - "", "Czech republic (accuracy 1 meter)"
  trans = NUMERIC(stored = True) # area of used towgs transformation + (accuracy) else ""
  trans_alt_name = TEXT(stored = True)
  trans_remarks = STORED
  accuracy = STORED
  
  # Specific fields for all coordinate systems
  #wkt = TEXT(stored = True)
  bbox = STORED # [area_north_bound_lat,area_west_bound_lon,area_south_bound_lat,area_east_bound_lon]

  scope = STORED # crs_scope
  remarks = STORED # remarks
  information_source = STORED # information_source
  revision_date = STORED # revision_date

  # Advanced with additional types such as "Elipsoid" | "Area" | ...
  datum = TEXT(stored=True) 
  geogcrs = TEXT(stored=True)
  target_crs = STORED
  #children_code = NUMERIC(stored=True)
  data_source = STORED
  uom = STORED
  target_uom = STORED
  primem = TEXT(stored=True)
  greenwich_longitude = STORED
  concatop = STORED
  method = TEXT(stored=True)
  files = STORED
  reverse = STORED
  orientation = STORED
  abbreviation = STORED
  order = STORED
  description = STORED
  primary = STORED
  uom_code = STORED
  area_code = NUMERIC(stored=True)
  area_trans_code = NUMERIC(stored=True)
  
  #tgrams = NGRAM(minsize=2, maxsize=4, stored=False)
  #datum_name = TEXT(stored = True, sortable=True, spelling=True, field_boost=3.0, analyzer=stem_ana)
  #datum_deprecated = BOOLEAN(stored = True)
  #towgs = ID(stored = True) # epsg code for transformation used in wkt or empty
  #geogcs = ID(stored = True) # 
  #ellipsoid_code = NUMERIC(stored = True, field_boost=5.0) 
  #ellipsoid_name = TEXT(stored = True, sortable=True, spelling=True, field_boost=3.0 ,analyzer=stem_ana)
  #ellipsoid_deprecated = BOOLEAN(stored = True)
  
  # Specific for projected coordinate systems
  #projection = ID(stored = True)
  
  # CRS_exceptions
  alt_title = TEXT(stored = True, field_boost=3.0)
  code_id = ID(stored = True, unique=True)
  alt_code = NUMERIC(stored = True)
  alt_description = TEXT(stored=True)
  ellipsoid = TEXT(stored=True)
  cs = TEXT(stored=True)
  axis = STORED
  # frontpage_section = STORED
  # frontpage_title = STORED
  # importance = STORED
  

# MAKE DIRECTORY AND CREATE INDEX
if not os.path.exists(INDEX):
    os.mkdir(INDEX)

ix = create_in(INDEX, EPSGSchema)

###############################################################################
print " - SELECT EPSG FROM COORDINATE REFERENCE SYSTEM AND TRANSFORMATION"
###############################################################################
ref = osr.SpatialReference()
#writer = BufferedWriter(ix, period=0, limit = 200)
cur.execute('SELECT coord_ref_sys_code, coord_ref_sys_name,crs_scope, remarks, information_source, revision_date, datum_code, area_of_use_code,coord_ref_sys_kind,deprecated,source_geogcrs_code,data_source,coord_sys_code  FROM epsg_coordinatereferencesystem') #  WHERE coord_ref_sys_code > 5513 and coord_ref_sys_code < 5600 or coord_ref_sys_code = 4156  #WHERE coord_ref_sys_code > 5513 and coord_ref_sys_code < 5600'
for code, name, scope, remarks, information_source, revision_date,datum_code, area_code, coord_ref_sys_kind, deprecated, source_geogcrs_code,data_source,coord_sys_code in cur.fetchall():
  if source_geogcrs_code == None:
    source_geogcrs_code = code
  try:
    name = name.encode('LATIN1').decode('utf-8')
  except:
    print "NOT POSIBLE TO DECODE:", code, name
    continue
  
  # #Load WKT from GDAL
  # ref = osr.SpatialReference()
  ref.ImportFromEPSG(int(code))  
  # text = ref.ExportToWkt().decode('utf-8')
  
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
  cur.execute('SELECT coord_ref_sys_name,coord_ref_sys_code, datum_code FROM epsg_coordinatereferencesystem WHERE coord_ref_sys_code = %s', (source_geogcrs_code,))
  for coord_ref_sys_name, coord_ref_sys_code, datum_code in cur.fetchall():
    gcrs = str(coord_ref_sys_code), str(coord_ref_sys_name)
    pass
  
  # Get ellipsoid code from datum
  cur.execute('SELECT epsg_ellipsoid.ellipsoid_code, datum_code,prime_meridian_code,datum_name,epsg_ellipsoid.ellipsoid_name FROM epsg_datum LEFT JOIN epsg_ellipsoid ON epsg_datum.ellipsoid_code=epsg_ellipsoid.ellipsoid_code WHERE datum_code = %s', (datum_code,))
  for ellipsoid_code, datum_code, prime_meridian_code,datum_name,ellipsoid_name in cur.fetchall():
    datum = str(datum_code),str(datum_name)
    ellipsoid = str(ellipsoid_code), str(ellipsoid_name)
  
  # Get greenwich_longitude different from greenwich
  cur.execute('SELECT prime_meridian_name,prime_meridian_code,greenwich_longitude FROM epsg_primemeridian WHERE prime_meridian_code= %s',(prime_meridian_code,))
  for prime_meridian_name, prime_meridian_code, greenwich_longitude in cur.fetchall():
    prime_meridian = str(prime_meridian_code), str(prime_meridian_name)
    
  # Get unit code from coordinate axis
  cur.execute('SELECT epsg_coordinatesystem.coord_sys_code, epsg_coordinatesystem.coord_sys_name, epsg_coordinateaxis.uom_code FROM epsg_coordinatesystem LEFT JOIN epsg_coordinateaxis ON epsg_coordinateaxis.coord_sys_code = epsg_coordinatesystem.coord_sys_code WHERE epsg_coordinatesystem.coord_sys_code = %s', (coord_sys_code,))
  for coord_sys_code, coord_sys_name, uom_code in cur.fetchall():
    coord_sys = str(coord_sys_code), coord_sys_name
    
  # Get uom_name code from uom
  cur.execute('SELECT uom_code, unit_of_meas_name FROM epsg_unitofmeasure WHERE uom_code = %s', (uom_code,))
  for uom_code, unit_of_meas_name in cur.fetchall():
    pass

  # popularity = 0.0
  deprecated = int(deprecated)
  code = str(code).decode('utf-8')
  kind = u""
  if kind_list.has_key(coord_ref_sys_kind):
    kind = kind_list[coord_ref_sys_kind].decode('utf-8')

  # boost by kind
  boost = 0
  if kind == "CRS-PROJCRS":
    boost = 0.2
  if kind == "CRS-GEOGCRS" or kind == "CRS-GEOG3DCRS":
    boost = 0.05
  # boost by code from csv file
  importance = 0
  try:
    importance = crs_ex_line[code][1]
    if importance == u"":
      importance = 0
  except:
    pass
  
  
  score = float((1 + boost) * (1 + float(importance)*4))
  
  doc = {
    'code': code,
    'code_id':code,
    'code_trans' : 0,
    'name': name,
    'alt_name' : alt_name,
    'kind': kind,
    'area': area,
    'area_code': area_code,
    'deprecated': deprecated,
    # 'popularity': popularity,
    'trans' : u"",
    'trans_alt_name' : u"",
    'trans_remarks': u"",
    'area_trans' : u"",
    'accuracy' : u"",
    #'wkt': text,
    'bbox': bbox,
    'scope': scope,
    'remarks': remarks,
    'information_source': information_source,
    'revision_date': revision_date,
    'datum' : datum,
    'geogcrs': gcrs,
    #'children_code' : coord_sys_code,
    'data_source' : data_source,
    'uom_code' : uom_code,
    'uom' : unit_of_meas_name,
    'target_uom': u"",
    'primem' : prime_meridian,
    'greenwich_longitude' : greenwich_longitude,
    'concatop' : u"",
    'method' : u"",
    'files' : u"",
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description':u"",
    'primary' : 0,
    #'tgrams':name.lower()+" "+area.lower(),
    'ellipsoid' : ellipsoid,
    'cs': coord_sys,
    '_boost' : score
  }  
# transofrmation to wgs84
  cur.execute('SELECT epsg_coordoperation.coord_op_code, epsg_coordoperation.coord_op_accuracy, epsg_coordoperation.coord_op_type, epsg_coordoperation.deprecated, epsg_coordoperation.coord_op_scope, epsg_coordoperation.remarks, epsg_coordoperation.information_source, epsg_coordoperation.revision_date, epsg_coordoperation.uom_code_source_coord_diff,epsg_coordoperation.coord_op_method_code,epsg_coordoperation.area_of_use_code, epsg_area.area_of_use, epsg_area.area_north_bound_lat, epsg_area.area_west_bound_lon, epsg_area.area_south_bound_lat, epsg_area.area_east_bound_lon FROM epsg_coordoperation LEFT JOIN epsg_area ON area_of_use_code = area_code  WHERE source_crs_code = %s and target_crs_code = 4326',(source_geogcrs_code,))
  towgs84 = cur.fetchall()  
  op_code_original = 0
  op_code_trans = {}
  towgs84_original = ref.GetTOWGS84()
  transformations = []
  if len(towgs84) != 0:
    for op_code, op_accuracy, coord_op_type, opdeprecated, coord_op_scope, remarks, information_source, revision_date,uom_code, coord_op_method_code, area_code,area, area_north_bound_lat, area_west_bound_lon, area_south_bound_lat, area_east_bound_lon in towgs84:
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
      cur.execute('SELECT coord_op_method_code, coord_op_method_name FROM epsg_coordoperationmethod WHERE coord_op_method_code= %s', (coord_op_method_code,))
      for coord_op_method_code,coord_op_method_name in cur.fetchall():
        coord_op_method = str(coord_op_method_code), coord_op_method_name
      if op_accuracy == None or op_accuracy == 0.0:
        op_accuracy = u'unknown'
      #   popularity_acc = -0.02
      # else:
      #   popularity_acc = 0.02
      #         
      op_code_trans[op_code] = v
      if towgs84_original == v:
        op_code_original = op_code
        doc['area_trans'] = area
        doc['area_trans_code'] = area_code
        doc['accuracy'] = op_accuracy
        #doc['wkt'] = text
        doc['primary'] = 1
        doc['method'] = coord_op_method
        doc['code_trans'] = op_code
        # doc['popularity'] = popularity_acc + popularity_kind + 0.1
      
      transformations.append(op_code)
    
    if op_code == op_code_original:    
      doc['trans'] = transformations
    else:
      # CRS has transformation to wgs84, but any transformation is not default 
      doc['trans'] = transformations
      doc['primary'] = 0
      # doc['popularity'] = popularity_acc + popularity_kind
      
  with ix.writer(procs=4, limitmb=1048, multisegment=True) as writer:
    writer.add_document(**doc)

###############################################################################
print " - SELECT EPSG FROM OPERATIONS"
###############################################################################
#writer = BufferedWriter(ix, period=0, limit = 200)

cur.execute('SELECT epsg_coordoperation.coord_op_code,epsg_coordoperation.coord_op_name,epsg_coordoperation.coord_op_accuracy, epsg_coordoperation.coord_op_type,epsg_coordoperation.source_crs_code,epsg_coordoperation.target_crs_code, epsg_coordoperation.deprecated, epsg_coordoperation.coord_op_scope, epsg_coordoperation.remarks, epsg_coordoperation.information_source, epsg_coordoperation.revision_date, epsg_coordoperation.uom_code_source_coord_diff,epsg_coordoperation.coord_op_method_code, epsg_coordoperation.data_source, epsg_coordoperation.area_of_use_code, epsg_area.area_of_use, epsg_area.area_north_bound_lat, epsg_area.area_west_bound_lon, epsg_area.area_south_bound_lat, epsg_area.area_east_bound_lon FROM epsg_coordoperation LEFT JOIN epsg_area ON area_of_use_code = area_code')
for op_code,op_name, op_accuracy, coord_op_type, source_crs, target_crs, deprecated, scope, remarks, information_source, revision_date, uom_code, method_code, data_source, area_code, area, area_north_bound_lat, area_west_bound_lon, area_south_bound_lat, area_east_bound_lon in cur.fetchall():
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
  
  method = u""
  cur.execute('SELECT coord_op_method_code,coord_op_method_name FROM epsg_coordoperationmethod WHERE coord_op_method_code = %s', (method_code,))
  for method_code, method_name in cur.fetchall():
    method = str(method_code), method_name
  
  gcrs = u""
  datum_code = u""
  if source_crs:
    cur.execute('SELECT coord_ref_sys_name,source_geogcrs_code, datum_code, coord_ref_sys_code FROM epsg_coordinatereferencesystem WHERE coord_ref_sys_code = %s', (source_crs,))
    for coord_ref_sys_name, source_geogcrs, datum_code, coord_ref_sys_code in cur.fetchall():
      gcrs = str(coord_ref_sys_code), coord_ref_sys_name
      pass
  

  # Get ellipsoid code from datum
  prime_meridian_code = u""
  datum = u""
  ellipsoid = u""
  if datum_code:
    cur.execute('SELECT epsg_ellipsoid.ellipsoid_code, datum_code,prime_meridian_code,datum_name,epsg_ellipsoid.ellipsoid_name FROM epsg_datum LEFT JOIN epsg_ellipsoid ON epsg_datum.ellipsoid_code=epsg_ellipsoid.ellipsoid_code WHERE datum_code = %s', (datum_code,))
    for ellipsoid_code, datum_code, prime_meridian_code,datum_name,ellipsoid_name in cur.fetchall():
      datum = str(datum_code),str(datum_name)
      ellipsoid = str(ellipsoid_code), str(ellipsoid_name)
    
  
  # Get greenwich_longitude different from greenwich
  prime_meridian = u""
  greenwich_longitude = u""
  if prime_meridian_code:
    cur.execute('SELECT prime_meridian_name,prime_meridian_code,greenwich_longitude FROM epsg_primemeridian WHERE prime_meridian_code= %s',(prime_meridian_code,))
    for prime_meridian_name, prime_meridian_code, greenwich_longitude in cur.fetchall():
      prime_meridian = str(prime_meridian_code), str(prime_meridian_name)
  
    
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

  doc = {
    'code': op_code,
    'code_trans' : 0,
    'name': op_name,
    'alt_name' : u"",
    'kind': kind,
    'area': area,
    'area_code': area_code,
    'deprecated': deprecated,
    # 'popularity': 0,
    'trans' : u"",
    'trans_alt_name' : u"",
    'trans_remarks': u"",
    'area_trans' : u"",
    'accuracy' : op_accuracy,
    #'wkt': text,
    'bbox': bbox,
    'scope': scope,
    'remarks': remarks,
    'information_source': information_source,
    'revision_date': revision_date,
    'datum' : datum,
    'geogcrs': gcrs,
    'target_crs' : target_crs,
    #'children_code' : 0,
    'data_source' : data_source,
    'uom_code' : uom_code,
    'uom' : uom_name,
    'target_uom': u"",
    'primem' : prime_meridian,
    'greenwich_longitude' : greenwich_longitude,
    'concatop' : step_codes,
    'method' : method,
    'files' : u"",
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description': text,
    'primary' : 0,
    #'tgrams':name.lower()+" "+area.lower(),
    'ellipsoid':ellipsoid
  }
  with ix.writer(procs=4, limitmb=1048, multisegment=True) as writer:
    writer.add_document(**doc)
#   writer.add_document(**doc )
# writer.close()

###############################################################################
print " - SELECT EPSG FROM DATUM"
###############################################################################
#writer = BufferedWriter(ix, period=0, limit = 200)

prime_meridian_code = 0
cur.execute('SELECT datum_code, datum_name, datum_type, ellipsoid_code, area_of_use_code, datum_scope, remarks, information_source, revision_date, data_source, deprecated, prime_meridian_code  FROM epsg_datum')
for code, name, kind, ellipsoid_code, area_code,scope,remarks,information_source,revision_date,data_source, deprecated, prime_meridian_code in cur.fetchall():
  code = str(code)
    
  kind = kind_list[u"DATUM-"+kind].decode('utf-8')
  
  #if not prime_meridian_code:
  #  prime_meridian_code = 0
  #if not ellipsoid_code:
  #  ellipsoid_code = 0
  
  # Get ellipsoid code from datum
  ellipsoid = u""
  cur.execute('SELECT ellipsoid_code,ellipsoid_name FROM epsg_ellipsoid WHERE ellipsoid_code = %s', (ellipsoid_code,))
  for ellipsoid_code, ellipsoid_name in cur.fetchall():
    ellipsoid = str(ellipsoid_code), str(ellipsoid_name)
  
  # Get greenwich_longitude different from greenwich
  prime_meridian = u""
  greenwich_longitude = u""
  cur.execute('SELECT prime_meridian_name,prime_meridian_code,greenwich_longitude FROM epsg_primemeridian WHERE prime_meridian_code= %s',(prime_meridian_code,))
  for prime_meridian_name, prime_meridian_code, greenwich_longitude in cur.fetchall():
    prime_meridian = str(prime_meridian_code), str(prime_meridian_name)
  
  cur.execute('SELECT area_of_use, area_north_bound_lat, area_west_bound_lon, area_south_bound_lat, area_east_bound_lon FROM epsg_area WHERE area_code = %s;', (area_code,))
  area_of_use = cur.fetchall()
  for area, area_north_bound_lat, area_west_bound_lon, area_south_bound_lat, area_east_bound_lon in area_of_use:
    bbox = area_north_bound_lat,area_west_bound_lon,area_south_bound_lat,area_east_bound_lon
  
  alt_name = u""
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
    'area_code': area_code,
    'area_trans' : u"",
    'deprecated': deprecated,
    # 'popularity': 0.0,
    'trans' : u"",
    'trans_alt_name' : u"",
    'trans_remarks': u"",
    'accuracy' : u"",
    #'wkt': u"",
    'bbox': bbox,
    'scope': scope,
    'remarks': remarks,
    'information_source': information_source,
    'revision_date': revision_date,
    'datum' : u"",
    #'children_code' : ellipsoid_code,
    'data_source' : data_source,
    'uom_code' : 0,
    'uom' : u"",
    'target_uom': u"",
    'primem' : prime_meridian,
    'greenwich_longitude' : greenwich_longitude,
    'concatop' : u"",
    'method' : u"",
    'files' : u"",
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description':u"",
    'primary' : 0,
    #'tgrams': name.lower(),
    'ellipsoid':ellipsoid 
  }
  with ix.writer(procs=4, limitmb=1048, multisegment=True) as writer:
    writer.add_document(**doc)   
#   writer.add_document(**doc )
# writer.close()

###############################################################################
print " - SELECT EPSG FROM ELLIPSOID"
###############################################################################
#writer = BufferedWriter(ix, period=0, limit = 100)

cur.execute('SELECT ellipsoid_code, ellipsoid_name, uom_code, remarks, information_source, revision_date, data_source, deprecated FROM epsg_ellipsoid')
for code, name, uom_code,remarks,information_source,revision_date,data_source, deprecated in cur.fetchall():
  code = str(code)
  
  alt_name = u""
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
    #'wkt': u"",
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
    'area_trans' : u"",
    'datum' : u"",
    'uom_code' : uom_code,
    'uom' : unit_name,
    'target_uom': u"",
    'kind': u"ELLIPSOID",
    # 'popularity': 0,
    #'children_code' : 0,
    'data_source' : data_source,
    'primem' : u"",
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
    #'tgrams': name.lower()     
  }
  with ix.writer(procs=4, limitmb=1048, multisegment=True) as writer:
    writer.add_document(**doc)    
#   writer.add_document(**doc )
# writer.close() 

###############################################################################
print " - SELECT EPSG FROM PRIME MERIDIAN"
###############################################################################
#writer = BufferedWriter(ix, period=0, limit = 100)

cur.execute('SELECT prime_meridian_code, prime_meridian_name,greenwich_longitude, uom_code, remarks, information_source, revision_date, data_source, deprecated FROM epsg_primemeridian')
for code, name, greenwich_longitude, uom_code,remarks,information_source,revision_date,data_source, deprecated in cur.fetchall():
  code = str(code)

  cur.execute('SELECT unit_of_meas_name,uom_code FROM epsg_unitofmeasure WHERE uom_code = %s ', (uom_code, ))
  for unit_name,uom_code in cur.fetchall():
    pass
 
  doc = {
    'code': code + u"-primem",
    'code_trans' : 0,
    'name': name,
    'alt_name' : u"",
    'area': u"",
    #'wkt': u"",
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
    'area_trans' : u"",
    'datum' : u"",
    'uom_code' : uom_code,
    'uom' : unit_name,
    'target_uom': u"",
    'kind': u"PRIMEM",
    # 'popularity': 0,
    #'children_code' : 0,
    'data_source' : data_source,
    'primem' : u"",
    'greenwich_longitude' : greenwich_longitude,
    'concatop' : u"",
    'method' : u"",
    'files' : u"",
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description':u"",
    'primary' : 0,
    #'tgrams': name.lower()

  }
  with ix.writer(procs=4, limitmb=1048, multisegment=True) as writer:
    writer.add_document(**doc)
#   writer.add_document(**doc )
# writer.close()

###############################################################################
print " - SELECT EPSG FROM METHOD"
###############################################################################
#writer = BufferedWriter(ix, period=0, limit = 100)

cur.execute('SELECT coord_op_method_code, coord_op_method_name,reverse_op, remarks, information_source, revision_date, data_source, deprecated FROM epsg_coordoperationmethod')
for code, name, reverse, remarks, information_source, revision_date, data_source, deprecated in cur.fetchall():
  code = str(code)

  alt_name = u""
  cur.execute('SELECT alias, alias_code FROM epsg_alias WHERE object_table_name = %s and object_code = %s', ("epsg_coordoperationmethod", code, ))
  for alt_name, alias_code in cur.fetchall():
    pass
    
    
  doc = {
    'code': code + u"-method",
    'code_trans' : 0,
    'name': name,
    'alt_name' : alt_name,
    'area': u"",
    #'wkt': u"",
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
    'area_trans' : u"",
    'datum' : u"",
    'uom_code' : 0,
    'uom' : u"",
    'target_uom': u"",
    'kind': u"METHOD",
    # 'popularity': 0,
   # 'children_code' : 0,
    'data_source' : data_source,
    'primem' : u"",
    'greenwich_longitude' : u"",
    'concatop' : u"",
    'method' : u"",
    'files' : u"",
    'reverse' : reverse,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description':u"",
    'primary' : 0,
    #'tgrams': name.lower()       

  }
  with ix.writer(procs=4, limitmb=1048, multisegment=True) as writer:
    writer.add_document(**doc)
#   writer.add_document(**doc )
# writer.close()
###############################################################################
print " - SELECT EPSG FROM COORDINATE SYSTEMS"
###############################################################################
#writer = BufferedWriter(ix, period=0, limit = 100)

cur.execute('SELECT coord_sys_code, coord_sys_name, coord_sys_type, remarks, information_source, revision_date, data_source, deprecated FROM epsg_coordinatesystem')
for code, name, kind, remarks, information_source, revision_date, data_source, deprecated in cur.fetchall():
  code = str(code)
  axis_code = []
  cur.execute('SELECT epsg_coordinateaxis.coord_axis_code,epsg_coordinateaxis.coord_axis_name_code, epsg_coordinateaxisname.coord_axis_name FROM epsg_coordinateaxis LEFT JOIN epsg_coordinateaxisname ON epsg_coordinateaxis.coord_axis_name_code=epsg_coordinateaxisname.coord_axis_name_code WHERE epsg_coordinateaxis.coord_sys_code = %s', (code,))
  
  for coord_axis_code,coord_axis_name_code,coord_axis_name in cur.fetchall():
    axis_code.append({'axis_code': coord_axis_code, 'axis_name':coord_axis_name})
  
  kind = kind_list["CS-"+kind].decode('utf-8')
  

  
  doc = {
    'code': code + u"-cs",
    'code_trans' : 0,
    'name': name,
    'alt_name' : u"",
    'area': u"",
    #'wkt': u"",
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
    'area_trans' : u"",
    'datum' : u"",
    'uom_code' : 0,
    'uom' : u"",
    'target_uom': u"",
    'kind': kind,
    # 'popularity': 0,
   # 'children_code' : 0,
    'data_source' : data_source,
    'primem' : u"",
    'greenwich_longitude' : u"",
    'concatop' : u"",
    'method' : u"",
    'files' : u"",
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description':u"",
    'primary' : 0,
    #'tgrams': name.lower(),      
    'axis':axis_code
  }
  with ix.writer(procs=4, limitmb=1048, multisegment=True) as writer:
    writer.add_document(**doc)
#   writer.add_document(**doc )
# writer.close()


###############################################################################
print " - SELECT EPSG FROM COORDINATE AXIS"
###############################################################################
#writer = BufferedWriter(ix, period=0, limit = 100)

cur.execute('SELECT epsg_coordinateaxis.coord_axis_code, epsg_coordinateaxis.coord_sys_code, epsg_coordinateaxis.coord_axis_orientation, epsg_coordinateaxis.coord_axis_abbreviation, epsg_coordinateaxis.uom_code, epsg_coordinateaxis.coord_axis_order, epsg_coordinateaxisname.coord_axis_name, epsg_coordinateaxisname.description, epsg_coordinateaxisname.remarks, epsg_coordinateaxisname.information_source, epsg_coordinateaxisname.data_source, epsg_coordinateaxisname.revision_date, epsg_coordinateaxisname.deprecated FROM epsg_coordinateaxis LEFT JOIN epsg_coordinateaxisname ON epsg_coordinateaxis.coord_axis_name_code=epsg_coordinateaxisname.coord_axis_name_code') 
for code, sys_code, orientation, abbreviation, uom_code, order, axis_name, description, remarks, information_source, data_source, revision_date, deprecated  in cur.fetchall():
  code = str(code)
  cur.execute('SELECT unit_of_meas_name,uom_code FROM epsg_unitofmeasure WHERE uom_code = %s ', (uom_code, ))
  for unit_name,uom_code in cur.fetchall():
    pass
  
  coord_sys = u""
  # Get unit code from coordinate axis
  cur.execute('SELECT coord_sys_code, coord_sys_name FROM epsg_coordinatesystem WHERE coord_sys_code = %s', (sys_code,))
  for coord_sys_code, coord_sys_name in cur.fetchall():
    coord_sys = str(coord_sys_code), coord_sys_name 
    
  doc = {
    'code': code + u"-axis",
    'code_trans' : 0,
    'name': axis_name,
    'alt_name' : u"",
    'area': u"",
    #'wkt': u"",
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
    'area_trans' : u"",
    'datum' : u"",
    'uom_code' : uom_code,
    'uom' : unit_name,
    'target_uom': u"",
    'kind': u"AXIS",
    # 'popularity': 0,
   # 'children_code' : 0, 
    'data_source' : data_source,
    'primem' : u"",
    'greenwich_longitude' : u"",
    'concatop' : u"",
    'method' : u"",
    'files' : u"",
    'reverse' : 0,
    'orientation' : orientation,
    'abbreviation' : abbreviation,
    'order' : order,
    'description': description,
    'primary' : 0,
    #'tgrams': name.lower(),
    'cs': coord_sys,

  }
  with ix.writer(procs=4, limitmb=1048, multisegment=True) as writer:
    writer.add_document(**doc)
#   writer.add_document(**doc )
# writer.close()

###############################################################################
print " - SELECT EPSG FROM AREA"
###############################################################################
#writer = BufferedWriter(ix, period=0, limit = 200)

cur.execute('SELECT area_code, area_name, area_of_use, area_south_bound_lat, area_north_bound_lat, area_west_bound_lon, area_east_bound_lon, area_polygon_file_ref, remarks,information_source,data_source,revision_date,deprecated FROM epsg_area')
for code, name, area,area_south_bound_lat,area_north_bound_lat,area_west_bound_lon,area_east_bound_lon,area_polygon_file_ref,remarks,information_source,data_source,revision_date, deprecated in cur.fetchall():
  code = str(code)
  bbox = area_north_bound_lat,area_west_bound_lon,area_south_bound_lat,area_east_bound_lon
  
  alt_name = u""
  cur.execute('SELECT alias, alias_code FROM epsg_alias WHERE object_table_name = %s and object_code = %s', ("epsg_area", code, ))
  for alt_name, alias_code in cur.fetchall():
    pass
    

  doc = {
    'code': code + u"-area",
    'area_code':int(code),
    'code_trans' : 0,
    'name': name,
    'alt_name' : alt_name,
    'area': area,
    #'wkt': u"",
    'bbox': bbox,
    'scope': u"",
    'remarks': remarks,
    'trans_remarks': u"",
    'accuracy' : u"",
    'information_source': information_source,
    'revision_date': revision_date,
    'deprecated': int(deprecated),
    'area_trans' : u"",
    'trans' : u"",
    'trans_alt_name' : u"",
    'datum' : u"",
    'uom_code' : 0,
    'uom' : u"",
    'target_uom': u"",
    'kind': u"AREA",
    # 'popularity': 0,
   # 'children_code' : 0,
    'data_source' : data_source,
    'primem' : u"",
    'greenwich_longitude' : u"",
    'concatop' : u"",
    'method' : u"",
    'files': area_polygon_file_ref,
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description': u"",
    'primary' : 0,
    #'tgrams': name.lower()    
  }
  with ix.writer(procs=4, limitmb=1048, multisegment=True) as writer:
    writer.add_document(**doc)
#   writer.add_document(**doc )
# writer.close()

###############################################################################
print " - SELECT EPSG FROM UNIT OF MEASURE"
###############################################################################
#writer = BufferedWriter(ix, period=0, limit = 100)

cur.execute('SELECT uom_code, unit_of_meas_name, unit_of_meas_type, target_uom_code, remarks, information_source, data_source, revision_date, deprecated, factor_b, factor_c, change_id FROM epsg_unitofmeasure')
for code, name, kind, target_uom_code, remarks, information_source, data_source, revision_date, deprecated, factor_b, factor_c, change_id in cur.fetchall():
  code = str(code)
  alt_name = u""
  alias_code = 0
  cur.execute('SELECT alias, alias_code FROM epsg_alias WHERE object_table_name = %s and object_code = %s', ("epsg_unitofmeasure", code, ))
  for alt_name, alias_code in cur.fetchall():
    pass
  kind = kind_list[u"UNIT-"+kind].decode('utf-8')
  
  cur.execute('SELECT uom_code,unit_of_meas_name FROM epsg_unitofmeasure WHERE uom_code = %s', (target_uom_code,))
  for uom_code,unit_of_meas_name in cur.fetchall():
    target_uom = uom_code, unit_of_meas_name
  
  #parameters = json.dumps({"factor_b": factor_b, "factor_c":factor_c, "change_id":change_id})
  
  doc = {
    'code': code + u"-units",
    'code_trans' : 0,
    'name': name,
    'alt_name' : alt_name,
    'area': u"",
    #'wkt': u"",
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
    'area_trans' : u"",
    'datum' : u"",
    'uom_code' : 0,
    'uom' : u"",
    'target_uom': target_uom,
    'kind': kind,
    # 'popularity': 0,
   # 'children_code' : 0,
    'data_source' : data_source,
    'primem' : u"",
    'greenwich_longitude' : u"",
    'concatop' : u"",
    'method' : u"",
    'files': u"",
    'reverse' : 0,
    'orientation' : u"",
    'abbreviation' : u"",
    'order' : u"",
    'description': u"",
    'primary' : 0,
    #'tgrams':name.lower(),
  }
  with ix.writer(procs=4, limitmb=1048, multisegment=True) as writer:
    writer.add_document(**doc)
#   writer.add_document(**doc )
# writer.close()

###############################################################################
print " - INSERT NEW EPSG CODES FROM EXTRA FILES(ESRI,OTHER)"
###############################################################################
#writer = BufferedWriter(ix, period=0, limit = 100)
ref = osr.SpatialReference()
FILES = ["extra_codes_proj4_4.8.0.2/esri.extra", "extra_codes_proj4_4.8.0.2/other.extra"]

for extra_file in FILES:
  f = open(extra_file)
  for line in f:
    #alt_description = u""
    #wkt = u""
    #a = None
    #description = u""
    code = u""
    kind = u""
    inf_source = u""
    if line[0] == "#":
      sharp,name = line.split(" ",1)
      name = name.strip()
      continue

    if line[0] == "<":
      code, proj = line.split(" ",1)
      code = code.replace("<","").replace(">","").strip()
      proj = proj.replace("<>","").strip()

    boost = 0
    ref.ImportFromEPSG(int(code))
    if ref.GetAttrValue("PROJCS"):
      kind = u"CRS-PROJCRS"
      boost = 0.2
      
    elif ref.GetAttrValue("GEOGCS"):
      kind = u"CRS-GEOGCRS"
      boost = 0.05
    
    importance = 0
    try:
      importance = crs_ex_line[code][1]
      if importance == u"":
        importance = 0
    except:
      pass
    
    score = float((1 + boost) * (1 + float(importance)))
    name = name.decode('utf-8')
    inf_source = "other"
    
    if extra_file == FILES[0]:
      name = u"ESRI: " + name
      inf_source = "ESRI"
      
    code = str(code).decode('utf-8')
    proj = str(proj).decode('utf-8')
     
    doc = {
       'code': code,
       'code_id':code,
       'code_trans' : 0,
       'name': name,
       'alt_name' : u"",
       'kind': kind,
       'area': u"",
       'area_code': u"",
       'deprecated': 0,
       # 'popularity': popularity,
       'trans' : u"",
       'trans_alt_name' : u"",
       'trans_remarks': u"",
       'area_trans' : u"",
       'accuracy' : u"",
       #'wkt': wkt,
       'bbox': u"",
       'scope': u"",
       'remarks': u"",
       'information_source': inf_source,
       'revision_date': 0,
       'datum' : u"",
       'geogcrs': u"",
      # 'children_code' : u"",
       'data_source' : u"PROJ4 4.8.0.2",
       'uom_code' : u"",
       'uom' : u"",
       'target_uom': u"",
       'primem' : u"",
       'greenwich_longitude' : 0,
       'concatop' : u"",
       'method' : u"",
       'files' : u"",
       'reverse' : 0,
       'orientation' : u"",
       'abbreviation' : u"",
       'order' : u"",
       'description': proj,
       'primary' : 0,
       #'tgrams':name.lower(),
       'ellipsoid' : u"",
       'cs': u"",
       'alt_description': u"",
       '_boost' : score
         
       
    }
    with ix.writer(procs=4, limitmb=1048, multisegment=True) as writer:
      writer.add_document(**doc) 
#     writer.add_document(**doc )
# writer.close()  