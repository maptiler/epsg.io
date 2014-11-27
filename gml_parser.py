#!/usr/bin/env python
# -*- coding: utf-8 -*-

DATABASE = 'gml.sqlite'
XML = 'GmlDictionary.xml'
INDEX = 'index'
CRS_EXCEPTIONS = 'CRS_exceptions.csv'
FILES = ["extra_codes_proj4_4.8.0.2/esri.extra",
         "extra_codes_proj4_4.8.0.2/other.extra"]

kind_list = {
    'vertical': "CRS-VERTCRS",
    'geocentric': "CRS-GCENCRS",
    'engineering': "CRS-ENGCRS",
    'geographic 3D': "CRS-GEOG3DCRS",
    'geographic 2D': "CRS-GEOGCRS",
    'compound': "CRS-COMPOUNDCRS",
    'projected': "CRS-PROJCRS",
    'transformation':  "COORDOP-COPTRANS",
    'concatenated operation': "COORDOP-COPCONOP",
    'conversion': "COORDOP-COPCON",
    'UNIT-angle': "UNIT-ANGUNIT",
    'UNIT-scale': "UNIT-SCALEUNIT",
    'UNIT-length': "UNIT-LENUNIT",
    'UNIT-time': "UNIT-TIMEUNIT",
    'DATUM-vertical': "DATUM-VERTDAT",
    'DATUM-engineering': "DATUM-ENGDAT",
    'DATUM-geodetic': "DATUM-GEODDAT",
    'ELLIPSOID': "ELLIPSOID",
    'PRIMEM': "PRIMEM",
    'METHOD': "METHOD",
    'CS': "CS",
    'CS-vertical': "CS-VERTCS",
    'CS-spherical': "CS-SPHERCS",
    'CS-Cartesian': "CS-CARTESCS",
    'CS-ellipsoidal': "CS-ELLIPCS",
    'AXIS': "AXIS",
    'AREA': "AREA"
}
dict_index = {
    'code': u"",
    'code_trans': 0,
    'name': u"",
    'alt_name': u"",
    'kind': u"",
    'area': u"",
    'area_trans': u"",
    'deprecated': 0,
    'trans': 0,
    'trans_alt_name': u"",
    'trans_remarks': u"",
    'accuracy': u"",
    'bbox': u"",
    'scope': u"",
    'remarks': u"",
    'information_source': u"",
    'revision_date': u"",
    'datum': u"",
    'geogcrs': u"",
    'target_crs': u"",
    'data_source': u"OGP",
    'uom': u"",
    'target_uom': u"",
    'primem': u"",
    'greenwich_longitude': 0,
    'concatop': [],
    'method': u"",
    'files': u"",
    'reverse': 0,
    'orientation': u"",
    'abbreviation': u"",
    'order': u"",
    'description': u"",
    'primary': 0,
    'uom_code': 0,
    'area_code': 0,
    'area_trans_code': 0,
    'alt_title': u"",
    'code_id': u"",
    'alt_description': u"",
    'ellipsoid': u"",
    'cs': u"",
    'axis': u""
}

dict_ellipsoid = {}
dict_area = {}
dict_datum = {}
dict_meridian = {}
dict_cs = {}
dict_axisname = {}
dict_uom = {}
dict_crs = {}
dict_op = {}
dict_method = {}
dict_concatenated_op = {}
dict_axis = {}
dict_axis_in_cs = {}
list_crs_op = []

import os
import sys
import xml.etree.ElementTree as et
import pprint
import time
import copy
from osgeo import osr
import sqlite3
import whoosh.fields
import whoosh.index
import csv


###############################################################################
print "INITIALIZE OUTPUT"
###############################################################################

con = sqlite3.connect(DATABASE)
if not con:
    print "Connection to sqlite FAILED"
cur = con.cursor()
cur.execute(
    'CREATE TABLE IF NOT EXISTS gml (urn VARCHAR, id VARCHAR, xml VARCHAR, deprecated BOOLEAN, name VARCHAR, PRIMARY KEY (urn))')
cur.execute('DELETE FROM gml')
###############################################################################
print "INITIALIZE INPUT"
###############################################################################
print " - CRS_EXCEPTIONS"
crs_ex_line = {}
try:
    with open(CRS_EXCEPTIONS) as crs_ex:
        text = csv.reader(crs_ex, delimiter=',')
        # skip the header
        next(text, None)
        for row in text:
            crs_ex_line[row[0]] = row
            # print crs_ex_line['4326'][2]
            # print crs_ex_line
except:
    print "!!! FAILED: NO CRS_EXCEPTIONS !!!"

print " - WHOOSH!"


class EPSGSchema(whoosh.fields.SchemaClass):

    # "4326", "1024-datum"
    code = whoosh.fields.TEXT(stored=True, field_boost=5.0)
    code_trans = whoosh.fields.NUMERIC(stored=True)
    # Name "WGS 84" 
    name = whoosh.fields.TEXT(stored=True, field_boost=3.0)
    alt_name = whoosh.fields.TEXT(stored=True)
    # "ProjectedCRS" | "GeodeticCRS" 
    kind = whoosh.fields.TEXT(stored=True, sortable=True)
    area = whoosh.fields.TEXT(stored=True)  # epsg_area/area_of_use
    area_trans = whoosh.fields.TEXT(stored=True)
    # "0 = Valid", "1 - Invalid"
    deprecated = whoosh.fields.BOOLEAN(stored=True)

    trans = whoosh.fields.NUMERIC(stored=True)
    trans_alt_name = whoosh.fields.TEXT(stored=True)
    trans_remarks = whoosh.fields.STORED
    accuracy = whoosh.fields.STORED

    # [area_north_bound_lat,area_west_bound_lon,area_south_bound_lat,area_east_bound_lon]
    bbox = whoosh.fields.STORED

    scope = whoosh.fields.STORED
    remarks = whoosh.fields.STORED
    information_source = whoosh.fields.STORED
    revision_date = whoosh.fields.STORED

    # Advanced with additional types such as "Elipsoid" | "Area" | ...
    datum = whoosh.fields.TEXT(stored=True)
    geogcrs = whoosh.fields.TEXT(stored=True)
    target_crs = whoosh.fields.STORED
    data_source = whoosh.fields.STORED
    uom = whoosh.fields.STORED
    target_uom = whoosh.fields.STORED
    primem = whoosh.fields.TEXT(stored=True)
    greenwich_longitude = whoosh.fields.STORED
    concatop = whoosh.fields.STORED
    method = whoosh.fields.TEXT(stored=True)
    files = whoosh.fields.STORED
    reverse = whoosh.fields.STORED
    orientation = whoosh.fields.STORED
    abbreviation = whoosh.fields.STORED
    order = whoosh.fields.STORED
    description = whoosh.fields.STORED
    primary = whoosh.fields.STORED
    uom_code = whoosh.fields.STORED
    area_code = whoosh.fields.NUMERIC(stored=True)
    area_trans_code = whoosh.fields.NUMERIC(stored=True)

    # CRS_exceptions
    alt_title = whoosh.fields.TEXT(stored=True, field_boost=3.0)
    code_id = whoosh.fields.ID(stored=True, unique=True)
    alt_code = whoosh.fields.NUMERIC(stored=True)
    alt_description = whoosh.fields.TEXT(stored=True)
    ellipsoid = whoosh.fields.TEXT(stored=True)
    cs = whoosh.fields.TEXT(stored=True)
    axis = whoosh.fields.STORED

# MAKE DIRECTORY AND CREATE INDEX
if not os.path.exists(INDEX):
    os.mkdir(INDEX)
# Create whoosh's index with EPSGSchema
ix = whoosh.index.create_in(INDEX, EPSGSchema)

###############################################################################
print "PARSING"
start_parse = time.clock()
###############################################################################
print "start parsing"
parser = et.XMLParser(encoding='UTF-8')
tree = et.parse(XML,parser)
root = tree.getroot()
et.register_namespace("gml", 'http://www.opengis.net/gml/3.2')
et.register_namespace("epsg", 'urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset')
et.register_namespace("xlink", 'http://www.w3.org/1999/xlink')
et.register_namespace("rim", 'urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0')
et.register_namespace("gmd", 'http://www.isotc211.org/2005/gmd')
et.register_namespace("gco", 'http://www.isotc211.org/2005/gco')
print "stop parsing"
print (time.clock() - start_parse), "s : parse time"

start = time.clock()

dict = []

# First cycle - It's necessary have additional information in dictionaries.
# It's much faster, then searching through whole document for one information,
# from another record.
# This first cycle take approximately (depends on processor clock) 5 second.
# On the other hand, it's not necessary have saved information in dict,
# if it possible to take directly from gml. 

time_saving_dict = time.clock()

for entry in root.findall('.//*[@{http://www.opengis.net/gml/3.2}id]'):
    if "-ellipsoid-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        id = (entry.attrib['{http://www.opengis.net/gml/3.2}id'])
        code = id.split('-')[2]

        name = None
        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text

        dict_ellipsoid[int(code)] = name

    if "-area-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        code = entry.attrib['{http://www.opengis.net/gml/3.2}id'].split('-')[2]

        area_of_use = (entry.find(
            './/*{http://www.isotc211.org/2005/gco}CharacterString').text)
        west = 0
        east = 0
        south = 0
        north = 0
        for bounds in entry.findall('.//*{http://www.isotc211.org/2005/gmd}EX_GeographicBoundingBox'):
            west = bounds.find(
                "{http://www.isotc211.org/2005/gmd}westBoundLongitude/{http://www.isotc211.org/2005/gco}Decimal").text
            east = bounds.find(
                "{http://www.isotc211.org/2005/gmd}eastBoundLongitude/{http://www.isotc211.org/2005/gco}Decimal").text
            south = bounds.find(
                "{http://www.isotc211.org/2005/gmd}southBoundLatitude/{http://www.isotc211.org/2005/gco}Decimal").text
            north = bounds.find(
                "{http://www.isotc211.org/2005/gmd}northBoundLatitude/{http://www.isotc211.org/2005/gco}Decimal").text

        dict_area[int(code)] = [
            area_of_use, (float(north), float(west), float(south), float(east))]

    if "-datum-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        code = entry.attrib['{http://www.opengis.net/gml/3.2}id'].split('-')[2]
        name = None
        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text
        ellipsoid = 0
        if entry.find('{http://www.opengis.net/gml/3.2}ellipsoid') is not None:
            ellipsoid = entry.find(
                '{http://www.opengis.net/gml/3.2}ellipsoid').get('{http://www.w3.org/1999/xlink}href')
            ellipsoid = ellipsoid.split("::")[1]

        if entry.find('{http://www.opengis.net/gml/3.2}primeMeridian') is not None:
            meridian = entry.find(
                '{http://www.opengis.net/gml/3.2}primeMeridian').get('{http://www.w3.org/1999/xlink}href')
            meridian = meridian.split("::")[1]

        dict_datum[int(code)] = [name, int(ellipsoid), int(meridian)]

    if "-meridian-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        code = entry.attrib['{http://www.opengis.net/gml/3.2}id'].split('-')[2]
        name = None
        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text

        greenwich = ""
        if entry.find('{http://www.opengis.net/gml/3.2}greenwichLongitude') is not None:
            greenwich = entry.find(
                '{http://www.opengis.net/gml/3.2}greenwichLongitude').text
            if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}hemisphere') is not None:
                sign = entry.find(
                    './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}hemisphere').text
                if sign == "W":
                    greenwich = float(greenwich) * -1

        dict_meridian[int(code)] = [name, greenwich]

    if "-cs-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        code = entry.attrib['{http://www.opengis.net/gml/3.2}id'].split('-')[2]
        name = None
        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text
        axis_list = []

        for coordaxis in entry.findall('.//*{http://www.opengis.net/gml/3.2}CoordinateSystemAxis'):
            axis = coordaxis.attrib[
                '{http://www.opengis.net/gml/3.2}id'].split('-')[2]
            axis_name_code = coordaxis.find(
                '{http://www.opengis.net/gml/3.2}descriptionReference').get('{http://www.w3.org/1999/xlink}href')
            axis_name_code = axis_name_code.split("::")[1]
            uom = coordaxis.attrib['uom'].split('::')[1]

            axis_list.append([int(axis), int(axis_name_code)])
            dict_axis[int(axis)] = int(axis_name_code)
            dict_axis_in_cs[int(axis)] = int(code)
        dict_cs[int(code)] = [name, axis_list, uom]

    if "-axisname-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        code = id.split('-')[2]
        name = None

        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text

        information_source = ""
        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource') is not None:
            information_source = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource').text

        rev_date = ""
        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}revisionDate') is not None:
            rev_date = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}revisionDate').text

        remarks = ""
        if entry.find('{http://www.opengis.net/gml/3.2}remarks') is not None:
            remarks = entry.find(
                '{http://www.opengis.net/gml/3.2}remarks').text

        deprecated = 0
        if entry.find(".//*[{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated]") is not None:
            deprecated = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated').text
        if deprecated == 'true':
            deprecated = 1
        elif deprecated == 'false':
            deprecated = 0

        description = ""
        if entry.find('{http://www.opengis.net/gml/3.2}description') is not None:
            description = entry.find(
                '{http://www.opengis.net/gml/3.2}description').text

        dict_axisname[int(code)] = [
            name, information_source, rev_date, deprecated, description, remarks]

    if "-uom-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        code = id.split('-')[2]
        name = ""
        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text

        dict_uom[int(code)] = name

    if "-crs-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        code = id.split('-')[2]
        name = ""
        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text

        geod_datum = ""
        if entry.find('{http://www.opengis.net/gml/3.2}geodeticDatum') is not None:
            geod_datum = entry.find(
                '{http://www.opengis.net/gml/3.2}geodeticDatum').get('{http://www.w3.org/1999/xlink}href')
        elif entry.find('{http://www.opengis.net/gml/3.2}verticalDatum') is not None:
            geod_datum = entry.find(
                '{http://www.opengis.net/gml/3.2}verticalDatum').get('{http://www.w3.org/1999/xlink}href')
        elif entry.find('{http://www.opengis.net/gml/3.2}engineeringDatum') is not None:
            geod_datum = entry.find(
                '{http://www.opengis.net/gml/3.2}engineeringDatum').get('{http://www.w3.org/1999/xlink}href')

        geogcrs = ""
        same_geogcrs_as_code = False
        if entry.find('{http://www.opengis.net/gml/3.2}baseGeodeticCRS') is not None:
            geogcrs = entry.find(
                '{http://www.opengis.net/gml/3.2}baseGeodeticCRS').get('{http://www.w3.org/1999/xlink}href')
        else:
            if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}sourceGeographicCRS') is not None:
                geogcrs = entry.find(
                    './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}sourceGeographicCRS').get('{http://www.w3.org/1999/xlink}href')
            else:
                if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}type').text == 'compound':
                    geogcrs = ""
                else:
                    geogcrs = code
                    same_geogcrs_as_code = True

        if geod_datum != "":
            geod_datum = int(geod_datum.split("::")[1])
        if geogcrs != "" and not same_geogcrs_as_code:
            geogcrs = int(geogcrs.split("::")[1])

        dict_crs[int(code)] = [name, geod_datum, geogcrs]

    if "-op-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:

        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        code = id.split('-')[2]
        sourceCRS = 0
        if entry.find('{http://www.opengis.net/gml/3.2}sourceCRS') is not None:
            sourceCRS = entry.find(
                '{http://www.opengis.net/gml/3.2}sourceCRS').get('{http://www.w3.org/1999/xlink}href')
            sourceCRS = sourceCRS.split("::")[1]

        parametr_list = []
        parametr = 0
        for params in entry.findall('{http://www.opengis.net/gml/3.2}parameterValue'):
            if params.find(".//*{http://www.opengis.net/gml/3.2}value") is not None:
                parametr = params.find(
                    ".//*{http://www.opengis.net/gml/3.2}value").text

            parametr_list.append(float(parametr))

        if len(parametr_list) == 7:
            v = parametr_list
        elif len(parametr_list) == 3:
            v = parametr_list + [0.0] * 4
        else:
            v = [0]
            parameters = u"0"
        if v == [0] and entry.find('.//*{http://www.opengis.net/gml/3.2}valueFile') is not None:
            parameters = entry.find('.//*{http://www.opengis.net/gml/3.2}valueFile').text
        else:
            parameters = tuple(v)

        area = ""
        if entry.find('{http://www.opengis.net/gml/3.2}domainOfValidity') is not None:
            area = entry.find(
                '{http://www.opengis.net/gml/3.2}domainOfValidity').get('{http://www.w3.org/1999/xlink}href')
            area = area.split("::")[1]

        accuracy = u"unknown"
        if entry.find(".//*{http://www.isotc211.org/2005/gco}Decimal") is not None:
            accuracy = float(entry.find(
                ".//*{http://www.isotc211.org/2005/gco}Decimal").text)

        method_code = ""
        if entry.find('{http://www.opengis.net/gml/3.2}method') is not None:
            method_code = entry.find(
                '{http://www.opengis.net/gml/3.2}method').get('{http://www.w3.org/1999/xlink}href')
            method_code = method_code.split("::")[1]

        dict_op[int(code)] = [
            int(sourceCRS), parameters, area, accuracy, method_code]

        if "concatenated operation" in entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}type').text:
            con_op_list = []
            for concatenated in entry.findall('{http://www.opengis.net/gml/3.2}coordOperation'):
                con_operations = concatenated.get(
                    '{http://www.w3.org/1999/xlink}href')
                if con_operations != "":
                    con_operations = con_operations.split("::")[1]
                    con_op_list.append(int(con_operations))
            dict_concatenated_op[int(code)] = con_op_list

        if "conversion" not in entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}type').text:

            if "urn:ogc:def:crs:EPSG::4326" in entry.find('{http://www.opengis.net/gml/3.2}targetCRS').get('{http://www.w3.org/1999/xlink}href'):
                crs_op = sourceCRS, code
                list_crs_op.append(tuple(crs_op))

    if "-method-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        code = entry.attrib['{http://www.opengis.net/gml/3.2}id'].split('-')[2]
        name = None
        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text

        dict_method[int(code)] = name

print time.clock() - time_saving_dict, "saving dictionaries"
# pprint.pprint(dict_crs)

# Second cycle
# This cycle saved every record into specific document in whoosh index
# and for every record is saved addition information into sqlite database.

ref = osr.SpatialReference()
# ///////////////////////////////////////////////////////
# find in whole document area
# ///////////////////////////////////////////////////////
for entry in root.findall('.//*[@{http://www.opengis.net/gml/3.2}id]'):
    doc = copy.deepcopy(dict_index)
    if "-area-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        doc = copy.deepcopy(dict_index)
        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        code = id.split('-')[2]
        doc['code'] = (code + u"-area").decode('utf-8')
        doc['area_code'] = int(code)
        doc['kind'] = u"AREA"
        doc['area'] = dict_area[int(code)][0].encode('UTF-8').decode('UTF-8')
        doc['bbox'] = dict_area[int(code)][1]

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias') is not None:
            doc['alt_name'] = (entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias').get('alias')).encode('UTF-8').decode('UTF-8')

        if entry.find('{http://www.opengis.net/gml/3.2}remarks') is not None:
            doc['remarks'] = (entry.find(
                '{http://www.opengis.net/gml/3.2}remarks').text).encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource') is not None:
            doc['information_source'] = (entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource').text).encode('UTF-8').decode('UTF-8')

        doc['revision_date'] = (entry.find(
            './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}revisionDate').text).decode('utf-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}geometryFile') is not None:
            doc['files'] = (entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}geometryFile').get('{http://www.w3.org/1999/xlink}href')).decode('utf-8')

        if entry.find(".//*[{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated]") is not None:
            deprecated = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated').text
            if deprecated == 'true':
                doc['deprecated'] = 1
            elif deprecated == 'false':
                doc['deprecated'] = 0

        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = (entry.find('.//*{http://www.opengis.net/gml/3.2}name').text).encode('utf-8')
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = (entry.find('{http://www.opengis.net/gml/3.2}name').text).encode('utf-8')
        doc['name'] = name.decode('utf-8')

        # Save information into sqlite database
        xml = et.tostring(entry, encoding="utf-8", method="xml")
        urn = entry.find('{http://www.opengis.net/gml/3.2}identifier').text
        cur.execute('INSERT INTO gml VALUES (?,?,?,?,?)',
                    (urn.decode('utf-8'), id.decode('utf-8'), buffer(xml), deprecated.decode('utf-8'), name.decode('utf-8')))
        con.commit()

        # Write into Whoosh index
        with ix.writer(limitmb=1048, multisegment=True) as writer:
            writer.add_document(**doc)


# ///////////////////////////////////////////////////////
# find in whole document coordinate systems with axis
# ///////////////////////////////////////////////////////
    if "-cs-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        doc = copy.deepcopy(dict_index)
        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        code = id.split('-')[2]
        doc['code'] = code + u"-cs"

        if entry.find('{http://www.opengis.net/gml/3.2}remarks') is not None:
            doc['remarks'] = entry.find('{http://www.opengis.net/gml/3.2}remarks').text

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource') is not None:
            doc['information_source'] = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource').text

        doc['revision_date'] = entry.find(
            './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}revisionDate').text

        doc['kind'] = kind_list[
            "CS-" + entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}type').text].decode('utf-8')

        if entry.find(".//*[{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated]") is not None:
            deprecated = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated').text
            if deprecated == 'true':
                doc['deprecated'] = 1
            elif deprecated == 'false':
                doc['deprecated'] = 0

        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text
        doc['name'] = name.encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias') is not None:
            doc['alt_name'] = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias').get('alias')
        axis_list = []

        # in dict_cs is key "code cs" and values [name cs, [axis code, code of axis name]]
		# in dict_axisname is key "axis code" and value is axis name
        for axis_code in dict_cs[int(code)][1]:
            axis_name = dict_axisname[int(axis_code[1])][0]
            axis_list.append(
                {'axis_code': axis_code[0], 'axis_name': axis_name})
        doc['axis'] = axis_list

        urn = entry.find('{http://www.opengis.net/gml/3.2}identifier').text
        xml = et.tostring(entry, encoding="utf-8", method="xml")
        cur.execute('INSERT INTO gml VALUES (?,?,?,?,?)',
                    (urn, id, buffer(xml), deprecated, name))
        con.commit()

        # Write into Whoosh index
        with ix.writer(limitmb=1048, multisegment=True) as writer:
            writer.add_document(**doc)

# ///////////////////////////////////////////////////////
# find in whole document method
# ///////////////////////////////////////////////////////
    
    if "-method-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        doc = copy.deepcopy(dict_index)
        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        doc['code'] = (id.split('-')[2] + "-method").encode('UTF-8').decode('UTF-8')
        doc['kind'] = u"METHOD"
        
        if entry.find('{http://www.opengis.net/gml/3.2}remarks') is not None:
            doc['remarks'] = (entry.find('{http://www.opengis.net/gml/3.2}remarks').text).encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource') is not None:
            doc['information_source'] = (entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource').text).encode('UTF-8').decode('UTF-8')

        doc['revision_date'] = (entry.find(
            './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}revisionDate').text).encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isOperationReversible') is not None:
            doc['reverse'] = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isOperationReversible').text

        if entry.find(".//*[{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated]") is not None:
            deprecated = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated').text
            if deprecated == 'true':
                doc['deprecated'] = 1
            elif deprecated == 'false':
                doc['deprecated'] = 0

        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text
        doc['name'] = name.encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias') is not None:
            doc['alt_name'] = (entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias').get('alias')).encode('UTF-8').decode('UTF-8')

        urn = entry.find('{http://www.opengis.net/gml/3.2}identifier').text
        xml = et.tostring(entry, encoding="utf-8", method="xml")
        cur.execute('INSERT INTO gml VALUES (?,?,?,?,?)',
                    (urn.encode('UTF-8').decode('UTF-8'), id.encode('UTF-8').decode('UTF-8'), buffer(xml), deprecated.encode('UTF-8').decode('UTF-8'), name.encode('UTF-8').decode('UTF-8')))
        con.commit()
        # Write into Whoosh index
        with ix.writer(limitmb=1048, multisegment=True) as writer:
            writer.add_document(**doc)

# ///////////////////////////////////////////////////////
# find in whole document prime meridian
# ///////////////////////////////////////////////////////
    if "-meridian-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        doc = copy.deepcopy(dict_index)
        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        code = id.split('-')[2]
        doc['code'] = (code + "-primem").decode('UTF-8')

        doc['kind'] = u"PRIMEM"

        if entry.find('{http://www.opengis.net/gml/3.2}remarks') is not None:
            doc['remarks'] = (entry.find('{http://www.opengis.net/gml/3.2}remarks').text).encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource') is not None:
            doc['information_source'] = (entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource').text).encode('UTF-8').decode('UTF-8')

        doc['revision_date'] = entry.find(
            './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}revisionDate').text

        if entry.find(".//*[{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated]") is not None:
            deprecated = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated').text
            if deprecated == 'true':
                doc['deprecated'] = 1
            elif deprecated == 'false':
                doc['deprecated'] = 0

        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text
        doc['name'] = name.encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias') is not None:
            doc['alt_name'] = (entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias').get('alias')).encode('UTF-8').decode('UTF-8')
        
        if entry.find('{http://www.opengis.net/gml/3.2}greenwichLongitude') is not None:
            doc['greenwich_longitude'] = dict_meridian[int(code)][1]
        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}sexagesimalValue') is not None:
            uom = entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}sexagesimalValue').get('uom')
            uom_code = uom.split('::')[1]
            doc['uom'] = dict_uom[int(uom_code)].encode('UTF-8').decode('UTF-8')
            doc['uom_code'] = uom_code

        urn = entry.find('{http://www.opengis.net/gml/3.2}identifier').text
        xml = et.tostring(entry, encoding="utf-8", method="xml")
        cur.execute('INSERT INTO gml VALUES (?,?,?,?,?)',
                    (urn.encode('UTF-8').decode('UTF-8'), id.encode('UTF-8').decode('UTF-8'), buffer(xml), deprecated.encode('UTF-8').decode('UTF-8'), name.encode('UTF-8').decode('UTF-8')))
        con.commit()
        # Write into Whoosh index
        with ix.writer(limitmb=1048, multisegment=True) as writer:
            writer.add_document(**doc)

			# ///////////////////////////////////////////////////////
# find in whole document ellipsoid
# ///////////////////////////////////////////////////////
    if "-ellipsoid-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        doc = copy.deepcopy(dict_index)
        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        doc['code'] = (id.split('-')[2] + "-ellipsoid").encode('UTF-8').decode('UTF-8')
        doc['kind'] = u"ELLIPSOID"

        if entry.find('{http://www.opengis.net/gml/3.2}remarks') is not None:
            doc['remarks'] = (entry.find('{http://www.opengis.net/gml/3.2}remarks').text).encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource') is not None:
            doc['information_source'] = (entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource').text).encode('UTF-8').decode('UTF-8')

        doc['revision_date'] = (entry.find(
            './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}revisionDate').text).encode('UTF-8').decode('UTF-8')

        if entry.find(".//*[{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated]") is not None:
            deprecated = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated').text
            if deprecated == 'true':
                doc['deprecated'] = 1
            elif deprecated == 'false':
                doc['deprecated'] = 0

        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text
        doc['name'] = name.encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias') is not None:
            doc['alt_name'] = (entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias').get('alias')).encode('UTF-8').decode('UTF-8')

        if entry.find('{http://www.opengis.net/gml/3.2}semiMajorAxis') is not None:
            uom_code = entry.find(
                '{http://www.opengis.net/gml/3.2}semiMajorAxis').get('uom')
            doc['uom_code'] = int(uom_code.split("::")[1])
            doc['uom'] = dict_uom[doc['uom_code']].encode('UTF-8').decode('UTF-8')

        urn = entry.find('{http://www.opengis.net/gml/3.2}identifier').text
        xml = et.tostring(entry, encoding="utf-8", method="xml")
        cur.execute('INSERT INTO gml VALUES (?,?,?,?,?)',
                    (urn.encode('UTF-8').decode('UTF-8'), id.encode('UTF-8').decode('UTF-8'), buffer(xml), deprecated.encode('UTF-8').decode('UTF-8'), name.encode('UTF-8').decode('UTF-8')))
        con.commit()
        # Write into Whoosh index
        with ix.writer(limitmb=1048, multisegment=True) as writer:
            writer.add_document(**doc)

# ///////////////////////////////////////////////////////
# find in whole document axis
# ///////////////////////////////////////////////////////
    if "-axis-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        doc = copy.deepcopy(dict_index)
        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        code = id.split('-')[2]
        uom = entry.attrib['uom']
        doc['uom_code'] = int(uom.split("::")[1])
        doc['uom'] = dict_uom[doc['uom_code']].encode('UTF-8').decode('UTF-8')
        doc['code'] = (code + "-axis").encode('UTF-8').decode('UTF-8')
        doc['kind'] = u"AXIS"
        # dict_axisname[int(code)] = [name, information_source, rev_date, deprecated, description, remarks]

        doc['name'] = dict_axisname[dict_axis[int(code)]][0].encode('UTF-8').decode('UTF-8')

        if entry.find('{http://www.opengis.net/gml/3.2}axisAbbrev') is not None:
            doc['abbreviation'] = (entry.find(
                '{http://www.opengis.net/gml/3.2}axisAbbrev').text).encode('UTF-8').decode('UTF-8')

        if entry.find('{http://www.opengis.net/gml/3.2}axisDirection') is not None:
            doc['orientation'] = (entry.find(
                '{http://www.opengis.net/gml/3.2}axisDirection').text).encode('UTF-8').decode('UTF-8')
        
        # dict_axisname[int(code)] = [name, information_source, rev_date, deprecated, description, remarks]
        doc['remarks'] = dict_axisname[dict_axis[int(code)]][5].encode('UTF-8').decode('UTF-8')
        doc['description'] = dict_axisname[dict_axis[int(code)]][4].encode('UTF-8').decode('UTF-8')
        doc['deprecated'] = dict_axisname[dict_axis[int(code)]][3]
        doc['revision_date'] = dict_axisname[dict_axis[int(code)]][2].encode('UTF-8').decode('UTF-8')
        doc['information_source'] = dict_axisname[dict_axis[int(code)]][1].encode('UTF-8').decode('UTF-8')
        doc['cs'] = str(dict_axis_in_cs[int(code)]).encode('UTF-8').decode('UTF-8'), (dict_cs[dict_axis_in_cs[int(code)]][0]).encode('UTF-8').decode('UTF-8')

        if dict_cs[dict_axis_in_cs[int(code)]][1][0][0] == int(code):
            doc['order'] = u"1."
        if len(dict_cs[dict_axis_in_cs[int(code)]][1]) > 1:
            if dict_cs[dict_axis_in_cs[int(code)]][1][1][0] == int(code):
                doc['order'] = u"2."
        if len(dict_cs[dict_axis_in_cs[int(code)]][1]) > 2:
            if dict_cs[dict_axis_in_cs[int(code)]][1][2][0] == int(code):
                doc['order'] = u"3."

        if doc['deprecated'] == 1:
            deprecated = 'true'
        elif doc['deprecated'] == 0:
            deprecated = 'false'

        urn = entry.find('{http://www.opengis.net/gml/3.2}identifier').text
        xml = et.tostring(entry, encoding="utf-8", method="xml")
        cur.execute('INSERT INTO gml VALUES (?,?,?,?,?)',
                    (urn.encode('UTF-8').decode('UTF-8'), id.encode('UTF-8').decode('UTF-8'), buffer(xml), deprecated.encode('UTF-8').decode('UTF-8'), doc['name']))
        con.commit()
        # Write into Whoosh index
        with ix.writer(limitmb=1048, multisegment=True) as writer:
            writer.add_document(**doc)

# ///////////////////////////////////////////////////////
# find in whole document datums
# ///////////////////////////////////////////////////////
    if "-datum-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        doc = copy.deepcopy(dict_index)
        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        doc['code'] = (id.split('-')[2] + "-datum").encode('UTF-8').decode('UTF-8')

        doc['kind'] = kind_list[
            "DATUM-" + entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}type').text].decode('utf-8')

        if entry.find('{http://www.opengis.net/gml/3.2}remarks') is not None:
            if entry.find('{http://www.opengis.net/gml/3.2}remarks').text is not None:
                doc['remarks'] = (entry.find('{http://www.opengis.net/gml/3.2}remarks').text)

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource') is not None:
            doc['information_source'] = (entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource').text).encode('UTF-8').decode('UTF-8')

        doc['revision_date'] = (entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}revisionDate').text).encode('UTF-8').decode('UTF-8')

        if entry.find(".//*[{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated]") is not None:
            deprecated = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated').text
            if deprecated == 'true':
                doc['deprecated'] = 1
            elif deprecated == 'false':
                doc['deprecated'] = 0

        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text
        doc['name'] = name.encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias') is not None:
            doc['alt_name'] = (entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias').get('alias')).encode('UTF-8').decode('UTF-8')

        if entry.find('{http://www.opengis.net/gml/3.2}primeMeridian') is not None:
            primem = entry.find(
                '{http://www.opengis.net/gml/3.2}primeMeridian').get('{http://www.w3.org/1999/xlink}href')
            primem = primem.split("::")[1]
            doc['primem'] = str(primem).encode('UTF-8').decode('UTF-8'), str(dict_meridian[int(primem)][0]).encode('UTF-8').decode('UTF-8')
            doc['greenwich_longitude'] = dict_meridian[int(primem)][1]

        if entry.find('{http://www.opengis.net/gml/3.2}ellipsoid') is not None:
            ellipsoid = entry.find(
                '{http://www.opengis.net/gml/3.2}ellipsoid').get('{http://www.w3.org/1999/xlink}href')
            ellipsoid = ellipsoid.split("::")[1]
            doc['ellipsoid'] = str(ellipsoid).encode('UTF-8').decode('UTF-8'), str(dict_ellipsoid[int(ellipsoid)]).encode('UTF-8').decode('UTF-8')

        if entry.find('{http://www.opengis.net/gml/3.2}domainOfValidity') is not None:
            area = entry.find(
                '{http://www.opengis.net/gml/3.2}domainOfValidity').get('{http://www.w3.org/1999/xlink}href')
            area = area.split("::")[1]
            doc['bbox'] = dict_area[int(area)][1]
            doc['area'] = (dict_area[int(area)][0]).encode('UTF-8').decode('UTF-8')
            doc['area_code'] = int(area)

        if entry.find('{http://www.opengis.net/gml/3.2}scope') is not None:
            doc['scope'] = entry.find(
                '{http://www.opengis.net/gml/3.2}scope').text

        urn = entry.find('{http://www.opengis.net/gml/3.2}identifier').text
        xml = et.tostring(entry, encoding="utf-8", method="xml")
        cur.execute('INSERT INTO gml VALUES (?,?,?,?,?)',
                    (urn.encode('UTF-8').decode('UTF-8'), id.encode('UTF-8').decode('UTF-8'), buffer(xml), deprecated.encode('UTF-8').decode('UTF-8'), name.encode('UTF-8').decode('UTF-8')))
        con.commit()
        # Write into Whoosh index
        with ix.writer(limitmb=1048, multisegment=True) as writer:
            writer.add_document(**doc)

# ///////////////////////////////////////////////////////
# find in whole document units of measure
# ///////////////////////////////////////////////////////
    if "-uom-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        doc = copy.deepcopy(dict_index)
        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        doc['code'] = (id.split('-')[2] + "-units").encode('UTF-8').decode('UTF-8')
        doc['kind'] = kind_list[
            "UNIT-" + entry.find('{http://www.opengis.net/gml/3.2}quantityType').text].decode('utf-8')
        
        if entry.find('{http://www.opengis.net/gml/3.2}remarks') is not None:
            doc['remarks'] = (entry.find('{http://www.opengis.net/gml/3.2}remarks').text).encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource') is not None:
            doc['information_source'] = (entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource').text).encode('UTF-8').decode('UTF-8')

        doc['revision_date'] = entry.find(
            './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}revisionDate').text

        if entry.find(".//*[{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated]") is not None:
            deprecated = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated').text
            if deprecated == 'true':
                doc['deprecated'] = 1
            elif deprecated == 'false':
                doc['deprecated'] = 0

        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text
        doc['name'] = name.encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias') is not None:
            doc['alt_name'] = (entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias').get('alias')).encode('UTF-8').decode('UTF-8')

        if entry.find('{http://www.opengis.net/gml/3.2}conversionToPreferredUnit') is not None:
            target = entry.find(
                '{http://www.opengis.net/gml/3.2}conversionToPreferredUnit').get('uom')
            target = target.split("::")[1]
            doc['target_uom'] = target, (dict_uom[int(target)]).encode('UTF-8').decode('UTF-8')

        urn = entry.find('{http://www.opengis.net/gml/3.2}identifier').text
        xml = et.tostring(entry, encoding="utf-8", method="xml")
        cur.execute('INSERT INTO gml VALUES (?,?,?,?,?)',
                    (urn.encode('UTF-8').decode('UTF-8'), id.encode('UTF-8').decode('UTF-8'), buffer(xml), deprecated.encode('UTF-8').decode('UTF-8'), name.encode('UTF-8').decode('UTF-8')))
        con.commit()
        # Write into Whoosh index
        with ix.writer(limitmb=1048, multisegment=True) as writer:
            writer.add_document(**doc)

# ///////////////////////////////////////////////////////
# find in whole document operation
# ///////////////////////////////////////////////////////
    if "-op-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        doc = copy.deepcopy(dict_index)
        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        doc['code'] = id.split('-')[2].encode('UTF-8').decode('UTF-8')
        type = entry.find(
            './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}type').text
        doc['kind'] = kind_list[type].decode('utf-8')

        doc['description'] = str(dict_op[int(doc['code'])][1]).decode('UTF-8')

        if type == "concatenated operation":
            doc['concatop'] = dict_concatenated_op[int(doc['code'])]

        if entry.find('{http://www.opengis.net/gml/3.2}remarks') is not None:
            doc['remarks'] = (entry.find(
                '{http://www.opengis.net/gml/3.2}remarks').text).encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource') is not None:
            doc['information_source'] = (entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource').text).encode('UTF-8').decode('UTF-8')

        doc['revision_date'] = (entry.find(
            './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}revisionDate').text)

        if entry.find(".//*[{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated]") is not None:
            deprecated = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated').text
            if deprecated == 'true':
                doc['deprecated'] = 1
            elif deprecated == 'false':
                doc['deprecated'] = 0

        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text
        doc['name'] = name.encode('UTF-8').decode('UTF-8')

        if entry.find('{http://www.opengis.net/gml/3.2}domainOfValidity') is not None:
            area = entry.find(
                '{http://www.opengis.net/gml/3.2}domainOfValidity').get('{http://www.w3.org/1999/xlink}href')
            area = area.split("::")[1]
            doc['bbox'] = dict_area[int(area)][1]
            doc['area'] = dict_area[int(area)][0].encode('UTF-8').decode('UTF-8')
            doc['area_code'] = int(area)

        if entry.find('{http://www.opengis.net/gml/3.2}scope') is not None:
            doc['scope'] = (entry.find(
                '{http://www.opengis.net/gml/3.2}scope').text).encode('UTF-8').decode('UTF-8')

        if entry.find(".//*{http://www.isotc211.org/2005/gco}Decimal") is not None:
            doc['accuracy'] = float(entry.find(
                ".//*{http://www.isotc211.org/2005/gco}Decimal").text)

        sourceCRS = int(dict_op[int(doc['code'])][0])

        if sourceCRS != 0:
            # if not exist datum for current op, then try find datum in his sourceCRS
            isDatum = True
			# transformations in compound CRS do not have sourceCRS, even datum or ellipsoid
            if dict_crs[int(sourceCRS)][1] == '' and type != "compound":
                sourceCRS = dict_crs[int(sourceCRS)][2]
  
				# if op do not have datum, even his sourceCRS, then save first sourceCRS and no datum or ellipsoid
                if sourceCRS == "" or sourceCRS == 0:
                    sourceCRS = dict_op[int(doc['code'])][0]
                    doc['geogcrs'] = str(sourceCRS).encode('UTF-8').decode('UTF-8'), dict_crs[int(sourceCRS)][0].encode('UTF-8').decode('UTF-8')

                if dict_crs[int(sourceCRS)][1] == "":
                    isDatum = False

            if sourceCRS != "" and isDatum:
                doc['geogcrs'] = str(sourceCRS).encode('UTF-8').decode('UTF-8'), dict_crs[int(sourceCRS)][0].encode('UTF-8').decode('UTF-8')
                datum_code = dict_crs[int(sourceCRS)][1]
                datum_name = dict_datum[int(datum_code)][0]
                doc['datum'] = str(datum_code).encode('UTF-8').decode('UTF-8'), str(datum_name).encode('UTF-8').decode('UTF-8')

                primeMeridian_code = dict_datum[int(datum_code)][2]
                primeMeridian_name = dict_meridian[int(primeMeridian_code)][0]
                doc['primem'] = str(primeMeridian_code).encode('UTF-8').decode('UTF-8'), str(
                    primeMeridian_name).encode('UTF-8').decode('UTF-8')

                doc['greenwich_longitude'] = str(dict_meridian[
                    int(primeMeridian_code)][1]).encode('UTF-8').decode('UTF-8')

                ellipsoid_code = dict_datum[int(datum_code)][1]
                if ellipsoid_code != 0:  # engineering datum nema elipsoid
                    ellipsoid_name = dict_ellipsoid[int(ellipsoid_code)]
                    doc['ellipsoid'] = str(ellipsoid_code).encode('UTF-8').decode('UTF-8'), str(ellipsoid_name).encode('UTF-8').decode('UTF-8')

        if entry.find('{http://www.opengis.net/gml/3.2}targetCRS') is not None:
            targetCRS = entry.find(
                '{http://www.opengis.net/gml/3.2}targetCRS').get('{http://www.w3.org/1999/xlink}href')
            doc['target_crs'] = targetCRS.split("::")[1].encode('UTF-8').decode('UTF-8')

        if entry.find('{http://www.opengis.net/gml/3.2}method') is not None:
            method_code = entry.find(
                '{http://www.opengis.net/gml/3.2}method').get('{http://www.w3.org/1999/xlink}href')
            method_code = method_code.split("::")[1]
            doc['method'] = (str(method_code)).encode('UTF-8').decode('UTF-8'), dict_method[int(method_code)].encode('UTF-8').decode('UTF-8')

        urn = entry.find('{http://www.opengis.net/gml/3.2}identifier').text
        xml = et.tostring(entry, encoding="utf-8", method="xml")
        cur.execute('INSERT INTO gml VALUES (?,?,?,?,?)',
                    (urn.encode('UTF-8').decode('UTF-8'), id, buffer(xml), deprecated.encode('UTF-8').decode('UTF-8'), name.encode('UTF-8').decode('UTF-8')))
        con.commit()
        # Write into Whoosh index
        with ix.writer(limitmb=1048, multisegment=True) as writer:
            writer.add_document(**doc)

# ///////////////////////////////////////////////////////
# find in whole document coordinate reference system with transformation
# ///////////////////////////////////////////////////////
    if "-crs-" in entry.attrib['{http://www.opengis.net/gml/3.2}id']:
        doc = copy.deepcopy(dict_index)
        id = entry.attrib['{http://www.opengis.net/gml/3.2}id']
        doc['code'] = id.split('-')[2].encode('UTF-8').decode('UTF-8')
        type = entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}type').text
        doc['kind'] = kind_list[type].decode('utf-8')
        doc['code_id'] = doc['code']
        
		# boost by kind
        boost = 0
        if doc['kind'] == "CRS-PROJCRS":
            boost = 0.2
        if doc['kind'] == "CRS-GEOGCRS" or doc['kind'] == "CRS-GEOG3DCRS":
            boost = 0.05
        # boost by code from csv file
        importance = 0
        try:
            importance = crs_ex_line[code][1]
            if importance == u"":
                importance = 0
        except:
            pass

        doc['_boost'] = float((1 + boost) * (1 + float(importance) * 4))

        if entry.find('{http://www.opengis.net/gml/3.2}remarks') is not None:
            doc['remarks'] = (entry.find(
                '{http://www.opengis.net/gml/3.2}remarks').text).encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource') is not None:
            doc['information_source'] = (entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}informationSource').text).encode('UTF-8').decode('UTF-8')

        doc['revision_date'] = (entry.find(
            './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}revisionDate').text)

        if entry.find(".//*[{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated]") is not None:
            deprecated = entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}isDeprecated').text
            if deprecated == 'true':
                doc['deprecated'] = 1
            elif deprecated == 'false':
                doc['deprecated'] = 0

        if entry.find('.//*{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('.//*{http://www.opengis.net/gml/3.2}name').text
        elif entry.find('{http://www.opengis.net/gml/3.2}name') is not None:
            name = entry.find('{http://www.opengis.net/gml/3.2}name').text
        doc['name'] = name.encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias') is not None:
            doc['alt_name'] = (entry.find(
                './/*{urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset}alias').get('alias')).encode('UTF-8').decode('UTF-8')

        if entry.find('{http://www.opengis.net/gml/3.2}domainOfValidity') is not None:
            area = entry.find(
                '{http://www.opengis.net/gml/3.2}domainOfValidity').get('{http://www.w3.org/1999/xlink}href')
            area = area.split("::")[1]
            doc['bbox'] = dict_area[int(area)][1]
            doc['area'] = (dict_area[int(area)][0]).encode('UTF-8').decode('UTF-8')
            doc['area_code'] = int(area)

        if entry.find('{http://www.opengis.net/gml/3.2}scope') is not None:
            doc['scope'] = (entry.find(
                '{http://www.opengis.net/gml/3.2}scope').text).encode('UTF-8').decode('UTF-8')

        if entry.find('.//*{http://www.isotc211.org/2005/gmd}valueUnit') is not None:
            uom = entry.find(
                './/*{http://www.isotc211.org/2005/gmd}valueUnit').get('{http://www.w3.org/1999/xlink}href')
            uom = uom.split("::")[1]
            doc['uom_code'] = uom
            doc['uom'] = (dict_uom[int(uom)]).encode('UTF-8').decode('UTF-8')

        if entry.find(".//*{http://www.isotc211.org/2005/gco}Decimal") is not None:
            doc['accuracy'] = float(entry.find(
                ".//*{http://www.isotc211.org/2005/gco}Decimal").text)

        sourceCRS = dict_crs[int(doc['code'])][2]
        if sourceCRS != "":
            doc['geogcrs'] = str(sourceCRS).encode('UTF-8').decode('UTF-8'), dict_crs[int(sourceCRS)][0].encode('UTF-8').decode('UTF-8')
            datum_code = dict_crs[int(sourceCRS)][1]
            if datum_code != "":
                datum_name = dict_datum[int(datum_code)][0]
                doc['datum'] = str(datum_code).encode('UTF-8').decode('UTF-8'), datum_name.encode('UTF-8').decode('UTF-8')
                
                primeMeridian_code = dict_datum[int(datum_code)][2]
                primeMeridian_name = dict_meridian[int(primeMeridian_code)][0]
                doc['primem'] = str(primeMeridian_code).encode('UTF-8').decode('UTF-8'), str(primeMeridian_name).encode('UTF-8').decode('UTF-8')
                
                doc['greenwich_longitude'] = str(dict_meridian[int(primeMeridian_code)]).encode('UTF-8').decode('UTF-8')

                ellipsoid_code = dict_datum[int(datum_code)][1]
				
                if ellipsoid_code != 0:  # engineering datum has not ellipsoid
                    ellipsoid_name = dict_ellipsoid[int(ellipsoid_code)]
                    doc['ellipsoid'] = str(ellipsoid_code).encode('UTF-8').decode('UTF-8'), str(ellipsoid_name).encode('UTF-8').decode('UTF-8')
        cs = 0
        if entry.find('{http://www.opengis.net/gml/3.2}cartesianCS') is not None:
            cs = entry.find(
                '{http://www.opengis.net/gml/3.2}cartesianCS').get('{http://www.w3.org/1999/xlink}href')
        elif entry.find('{http://www.opengis.net/gml/3.2}ellipsoidalCS') is not None:
            cs = entry.find(
                '{http://www.opengis.net/gml/3.2}ellipsoidalCS').get('{http://www.w3.org/1999/xlink}href')
        elif entry.find('{http://www.opengis.net/gml/3.2}verticalCS') is not None:
            cs = entry.find(
                '{http://www.opengis.net/gml/3.2}verticalCS').get('{http://www.w3.org/1999/xlink}href')
        elif entry.find('{http://www.opengis.net/gml/3.2}coordinateSystem') is not None:
            cs = entry.find(
                '{http://www.opengis.net/gml/3.2}coordinateSystem').get('{http://www.w3.org/1999/xlink}href')
        elif doc['kind'] == "CRS-COMPOUNDCRS":
            cs = None

        if cs is not None:
            cs = cs.split("::")[1]
            doc['cs'] = cs.encode('UTF-8').decode('UTF-8'), (dict_cs[int(cs)][0]).encode('UTF-8').decode('UTF-8')
            doc['uom_code'] = dict_cs[int(cs)][2]
            doc['uom'] = (dict_uom[int(dict_cs[int(cs)][2])]).encode('UTF-8').decode('UTF-8')
        op = [] 
        
        if sourceCRS != "":
            for crs_op in list_crs_op:
                if crs_op[0] != "":
                    if int(crs_op[0]) == int(sourceCRS):
                        op.append(int(crs_op[1]))
        ref.ImportFromEPSG(int(doc['code']))
        op_code_original = 0
        op_code_trans = {}
        towgs84_original = ref.GetTOWGS84()
        transformations = []

        if len(op) != 0:
            for operation in op:
                parameters = dict_op[int(operation)][1]
                method_code = dict_op[int(operation)][4]
                if method_code != "":
                    method_name = dict_method[int(method_code)]
                accuracy = dict_op[int(operation)][3]
                area_code = dict_op[int(operation)][2]
                if area_code != "":
                    area_name = dict_area[int(area)][0]

                op_code_trans[operation] = parameters
                if towgs84_original == parameters:
                    op_code_original = operation
                    doc['area_trans'] = area_name.encode('UTF-8').decode('UTF-8')
                    doc['area_trans_code'] = area_code
                    doc['accuracy'] = accuracy
                    doc['primary'] = 1
                    doc['method'] = method_code.encode('UTF-8').decode('UTF-8'), method_name.encode('UTF-8').decode('UTF-8')
                    doc['code_trans'] = int(operation)

                transformations.append(operation)
            if operation == op_code_original:
                doc['trans'] = transformations
            else:
                # CRS has transformation to wgs84, but any transformation is
                # not default
                doc['trans'] = transformations
                doc['primary'] = 0

        urn = entry.find('{http://www.opengis.net/gml/3.2}identifier').text
        xml = et.tostring(entry, encoding="utf-8", method="xml")
        cur.execute('INSERT INTO gml VALUES (?,?,?,?,?)',
                    (urn.encode('UTF-8').decode('UTF-8'), id.encode('UTF-8').decode('UTF-8'), buffer(xml), deprecated.encode('UTF-8').decode('UTF-8'), name.encode('UTF-8').decode('UTF-8')))
        con.commit()

        with ix.writer(limitmb=1048, multisegment=True) as writer:
            writer.add_document(**doc)

###############################################################################
print " - INSERT NEW EPSG CODES FROM EXTRA FILES(ESRI,OTHER)"
###############################################################################
ref = osr.SpatialReference()

for extra_file in FILES:

    f = open(extra_file)
    for line in f:
        doc = copy.deepcopy(dict_index)
        code = u""
        kind = u""
        inf_source = u""
        if line[0] == "#":
            sharp, name = line.split(" ", 1)
            name = name.strip()
            continue

        if line[0] == "<":
            code, proj = line.split(" ", 1)
            code = code.replace("<", "").replace(">", "").strip()
            proj = proj.replace("<>", "").strip()

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
        doc['description'] = str(proj).decode('utf-8')
        doc['data_source'] = u"PROJ.4"
        doc['code'] = code
        doc['code_id'] = code
        doc['name'] = name
        doc['kind'] = kind
        doc['information_source'] = inf_source
        doc['_boost'] = score

        # Write into Whoosh index
        with ix.writer(limitmb=1048, multisegment=True) as writer:
            writer.add_document(**doc)