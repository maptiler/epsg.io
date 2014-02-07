#!/usr/bin/env python
# -*- coding: utf-8 -*-

DATABASE = 'gml.sqlite'
#XML = 'test_sample.xml'
XML = 'GmlDictionary.xml'

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
cur.execute('CREATE TABLE IF NOT EXISTS gml (urn VARCHAR, id VARCHAR, xml VARCHAR, PRIMARY KEY (urn))')
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
  cur.execute('INSERT INTO gml VALUES (?,?,?)', (urn,id,buffer(xml)))
  con.commit()