<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<link rel="stylesheet" type="text/css" href="/css/style.css">

	<title>{{title}}</title>

</head>
<body>

<div id ="mysearchabout"><a href=/about>About</a> &nbsp; &nbsp; <a href=/>Search</a></div>

<h1>EPSG.io</h1>

<h2>Find coordinate systems for spatial reference worldwide</h2>
<hr>
<h3>{{item['kind']}}</h3>
<div id="topic">EPSG:{{item['code']}} {{item['name']}} </div>
</br>
%if trans:
	<b>Transformation</b>
%end

</br>
</br>
% i = 0
%for r in trans:
	%if r['link'] == "" and r['deprecated'] == item['deprecated'] and r['area_trans']:
		
		<div id="me">
			</br>
			<li> {{r['area_trans']}}
		
		%if r['accuracy']:
			, accuracy {{r['accuracy']}}
		%end
		
		%if r['code_trans'] != 0:
			code {{r['code_trans']}} 
		%end
		%if r['default'] == True:
			DEFAULT
		%end
		% i +=1
			</li>
		</div>
		</br></br>
		
	%elif r['deprecated'] == item['deprecated'] and r['area_trans']:
		<li><a href="/{{r['link']}}/" title = "{{r['trans_remarks']}}">{{r['area_trans']}}, accuracy 
			{{r['accuracy']}} code {{r['code_trans']}} 
			%if r['default'] == True:
				DEFAULT
			%end
			</a>
			%i+=1
			</br></br>
		</li>

	%end

%end
%if i !=0:
</br>
Count of transformations: {{i}}
</br>
	<b>Information about transformation: {{item['code_trans']}}</b>

	<li>Method: <a href="{{url_method}}">{{item['method']}}</a></li>
	<li>Remarks: {{item['trans_remarks']}}</li>
	<li>Area of use: <a href="{{url_area_trans}}">{{item['area_trans']}}</a></li>

	%if item['concatop']:
	<li>steps of transformation : {{item['concatop'][0]}}</li>
	%end
%end



</br>
</br>
<b>Information about EPSG: {{item['code']}}</b>
<li>Scope: {{item['scope']}}</li>
<li>Area of use: <a href="{{url_area}}">{{item['area']}}</a></li>
<li>Remarks: {{item['remarks']}}</li>
<li>Information source: {{item['information_source']}}</li>
<li>Revision date: {{item['revision_date']}}</li>
%if "children_code" in item:
	%if item['children_code']:
		<li>Coordinate system: <a href="/{{item['children_code']}}-coordsys/">{{item['children_code']}}</a></li>
	%end
%end
%if 'source_geogcrs' in item:
%if item['source_geogcrs']:
 	<li>Geodetic coordinate reference system: <a href="/{{item['source_geogcrs']}}/">{{item['source_geogcrs']}}</a></li>

%end
%end
%if item['datum_code'] != 0 :
	<li>Datum: <a href="/{{item['datum_code']}}-datum/">{{item['datum_code']}}-datum</a></li>
%end
<div id="formats">
%if item['wkt']:


	<li><a href="{{url_format}}/prettywkt">PrettyWKT</a></li>
	<li><a href="{{url_format}}/html">Human-readable PrettyWKT</a></li>
	<li><a href="{{url_format}}/esriwkt">ESRI WKT</a></li>
	<li><a href="{{url_format}}/prj">Download file {{item['code']}}.prj</a></li>
	<li><a href="{{url_format}}/proj4">PROJ.4</a></li>
	<li><a href="{{url_format}}/gml">OGC GML</a></li>
	<li><a href="{{url_format}}/geoserver">GeoServer</a></li>
	<li><a href="{{url_format}}/mapfile">MAPfile</a></li>
	<li><a href="{{url_format}}/mapserverpython">MapSever - Python</a></li>
	<li><a href="{{url_format}}/mapnik">mapnik</a></li>
	<li><a href="{{url_format}}/mapnikpython">mapnik - Python</a></li>
	<li><a href="{{url_format}}/postgis">PostGIS</a></li>
	<li><a href="{{url_format}}/json">JSON</a></li>
	<li><a href="{{url_format}}/ogcwkt">OGC WKT</a></li>
	<li><a href="{{url_format}}/usgs">USGS</a></li>


	</div>
	{{!export}}
%end

%if item['bbox']:

<div id=image>
<img src="/css/crosshair.png" id="crosshair" alt=""/>
<img src="https://maps.googleapis.com/maps/api/staticmap?size=235x190&scale=2&sensor=false&visual_refresh=true&center={{center[0]}},{{center[1]}}&path=color:0xff0000ff|fillcolor:0xff000022|weight:2|{{g_coords}}" alt="SimpleMap" height="190" width="235">
</div>
<li>center coords for wgs = {{center[0]}}, {{center[1]}}</li>
%if trans_coords:
	<li>center coords for EPSG:{{item['code']}} with EPSG:{{item['code_trans']}} transformation  = {{trans_coords[0]}}, {{trans_coords[1]}}, {{trans_coords[2]}}</li>
%end
%end

%if item['wkt'] and item['bbox'] and trans_coords:

<form action= "/{{item['code']}}-{{item['code_trans']}}/coordinates/" method="get">
  	from WGS84 to {{item['name']}} <input type="text" name="wgs" placeholder="{{center[0]}} {{center[1]}}" style="width: 200px"/>
		<input type="submit" value="TRANSFORM">
</form>

<form action= "/{{item['code']}}-{{item['code_trans']}}/coordinates/" method="get">
  	from {{item['name']}} to WGS84 <input type="text" name="other" placeholder="{{trans_coords[0]}} {{trans_coords[1]}}" style="width: 200px"/>
		<input type="submit" value="TRANSFORM">
</form>
%end
</body>
</html>
