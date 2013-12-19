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
<h3>
	%for i in range(0,len(facets_list)):
	%if facets_list[i][0] == item['kind']:
	{{facets_list[i][3]}} - {{facets_list[i][1]}}
	%end
	%end

</h3>
<div id="topic">EPSG:{{item['code']}} {{item['name']}} </div>
</br>
%if default_trans != item:
	<b>Transformations</b>
%end

</br>
</br>
% i = 0
%for r in trans:
	%if r['link'] == "" and r['deprecated'] == 0 and r['area_trans']:
		
		<div id="me">
			</br>
			<li> {{r['area_trans']}}
		
		%if r['accuracy']:
			, accuracy {{r['accuracy']}}m, 
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
		
	%elif r['deprecated'] == 0 and r['area_trans']:
		<li><a href="/{{r['link']}}/" title = "{{r['trans_remarks']}}">{{r['area_trans']}}, accuracy 
			{{r['accuracy']}}m, code {{r['code_trans']}} 
			%if r['default'] == True:
				DEFAULT
			%end
			</a>
			%i+=1
			</br></br>
		</li>
	
	%end
%end

<a href="#" onClick="javascript:document.getElementById('trans_deprecated').style.display='block';return false">Show deprecated transformations</a>
<div id="trans_deprecated" style="display:none">
%a = 0
%for r in trans:
%if r['deprecated'] == 1:
	%if r['link'] == "":
	<li>{{r['area_trans']}}, accuracy 
		{{r['accuracy']}}m, code {{r['code_trans']}} DEPRECATED
		%if r['default'] == True:
			DEFAULT
		%end

		</br></br>
	%else:
	<li><a href="/{{r['link']}}/" title = "{{r['trans_remarks']}}">{{r['area_trans']}}, accuracy 
		{{r['accuracy']}}m,  code {{r['code_trans']}} DEPRECATED
		%if r['default'] == True:
			DEFAULT
		%end
		</a>
		</br></br>
	%end
	%a+=1
%end
%end

</div>
</br>
</br>


%if (i !=0 or a!=0) and default_trans:
</br>
Count of transformations: {{i}} (deprecated: {{a}})
</br>
	<b>Information about transformation: {{default_trans['code']}}</b>

	<li>Method: <a href="{{url_method}}">{{default_trans['method']}}</a></li>
	<li>Remarks: {{default_trans['remarks']}}</li>
	<li>Area of use: <a href="{{url_area_trans}}">{{default_trans['area']}}</a></li>
	%if url_concatop != []:
		%for url in url_concatop:
			<li>steps of transformation : <a href="{{url}}">{{url}}</a></li>
		%end
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
%if item['concatop']:
<li>steps of transformation : {{item['concatop']}}</li>
%end
%if nadgrid:
	<li>NadGrid file : {{nadgrid}}</li>
%end

%if 'source_geogcrs' in item:
%if item['source_geogcrs']:
 	<li>Geodetic coordinate reference system: <a href="/{{item['source_geogcrs']}}/">{{item['source_geogcrs']}}</a></li>

%end
%end
%if 'datum_code' in item:
	%if item['datum_code'] != 0 :
		<li>Datum: <a href="/{{item['datum_code']}}-datum/">{{item['datum_code']}}-datum</a></li>
	%end
%end
%if 'children_code' in item:
	%if item['children_code'] != 0 :
		<li>Coordinate System: <a href="/{{item['children_code']}}-coordsys/">{{item['children_code']}}-coordsys</a></li>
	%end
%end


%if url_format:
<div id="formats">

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
%end
{{!export}}

%if item['bbox']:

<div id=image>
<img src="/css/crosshair.png" id="crosshair" alt=""/>
<img src="https://maps.googleapis.com/maps/api/staticmap?size=235x190&scale=2&sensor=false&visual_refresh=true&center={{center[0]}},{{center[1]}}&path=color:0xff0000ff|fillcolor:0xff000022|weight:2|{{g_coords}}" alt="SimpleMap" height="190" width="235">
</div>
<li>center coords for wgs = {{center[0]}}, {{center[1]}}</li>
%if trans_coords:
	<li>center coords for EPSG:{{item['code']}} with EPSG:{{default_trans['code']}} transformation  = {{trans_coords[0]}}, {{trans_coords[1]}}, {{trans_coords[2]}}</li>
%end
%end

%if item['wkt'] and item['bbox'] and trans_coords:

<form action= "{{url_format}}/coordinates/" method="get">
  	from WGS 84 to {{item['name']}} <input type="text" name="wgs" placeholder="{{center[0]}} {{center[1]}}" style="width: 200px"/>
		<input type="submit" value="TRANSFORM">
</form>

<form action= "{{url_format}}/coordinates/" method="get">
  	from {{item['name']}} to WGS 84 <input type="text" name="other" placeholder="{{trans_coords[0]}} {{trans_coords[1]}}" style="width: 200px"/>
		<input type="submit" value="TRANSFORM">
</form>
%end
</body>
</html>
