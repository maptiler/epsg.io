#!/usr/bin/python3 
# -*- coding: utf-8 -*-

DATABASE = 'gml.sqlite'
XML = 'test_sample.xml'
#XML = 'GmlDictionary.xml'
"""ids types in sqlite

ogp-uom-1043
epsg-uom-9001
ogp-method-9834
epsg-method-9835
epsg-meridian-8901
ogp-ellipsoid-7049
epsg-ellipsoid-7050
epsg-datum-9314
ogp-datum-9315
epsg-cs-6512
epsg-axis-211
ogp-cs-4493
ogp-axis-30
epsg-crs-7413
ogp-crs-7414
epsg-op-8635
ogp-op-8636
epsg-area-1024
ogp-cr-2014.001
"""
""" urn types in sqlite
urn:ogc:def:change-request:EPSG::2014.001
urn:ogc:def:version-history:EPSG::8.3.2
urn:ogc:def:uom:EPSG::9101
urn:ogc:def:method:EPSG::9629
urn:ogc:def:meridian:EPSG::8910
urn:ogc:def:ellipsoid:EPSG::7021
urn:ogc:def:parameter:EPSG::8641
urn:ogc:def:datum:EPSG::6600
urn:ogc:def:cs:EPSG::4491
urn:ogc:def:axis:EPSG::34
urn:ogc:def:crs:EPSG::6329
urn:ogc:def:coordinateOperation:EPSG::5984
urn:ogc:def:area:EPSG::3760

"""


import sys
import sqlite3 as sqlite
import xml.etree.ElementTree as et

###############################################################################
print "INITIALIZE OUTPUT"
###############################################################################

con = sqlite.connect(DATABASE)
if not con:
  print "Connection to sqlite FAILED"
  sys.exit(1)
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS gml (urn VARCHAR, id VARCHAR, xml VARCHAR, deprecated BOOLEAN, name VARCHAR, PRIMARY KEY (urn))')
cur.execute('DELETE FROM gml')

###############################################################################
print "PARSING"
###############################################################################
print "start parsing"
tree = et.parse(XML)
root = tree.getroot()
et.register_namespace("gml", 'http://www.opengis.net/gml/3.2')
et.register_namespace("epsg", 'urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset')
et.register_namespace("xlink", 'http://www.w3.org/1999/xlink')
et.register_namespace("rim", 'urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0')
et.register_namespace("gmd", 'http://www.isotc211.org/2005/gmd')
et.register_namespace("gco", 'http://www.isotc211.org/2005/gco')
print "stop parsing"

#for entry in root.findall('.//TRANSFORMATION[@{http://www.opengis.net/gml/3.2}id]'):

for entry in root.findall('.//*[@{http://www.opengis.net/gml/3.2}id]'):
  id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
  urn =  entry.find('{http://www.opengis.net/gml/3.2}identifier').text
  xml = et.tostring(entry, encoding="utf-8",method="xml")
  deprecated = None
  if entry.find(".//*[{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated]") != None:
    deprecated = entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated').text
  name = None
  if entry.find('.//*{http://www.opengis.net/gml/3.2}name') != None:
    name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
  elif entry.find('{http://www.opengis.net/gml/3.2}name') != None:
    name = entry.find('{http://www.opengis.net/gml/3.2}name').text
    

  cur.execute('INSERT INTO gml VALUES (?,?,?,?,?)', (urn, id, buffer(xml), deprecated, name))
  con.commit()