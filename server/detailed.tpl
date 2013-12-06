<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<link rel="stylesheet" type="text/css" href="/css/style.css">

	<title>{{title}}</title>

</head>
<body>

<div id ="searchabout"><a href=/about>About</a> &nbsp; &nbsp; <a href=/>Search</a></div>

<h1>EPSG.io</h1>

<h2>Find coordinate systems for spatial reference worldwide</h2>
<hr>
<h3>{{item['kind']}}</h3>
<div id="topic">EPSG:{{item['code']}} {{item['name']}} </div>
</br

<b>Transformation</b> ({{num_results}})
%for r in trans:
	%if r['link'] == "" and r['status'] == item['status']:
		<div id="me">
			</br>
			<li> {{r['area_trans']}}
		
		%if 'accuracy' in r:
			, accuracy {{r['accuracy']}}
		%end
		
		%if r['code_trans'] != 0:
			code {{r['code_trans']}} 
		%end
		%if r['default']== True:
			DEFAULT
		%end
			</li>
		</div>
		
		
		</br></br>
		
	
		
	%elif r['status'] == item['status']:
		<li><a href="/{{r['link']}}/" title = "{{r['trans_remarks']}}">{{r['area_trans']}}, accuracy 
			{{r['accuracy']}} code {{r['code_trans']}} 
			%if r['default'] == True:
				DEFAULT
			%end
			</a>
			</br></br>
		</li>
	%end
%end

</br>


For transformation: {{item['code_trans']}}

<li>Method: <a href="{{url_method}}">{{item['method']}}</a></li>
<li>Remarks: {{item['trans_remarks']}}</li>
<li>Area of use: <a href="{{url_area_trans}}">{{item['area_trans']}}</a></li>

%if item['concatop']:
	<li>steps of transformation : {{item['concatop'][0]}}</li>
%end
%if 'datum_code' in item:
	<li>Datum: <a href="/{{item['datum_code']}}-datum/">{{item['datum_code']}}-datum</a>
%end
</br>
</br>
For EPSG: {{item['code']}}
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

<div id="formats">
%if item['wkt']:

<ul>
	%for f in formats:
	<li><a href="{{url_format}}/{{f}}">{{f}}</a></li>
	%end
</ul>


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

</body>
</html>
