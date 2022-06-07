# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from os import sys, path
from fixtures import client
from cgi import escape

def escapePre(text):
    text = escape(text).\
        replace(u'"', u'&#34;')

    # text = text.\
    #     replace(u'"', u'&#34;').\
    #     replace(u'<', u'&lt;').\
    #     replace(u'>', u'&gt;')

    # print(text)

    return text

def test_transform_api(client):
  response = client.get("/trans?x=50&y=17&z=0&s_srs=4326&t_srs=5514")
  responseText = response.data.decode("utf-8")

  assert responseText == """{
  "x": "2960518.94", 
  "y": "-4472028.38", 
  "z": "176.13"
}
"""

def test_transform_multiple_api(client):
  response = client.get("/trans?data=17,50;17,50,300;17.132,50.456&s_srs=4326&&t_srs=5514")
  responseText = response.data.decode("utf-8")

  assert responseText == """[
  {
    "x": "-560595.70", 
    "y": "-1074706.26", 
    "z": "-43.16"
  }, 
  {
    "x": "-560595.70", 
    "y": "-1074706.26", 
    "z": "256.84"
  }, 
  {
    "x": "-546082.35", 
    "y": "-1025196.69", 
    "z": "-42.40"
  }
]
"""

# Will throw "ERROR 6: No translation for an empty SRS to PROJ.4 format is known." in std err

def test_czech_search_api(client):
  response = client.get("/?q=czech&format=json&trans=1")
  responseText = response.data.decode("utf-8")

  assert responseText == """{"status": "ok", "number_result": 2, "results": [{"code": "8045", "kind": "CRS-PROJCRS", "bbox": [50.45, 14.41, 47.42, 18.86], "wkt": "", "unit": "metre", "proj4": "", "name": "St. Stephen Grid (Ferro)", "area": "Austria - Lower Austria. Czechia - Moravia and Czech Silesia.", "default_trans": 0, "trans": [], "accuracy": ""}, {"code": "8043", "kind": "CRS-GEOGCRS", "bbox": [50.45, 14.41, 47.42, 18.86], "wkt": "", "unit": "degree (supplier to define representation)", "proj4": "", "name": "St. Stephen (Ferro)", "area": "Austria - Lower Austria. Czechia - Moravia and Czech Silesia.", "default_trans": 0, "trans": [], "accuracy": ""}]}"""


def test_czech_search_page(client):
  response = client.get("/?q=pakistan")
  responseText = response.data.decode("utf-8")

  assert "Kalianpur 1962 / UTM zone 43N" in responseText
  
  assert "Area of use: Pakistan - onshore and offshore. (accuracy: 999.0)" in responseText
  
  assert "Kalianpur 1937" in responseText
  
  assert "Kalianpur 1880 / India zone IIa" in responseText

  assert "EPSG:24313" in responseText
  assert "with transformation: 1247" in responseText


def test_5514_1623_wkt_api(client):
  
  response = client.get("/5514-1623.wkt")
  responseText = response.data.decode("utf-8")

  assert responseText == """PROJCS["S-JTSK / Krovak East North",GEOGCS["S-JTSK",DATUM["System_Jednotne_Trigonometricke_Site_Katastralni",SPHEROID["Bessel 1841",6377397.155,299.1528128,AUTHORITY["EPSG","7004"]],TOWGS84[570.8,85.7,462.8,4.998,1.587,5.261,3.56],AUTHORITY["EPSG","6156"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4156"]],PROJECTION["Krovak"],PARAMETER["latitude_of_center",49.5],PARAMETER["longitude_of_center",24.83333333333333],PARAMETER["azimuth",30.28813972222222],PARAMETER["pseudo_standard_parallel_1",78.5],PARAMETER["scale_factor",0.9999],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["X",EAST],AXIS["Y",NORTH],AUTHORITY["EPSG","5514"]]"""

def test_8901_primem_page(client):
  
  response = client.get("/8901-primem")
  responseText = response.data.decode("utf-8")

  assert "The international reference meridian as defined first by the 1884 International Meridian Conference and later by the Bureau International" in responseText

  assert escapePre("""<?xml version="1.0" encoding="UTF-8"?>
 <gml:PrimeMeridian xmlns:epsg="urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" gml:id="iogp-meridian-8901">
  <gml:metaDataProperty>
    <epsg:CommonMetaData>
      <epsg:informationSource>OGP</epsg:informationSource>
      <epsg:revisionDate>2016-12-15</epsg:revisionDate>
      <epsg:changes>
        <epsg:changeID xlink:href="urn:ogc:def:change-request:EPSG::1996.290" />
        <epsg:changeID xlink:href="urn:ogc:def:change-request:EPSG::2016.045" />
      </epsg:changes>
      <epsg:show>true</epsg:show>
      <epsg:isDeprecated>false</epsg:isDeprecated>
    </epsg:CommonMetaData>
  </gml:metaDataProperty>
  <gml:identifier codeSpace="IOGP">urn:ogc:def:meridian:EPSG::8901</gml:identifier>
  <gml:name>Greenwich</gml:name>""") in responseText

# This will throw "EPSG PCS/GCS code 1623 not found in EPSG support files." in std-err
def test_1623_page(client):
  
  response = client.get("/1623")
  responseText = response.data.decode("utf-8")

  assert "S-JTSK to WGS 84 (1)" in responseText

  assert "Assumes ETRS89 and WGS 84 can be considered the same to within the accuracy of the transformation" in responseText

  assert escapePre("""<?xml version="1.0" encoding="UTF-8"?>
 <gml:Transformation xmlns:epsg="urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" gml:id="ogp-op-1623">
   <gml:metaDataProperty>
      <epsg:CommonMetaData>
         <epsg:type>transformation</epsg:type>
         <epsg:informationSource>OGP</epsg:informationSource>
         <epsg:revisionDate>2010-11-02</epsg:revisionDate>
         <epsg:changes>
            <epsg:changeID xlink:href="urn:ogc:def:change-request:EPSG::2010.071" />
         </epsg:changes>
         <epsg:show>true</epsg:show>
         <epsg:isDeprecated>false</epsg:isDeprecated>
      </epsg:CommonMetaData>
   </gml:metaDataProperty>
   <gml:metaDataProperty>
      <epsg:CoordinateOperationMetaData>
         <epsg:variant>1</epsg:variant>
      </epsg:CoordinateOperationMetaData>
   </gml:metaDataProperty>
   <gml:identifier codeSpace="OGP">urn:ogc:def:coordinateOperation:EPSG::1623</gml:identifier>
   <gml:name>S-JTSK to WGS 84 (1)</gml:name>
   <gml:remarks>Parameter values from S-JTSK to ETRS89 (1) (code 1622). Assumes ETRS89 and WGS 84 can be considered the same to within the accuracy of the transformation. Replaced by S-JTSK to WGS 84 (5) (code 5239).</gml:remarks>
   <gml:domainOfValidity xlink:href="urn:ogc:def:area:EPSG::1079" />
   <gml:scope>For applications to an accuracy of 1 metre.</gml:scope>
   <gml:operationVersion>EPSG-Cze</gml:operationVersion>
   <gml:coordinateOperationAccuracy>
      <gmd:DQ_RelativeInternalPositionalAccuracy>
         <gmd:result>
            <gmd:DQ_QuantitativeResult>
               <gmd:valueUnit xlink:href="urn:ogc:def:uom:EPSG::9001" />
               <gmd:value>
                  <gco:Record>
                     <gco:Decimal>1</gco:Decimal>
                  </gco:Record>
               </gmd:value>
            </gmd:DQ_QuantitativeResult>
         </gmd:result>
      </gmd:DQ_RelativeInternalPositionalAccuracy>
   </gml:coordinateOperationAccuracy>
   <gml:sourceCRS xlink:href="urn:ogc:def:crs:EPSG::4156" />
   <gml:targetCRS xlink:href="urn:ogc:def:crs:EPSG::4326" />
   <gml:method xlink:href="urn:ogc:def:method:EPSG::9606" />
   <gml:parameterValue>
      <gml:ParameterValue>
         <gml:value uom="urn:ogc:def:uom:EPSG::9001">570.8</gml:value>
         <gml:operationParameter xlink:href="urn:ogc:def:parameter:EPSG::8605" />
      </gml:ParameterValue>
   </gml:parameterValue>
   <gml:parameterValue>
      <gml:ParameterValue>
         <gml:value uom="urn:ogc:def:uom:EPSG::9001">85.7</gml:value>
         <gml:operationParameter xlink:href="urn:ogc:def:parameter:EPSG::8606" />
      </gml:ParameterValue>
   </gml:parameterValue>
   <gml:parameterValue>
      <gml:ParameterValue>
         <gml:value uom="urn:ogc:def:uom:EPSG::9001">462.8</gml:value>
         <gml:operationParameter xlink:href="urn:ogc:def:parameter:EPSG::8607" />
      </gml:ParameterValue>
   </gml:parameterValue>
   <gml:parameterValue>
      <gml:ParameterValue>
         <gml:value uom="urn:ogc:def:uom:EPSG::9104">4.998</gml:value>
         <gml:operationParameter xlink:href="urn:ogc:def:parameter:EPSG::8608" />
      </gml:ParameterValue>
   </gml:parameterValue>
   <gml:parameterValue>
      <gml:ParameterValue>
         <gml:value uom="urn:ogc:def:uom:EPSG::9104">1.587</gml:value>
         <gml:operationParameter xlink:href="urn:ogc:def:parameter:EPSG::8609" />
      </gml:ParameterValue>
   </gml:parameterValue>
   <gml:parameterValue>
      <gml:ParameterValue>
         <gml:value uom="urn:ogc:def:uom:EPSG::9104">5.261</gml:value>
         <gml:operationParameter xlink:href="urn:ogc:def:parameter:EPSG::8610" />
      </gml:ParameterValue>
   </gml:parameterValue>
   <gml:parameterValue>
      <gml:ParameterValue>
         <gml:value uom="urn:ogc:def:uom:EPSG::9202">3.56</gml:value>
         <gml:operationParameter xlink:href="urn:ogc:def:parameter:EPSG::8611" />
      </gml:ParameterValue>
   </gml:parameterValue>
</gml:Transformation>""") in responseText



def test_3857_page(client):
    
    response = client.get("/3857")
    responseText = response.data.decode("utf-8")

    assert b'WGS 84 / Pseudo-Mercator' in response.data
    assert b'Spherical Mercator' in response.data
    assert b'<a href="/900913">900913</a>' in response.data
    assert b'Certain Web mapping and visualisation applications. It is not a recognised geodetic system: for that see ellipsoidal Mercator CRS code 3395' in response.data
    
    # Well Known Text (WKT)
    assert escapePre("""PROJCS["WGS 84 / Pseudo-Mercator",
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]],
    PROJECTION["Mercator_1SP"],
    PARAMETER["central_meridian",0],
    PARAMETER["scale_factor",1],
    PARAMETER["false_easting",0],
    PARAMETER["false_northing",0],
    UNIT["metre",1,
        AUTHORITY["EPSG","9001"]],
    AXIS["X",EAST],
    AXIS["Y",NORTH],
    EXTENSION["PROJ4","+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs"],
    AUTHORITY["EPSG","3857"]]""") in responseText

    # OGC WKT
    assert """PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.017453292519943295]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]""" in responseText

    # ESRI WKT
    assert """PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.017453292519943295]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]""" in responseText
    
    # OGC GML
    assert escapePre("""<?xml version="1.0" encoding="UTF-8"?>
 <gml:ProjectedCRS xmlns:epsg="urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" gml:id="iogp-crs-3857">
  <gml:metaDataProperty>
    <epsg:CommonMetaData>
      <epsg:type>projected</epsg:type>
      <epsg:alias alias="WGS 84 / Popular Visualisation Pseudo-Mercator" code="5966" codeSpace="urn:ogc:def:naming-system:EPSG::7301" />
      <epsg:alias alias="Web Mercator" code="7067" codeSpace="urn:ogc:def:naming-system:EPSG::7301" />
      <epsg:informationSource>Microsoft.</epsg:informationSource>
      <epsg:revisionDate>2015-11-25</epsg:revisionDate>
      <epsg:changes>
        <epsg:changeID xlink:href="urn:ogc:def:change-request:EPSG::2008.114" />
        <epsg:changeID xlink:href="urn:ogc:def:change-request:EPSG::2014.033" />
        <epsg:changeID xlink:href="urn:ogc:def:change-request:EPSG::2014.052" />
        <epsg:changeID xlink:href="urn:ogc:def:change-request:EPSG::2015.063" />
      </epsg:changes>
      <epsg:show>true</epsg:show>
      <epsg:isDeprecated>false</epsg:isDeprecated>
    </epsg:CommonMetaData>
  </gml:metaDataProperty>
  <gml:identifier codeSpace="IOGP">urn:ogc:def:crs:EPSG::3857</gml:identifier>
  <gml:name>WGS 84 / Pseudo-Mercator</gml:name>
  <gml:remarks>Uses spherical development of ellipsoidal coordinates. Relative to WGS 84 / World Mercator (CRS code 3395) errors of 0.7 percent in scale and differences in northing of up to 43km in the map (equivalent to 21km on the ground) may arise.</gml:remarks>
  <gml:domainOfValidity xlink:href="urn:ogc:def:area:EPSG::3544" />
  <gml:scope>Certain Web mapping and visualisation applications. It is not a recognised geodetic system: for that see ellipsoidal Mercator CRS code 3395 (WGS 84 / World Mercator).</gml:scope>
  <gml:conversion xlink:href="urn:ogc:def:coordinateOperation:EPSG::3856" />
  <gml:baseGeodeticCRS xlink:href="urn:ogc:def:crs:EPSG::4326" />
  <gml:cartesianCS xlink:href="urn:ogc:def:cs:EPSG::4499" />
</gml:ProjectedCRS>""") in responseText

    # XML
    assert escapePre("""<?xml version="1.0" encoding="UTF-8"?>
 <gml:ProjectedCRS gml:id="ogrcrs13" xmlns:gml="http://www.opengis.net/gml/3.2">
  <gml:srsName>WGS 84 / Pseudo-Mercator</gml:srsName>
  <gml:srsID>
    <gml:name gml:codeSpace="urn:ogc:def:crs:EPSG::">3857</gml:name>
  </gml:srsID>
  <gml:baseCRS>
    <gml:GeographicCRS gml:id="ogrcrs14">
      <gml:srsName>WGS 84</gml:srsName>
      <gml:srsID>
        <gml:name gml:codeSpace="urn:ogc:def:crs:EPSG::">4326</gml:name>
      </gml:srsID>
      <gml:usesEllipsoidalCS>
        <gml:EllipsoidalCS gml:id="ogrcrs15">
          <gml:csName>ellipsoidal</gml:csName>
          <gml:csID>
            <gml:name gml:codeSpace="urn:ogc:def:cs:EPSG::">6402</gml:name>
          </gml:csID>
          <gml:usesAxis>
            <gml:CoordinateSystemAxis gml:id="ogrcrs16" gml:uom="urn:ogc:def:uom:EPSG::9102">
              <gml:name>Geodetic latitude</gml:name>
              <gml:axisID>
                <gml:name gml:codeSpace="urn:ogc:def:axis:EPSG::">9901</gml:name>
              </gml:axisID>
              <gml:axisAbbrev>Lat</gml:axisAbbrev>
              <gml:axisDirection>north</gml:axisDirection>
            </gml:CoordinateSystemAxis>
          </gml:usesAxis>
          <gml:usesAxis>
            <gml:CoordinateSystemAxis gml:id="ogrcrs17" gml:uom="urn:ogc:def:uom:EPSG::9102">
              <gml:name>Geodetic longitude</gml:name>
              <gml:axisID>
                <gml:name gml:codeSpace="urn:ogc:def:axis:EPSG::">9902</gml:name>
              </gml:axisID>
              <gml:axisAbbrev>Lon</gml:axisAbbrev>
              <gml:axisDirection>east</gml:axisDirection>
            </gml:CoordinateSystemAxis>
          </gml:usesAxis>
        </gml:EllipsoidalCS>
      </gml:usesEllipsoidalCS>
      <gml:usesGeodeticDatum>
        <gml:GeodeticDatum gml:id="ogrcrs18">
          <gml:datumName>WGS_1984</gml:datumName>
          <gml:datumID>
            <gml:name gml:codeSpace="urn:ogc:def:datum:EPSG::">6326</gml:name>
          </gml:datumID>
          <gml:usesPrimeMeridian>
            <gml:PrimeMeridian gml:id="ogrcrs19">
              <gml:meridianName>Greenwich</gml:meridianName>
              <gml:meridianID>
                <gml:name gml:codeSpace="urn:ogc:def:meridian:EPSG::">8901</gml:name>
              </gml:meridianID>
              <gml:greenwichLongitude>
                <gml:angle gml:uom="urn:ogc:def:uom:EPSG::9102">0</gml:angle>
              </gml:greenwichLongitude>
            </gml:PrimeMeridian>
          </gml:usesPrimeMeridian>
          <gml:usesEllipsoid>
            <gml:Ellipsoid gml:id="ogrcrs20">
              <gml:ellipsoidName>WGS 84</gml:ellipsoidName>
              <gml:ellipsoidID>
                <gml:name gml:codeSpace="urn:ogc:def:ellipsoid:EPSG::">7030</gml:name>
              </gml:ellipsoidID>
              <gml:semiMajorAxis gml:uom="urn:ogc:def:uom:EPSG::9001">6378137</gml:semiMajorAxis>
              <gml:secondDefiningParameter>
                <gml:inverseFlattening gml:uom="urn:ogc:def:uom:EPSG::9201">298.257223563</gml:inverseFlattening>
              </gml:secondDefiningParameter>
            </gml:Ellipsoid>
          </gml:usesEllipsoid>
        </gml:GeodeticDatum>
      </gml:usesGeodeticDatum>
    </gml:GeographicCRS>
  </gml:baseCRS>
  <gml:definedByConversion>
    <gml:Conversion gml:id="ogrcrs21" />
  </gml:definedByConversion>
  <gml:usesCartesianCS>
    <gml:CartesianCS gml:id="ogrcrs22">
      <gml:csName>Cartesian</gml:csName>
      <gml:csID>
        <gml:name gml:codeSpace="urn:ogc:def:cs:EPSG::">4400</gml:name>
      </gml:csID>
      <gml:usesAxis>
        <gml:CoordinateSystemAxis gml:id="ogrcrs23" gml:uom="urn:ogc:def:uom:EPSG::9001">
          <gml:name>Easting</gml:name>
          <gml:axisID>
            <gml:name gml:codeSpace="urn:ogc:def:axis:EPSG::">9906</gml:name>
          </gml:axisID>
          <gml:axisAbbrev>E</gml:axisAbbrev>
          <gml:axisDirection>east</gml:axisDirection>
        </gml:CoordinateSystemAxis>
      </gml:usesAxis>
      <gml:usesAxis>
        <gml:CoordinateSystemAxis gml:id="ogrcrs24" gml:uom="urn:ogc:def:uom:EPSG::9001">
          <gml:name>Northing</gml:name>
          <gml:axisID>
            <gml:name gml:codeSpace="urn:ogc:def:axis:EPSG::">9907</gml:name>
          </gml:axisID>
          <gml:axisAbbrev>N</gml:axisAbbrev>
          <gml:axisDirection>north</gml:axisDirection>
        </gml:CoordinateSystemAxis>
      </gml:usesAxis>
    </gml:CartesianCS>
  </gml:usesCartesianCS>
</gml:ProjectedCRS>""") in responseText

    # Proj4
    assert "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs" in responseText

    # MapServer
    assert escapePre("""PROJECTION
	"proj=merc"
	"a=6378137"
	"b=6378137"
	"lat_ts=0.0"
	"lon_0=0.0"
	"x_0=0.0"
	"y_0=0"
	"k=1.0"
	"units=m"
	"nadgrids=@null"
	"wktext"
	"no_defs"
END""") in responseText

    # Mapnik
    assert escapePre("""<?xml version="1.0" encoding="utf-8"?>
<Map srs="+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs">
	<Layer srs="+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs">
	</Layer>
</Map>""") in responseText

def test_32100_1712_page(client):
    
    response = client.get("/32100-1712")
    responseText = response.data.decode("utf-8")

    assert b'NAD83 / Montana' in response.data
    assert b'NADCON' in response.data
    assert b'NAD83(HARN) (5) (code 1478)' in response.data
    assert b'639723.10 -812057.48' in response.data
    assert b'1229545.03 -330764.88' in response.data
    
    # Well Known Text (WKT)
    assert escapePre("""PROJCS["NAD83 / Montana",
    GEOGCS["NAD83",
        DATUM["North_American_Datum_1983",
            SPHEROID["GRS 1980",6378137,298.257222101,
                AUTHORITY["EPSG","7019"]],
            TOWGS84[0,0,0,0,0,0,0],
            AUTHORITY["EPSG","6269"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4269"]],
    PROJECTION["Lambert_Conformal_Conic_2SP"],
    PARAMETER["standard_parallel_1",49],
    PARAMETER["standard_parallel_2",45],
    PARAMETER["latitude_of_origin",44.25],
    PARAMETER["central_meridian",-109.5],
    PARAMETER["false_easting",600000],
    PARAMETER["false_northing",0],
    UNIT["metre",1,
        AUTHORITY["EPSG","9001"]],
    AXIS["X",EAST],
    AXIS["Y",NORTH],
    AUTHORITY["EPSG","32100"]]""") in responseText

    # OGC WKT
    assert escapePre("""PROJCS["NAD83 / Montana",GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4269"]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["standard_parallel_1",49],PARAMETER["standard_parallel_2",45],PARAMETER["latitude_of_origin",44.25],PARAMETER["central_meridian",-109.5],PARAMETER["false_easting",600000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["X",EAST],AXIS["Y",NORTH],AUTHORITY["EPSG","32100"]]""") in responseText

    # ESRI WKT
    assert """PROJCS["NAD83_Montana",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["standard_parallel_1",49],PARAMETER["standard_parallel_2",45],PARAMETER["latitude_of_origin",44.25],PARAMETER["central_meridian",-109.5],PARAMETER["false_easting",600000],PARAMETER["false_northing",0],UNIT["Meter",1]]""" in responseText
    
    # OGC GML
    assert escapePre("""<?xml version="1.0" encoding="UTF-8"?>
 <gml:ProjectedCRS xmlns:epsg="urn:x-ogp:spec:schema-xsd:EPSG:1.0:dataset" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xlink="http://www.w3.org/1999/xlink" gml:id="epsg-crs-32100">
   <gml:metaDataProperty>
      <epsg:CommonMetaData>
         <epsg:type>projected</epsg:type>
         <epsg:alias alias="NAD83 / Montana (m)" code="1553" codeSpace="urn:ogc:def:naming-system:EPSG::7301" />
         <epsg:revisionDate>2000-03-07</epsg:revisionDate>
         <epsg:changes>
            <epsg:changeID xlink:href="urn:ogc:def:change-request:EPSG::2000.091" />
         </epsg:changes>
         <epsg:show>true</epsg:show>
         <epsg:isDeprecated>false</epsg:isDeprecated>
      </epsg:CommonMetaData>
   </gml:metaDataProperty>
   <gml:identifier codeSpace="OGP">urn:ogc:def:crs:EPSG::32100</gml:identifier>
   <gml:name>NAD83 / Montana</gml:name>
   <gml:remarks>State law defines system in International feet (note: not US survey feet). See code 2256 for equivalent non-metric definition. For applications with an accuracy of better than 1m, replaced by NAD83(HARN) / SPCS.</gml:remarks>
   <gml:domainOfValidity xlink:href="urn:ogc:def:area:EPSG::1395" />
   <gml:scope>Large and medium scale topographic mapping and engineering survey.</gml:scope>
   <gml:conversion xlink:href="urn:ogc:def:coordinateOperation:EPSG::12530" />
   <gml:baseGeodeticCRS xlink:href="urn:ogc:def:crs:EPSG::4269" />
   <gml:cartesianCS xlink:href="urn:ogc:def:cs:EPSG::4499" />
</gml:ProjectedCRS>""") in responseText

    # XML
    assert escapePre("""<?xml version="1.0" encoding="UTF-8"?>
 <gml:ProjectedCRS gml:id="ogrcrs37" xmlns:gml="http://www.opengis.net/gml/3.2">
  <gml:srsName>NAD83 / Montana</gml:srsName>
  <gml:srsID>
    <gml:name gml:codeSpace="urn:ogc:def:crs:EPSG::">32100</gml:name>
  </gml:srsID>
  <gml:baseCRS>
    <gml:GeographicCRS gml:id="ogrcrs38">
      <gml:srsName>NAD83</gml:srsName>
      <gml:srsID>
        <gml:name gml:codeSpace="urn:ogc:def:crs:EPSG::">4269</gml:name>
      </gml:srsID>
      <gml:usesEllipsoidalCS>
        <gml:EllipsoidalCS gml:id="ogrcrs39">
          <gml:csName>ellipsoidal</gml:csName>
          <gml:csID>
            <gml:name gml:codeSpace="urn:ogc:def:cs:EPSG::">6402</gml:name>
          </gml:csID>
          <gml:usesAxis>
            <gml:CoordinateSystemAxis gml:id="ogrcrs40" gml:uom="urn:ogc:def:uom:EPSG::9102">
              <gml:name>Geodetic latitude</gml:name>
              <gml:axisID>
                <gml:name gml:codeSpace="urn:ogc:def:axis:EPSG::">9901</gml:name>
              </gml:axisID>
              <gml:axisAbbrev>Lat</gml:axisAbbrev>
              <gml:axisDirection>north</gml:axisDirection>
            </gml:CoordinateSystemAxis>
          </gml:usesAxis>
          <gml:usesAxis>
            <gml:CoordinateSystemAxis gml:id="ogrcrs41" gml:uom="urn:ogc:def:uom:EPSG::9102">
              <gml:name>Geodetic longitude</gml:name>
              <gml:axisID>
                <gml:name gml:codeSpace="urn:ogc:def:axis:EPSG::">9902</gml:name>
              </gml:axisID>
              <gml:axisAbbrev>Lon</gml:axisAbbrev>
              <gml:axisDirection>east</gml:axisDirection>
            </gml:CoordinateSystemAxis>
          </gml:usesAxis>
        </gml:EllipsoidalCS>
      </gml:usesEllipsoidalCS>
      <gml:usesGeodeticDatum>
        <gml:GeodeticDatum gml:id="ogrcrs42">
          <gml:datumName>North_American_Datum_1983</gml:datumName>
          <gml:datumID>
            <gml:name gml:codeSpace="urn:ogc:def:datum:EPSG::">6269</gml:name>
          </gml:datumID>
          <gml:usesPrimeMeridian>
            <gml:PrimeMeridian gml:id="ogrcrs43">
              <gml:meridianName>Greenwich</gml:meridianName>
              <gml:meridianID>
                <gml:name gml:codeSpace="urn:ogc:def:meridian:EPSG::">8901</gml:name>
              </gml:meridianID>
              <gml:greenwichLongitude>
                <gml:angle gml:uom="urn:ogc:def:uom:EPSG::9102">0</gml:angle>
              </gml:greenwichLongitude>
            </gml:PrimeMeridian>
          </gml:usesPrimeMeridian>
          <gml:usesEllipsoid>
            <gml:Ellipsoid gml:id="ogrcrs44">
              <gml:ellipsoidName>GRS 1980</gml:ellipsoidName>
              <gml:ellipsoidID>
                <gml:name gml:codeSpace="urn:ogc:def:ellipsoid:EPSG::">7019</gml:name>
              </gml:ellipsoidID>
              <gml:semiMajorAxis gml:uom="urn:ogc:def:uom:EPSG::9001">6378137</gml:semiMajorAxis>
              <gml:secondDefiningParameter>
                <gml:inverseFlattening gml:uom="urn:ogc:def:uom:EPSG::9201">298.257222101</gml:inverseFlattening>
              </gml:secondDefiningParameter>
            </gml:Ellipsoid>
          </gml:usesEllipsoid>
        </gml:GeodeticDatum>
      </gml:usesGeodeticDatum>
    </gml:GeographicCRS>
  </gml:baseCRS>
  <gml:definedByConversion>
    <gml:Conversion gml:id="ogrcrs45" />
  </gml:definedByConversion>
  <gml:usesCartesianCS>
    <gml:CartesianCS gml:id="ogrcrs46">
      <gml:csName>Cartesian</gml:csName>
      <gml:csID>
        <gml:name gml:codeSpace="urn:ogc:def:cs:EPSG::">4400</gml:name>
      </gml:csID>
      <gml:usesAxis>
        <gml:CoordinateSystemAxis gml:id="ogrcrs47" gml:uom="urn:ogc:def:uom:EPSG::9001">
          <gml:name>Easting</gml:name>
          <gml:axisID>
            <gml:name gml:codeSpace="urn:ogc:def:axis:EPSG::">9906</gml:name>
          </gml:axisID>
          <gml:axisAbbrev>E</gml:axisAbbrev>
          <gml:axisDirection>east</gml:axisDirection>
        </gml:CoordinateSystemAxis>
      </gml:usesAxis>
      <gml:usesAxis>
        <gml:CoordinateSystemAxis gml:id="ogrcrs48" gml:uom="urn:ogc:def:uom:EPSG::9001">
          <gml:name>Northing</gml:name>
          <gml:axisID>
            <gml:name gml:codeSpace="urn:ogc:def:axis:EPSG::">9907</gml:name>
          </gml:axisID>
          <gml:axisAbbrev>N</gml:axisAbbrev>
          <gml:axisDirection>north</gml:axisDirection>
        </gml:CoordinateSystemAxis>
      </gml:usesAxis>
    </gml:CartesianCS>
  </gml:usesCartesianCS>
</gml:ProjectedCRS>""") in responseText


    # Proj4
    assert "+proj=lcc +lat_1=49 +lat_2=45 +lat_0=44.25 +lon_0=-109.5 +x_0=600000 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs " in responseText

    # MapServer
    assert escapePre("""PROJECTION
	"proj=lcc"
	"lat_1=49"
	"lat_2=45"
	"lat_0=44.25"
	"lon_0=-109.5"
	"x_0=600000"
	"y_0=0"
	"ellps=GRS80"
	"towgs84=0,0,0,0,0,0,0"
	"units=m"
	"no_defs"
END""") in responseText

    # Mapnik
    assert escapePre("""<?xml version="1.0" encoding="utf-8"?>
<Map srs="+proj=lcc +lat_1=49 +lat_2=45 +lat_0=44.25 +lon_0=-109.5 +x_0=600000 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs">
	<Layer srs="+proj=lcc +lat_1=49 +lat_2=45 +lat_0=44.25 +lon_0=-109.5 +x_0=600000 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs">
	</Layer>
</Map>""") in responseText