# EPSG.io
This service allows you to discover and transform coordinate systems from all over the world. Created and maintained by the [MapTiler team](https://www.maptiler.com/).

## Installation

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
Copy the content of "index" directory from the .zip from the latest project release.

Start the server with:

```
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run
```

or use the gunicorn startup scripts (`./epsgio start`)


## Create your own index from EPSG export

Note: This is not required, as you can easily download the ready-to-use index from releases.

1. Download the newest EPSG database from [http://epsg-registry.org]
   * a. After `login` it will able to `export registry` as `Export GML 3.2.1 with EPSG metadata`
2. Make sure that these files(folder) are in one folder
    * a. folder `extra_codes_proj4_4.8.0.2`
    * b. file `CRS_exceptions.csv`
    * c. file `CRS_exceptions.py`
    * d. file `gml_parser.py`
    * e. file `GmlDictionary.xml` (downloaded EPSG database from http://epsg-registry.org)
3. Start indexing via `python gml_parser.py`
4. Move created `gml.sqlite` into `gml` folder

## Types of URLs:
 * [http://epsg.io/] > main page
 * [http://epsg.io/1623] > transformation or crs
 * [http://epsg.io/5514-1623] > crs with transformation
 * [http://epsg.io/5514-1623.wkt] > page with wkt of crs 5514 with transformation 1623
 * [http://epsg.io/5514-1623/map] > page with map of crs 5514 with transformation 1623
 * [http://epsg.io/8901-primem] > other type then transformation or crs (prime meridia, datum,...)
 * [http://epsg.io/ogp-op-1623] > gml:id from OGC XML
 * [http://epsg.io/urn:ogc:def:coordinateOperation:EPSG::1623] > gml:identifier from OGC XML

CRS and Transformations are just codes (5514, 1623, 4326, 27700)
Other are codes with suffix like:
  * for datums e.g. `9315-datum`
  * for prime meridian e.g. `8901-primem`
  * for ellipsoid e.g. `7004-ellipsoid`
  * for method e.g. `9840-method`
  * for coordinate system e.g. `6422-cs`
  * for axis e.g. `106-axis`
  * for area e.g. `1262-area`
  * for units e.g. `9001-units`

## API for results

For result page exist a export in JSON and JSONP
for example

[http://epsg.io/?q=czech&format=json&trans=1&callback=jsonpFunction]

where:
  * `format=json` for export in json **(obligatory)**
  * `trans=1` for more detailed transformation in each coordinate reference system (optional)
  * `callback=jsonpFunction` for jsonp where "jsonpFunction" is name of Javascript function (optional)

## API for /trans

### For one point
[http://epsg.io/trans?x=50&y=17&z=0&s_srs=4326&t_srs=5514&callback=jsonpFunction]

where everything is optional:
 * `x`, `y`, `z` are coordinates of point, which going to be transformed (default is 0,0,0)
 * `s_srs` represent source coordinate reference system (default is EPSG:4326)
 * `t_srs` represent target coordinate reference system (default is EPSG:4326)
 * `callback=jsonpFunction` is for jsonp where "jsonpFunction" is name of JavaScript function

e.g. [http://epsg.io/trans] will transform point on coordinates 0,0,0 from EPSG:4326 to EPSG:4326

### For many points
[http://epsg.io/trans?data=17,50;17,50,300;17.132,50.456&s_srs=4326&&t_srs=5514]

Where
* data=x,y;x,y,z;x.x,y.y (for example)
* Delimiter between points is `;`
* Delimiter between x,y,z is `,`
* Delimiter between decimal is `.`

## Types of queries

 * `kind:`

 value | meaning | value | meaning
 --- | --- | --- | ---
 CRS(default) | All coordinate reference systems | ELLIPSOID | Ellipsoid
 PROJCRS | Projected coordinate systems | PRIMEM | Prime meridian
 GEOGCRS|Geodetic coordinate systems|METHOD|Method
 GEOG3DCRS|Geodetic 3D coordinate systems|CS|Coordinate systems
 GCENCRS|Geocentric coordinate systems|VERTCS|Vertical coordinate system
 VERTCRS|Vertical coordinate systems|SPHERCS|Spherical coordinate system
 ENGCRS|Engineering coordinate systems|CARTESCS|Cartesian coordinate system
 COMPOUNDCRS|Compound coordinate systems|ELLIPCS|Ellipsoidal coordinate system
 COORDOP|All operations|AXIS|Axis
 COPTRANS|Transformations|AREA|Area
 COPCONOP|Compound operations|UNIT|Unit
 COPCON|Conversions|ANGUNIT|Angle unit
 DATUM|All datums|SCALEUNIT|Scale unit
 VERTDAT|Vertical datums|LENUNIT|Length unit
 ENGDAT|Engineering datums|TIMEUNIT|Time unit
 GEODDAT|Geodetic datums||


 * `deprecated:` 0(default), 1
 * `code:` number of EPSG (5514, 4326,...)
 * `name:` string of name (wgs 84, jtsk, s-jtks)
 * `area:` string area of use (czech republic, world)
 * `area_trans:` string area of use of transformation
 * `alt_title:` alternative title (wgs84,...)

combinations: 8901 kind:PRIMEM, 1623 kind:COORDOP, code:1625 kind:COORDOP deprecated:1,...

