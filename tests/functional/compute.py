import pytest
from os import sys, path
from fixtures import client
from cgi import escape

def escapePre(text):
    return escape(text).\
        replace(u'"', u'&#34;')

def test_info_page(client):
    
    response = client.get("/3857")

    assert b'WGS 84 / Pseudo-Mercator' in response.data
    assert b'Spherical Mercator' in response.data
    assert b'<a href="/900913">900913</a>' in response.data
    assert b'Certain Web mapping and visualisation applications. It is not a recognised geodetic system: for that see ellipsoidal Mercator CRS code 3395' in response.data
    
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
    AUTHORITY["EPSG","3857"]]""").encode('ascii') in response.data