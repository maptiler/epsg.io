<html>
<head>
	<title>Find coordinate systems for spatial reference worldwide</title>

</head>
<body>

<a href=/about>About</a> &nbsp; &nbsp; <a href=/>Search</a>

<h1>EPSG.io</h1>

<h2>Find coordinate systems for spatial reference worldwide</h2>
<hr>
{{item}}
<h3>{{item[0]['kind']}}<h3>
<h1>EPSG:{{item[0]['code']}} {{item[0]['name']}} {{item[0]['alt_name']}}</h1>
<!-- Not show number of results if it just one-->
%if num_results != 1:
	<b>Transformation</b> ({{num_results}})
	%for r in trans:
		%if r['me'] == 1:
			<li> {{r['area']}}
			%if 'accuracy' in r:
				, accuracy {{r['accuracy']}}
			%end
		
			%if r['code_trans'] != 0:
				code {{r['code_trans']}} 
			%end
			
			%if r['trans_alt_name']:
				({{r['trans_alt_name'][0]}})
			%end

			
			{{r['default']}}
			
			</li>
		%else:
			<li><a href="/{{r['link']}}/">{{r['area']}}, accuracy {{r['accuracy']}} code {{r['code_trans']}} 
				%if r['trans_alt_name']:
				 	({{r['trans_alt_name'][0]}})
				%end

				{{r['default']}}
				 </a></li>
		%end
	%end
%end
</br>
<li>Scope: {{item[0]['scope']}}</li>
<li>Area of use: <a href="{{url_area}}">{{item[0]['area']}}</a></li>
<li>Remarks: {{item[0]['remarks']}}</li>
<li>Information source: {{item[0]['information_source']}}</li>
<li>Revision date: {{item[0]['revision_date']}}</li>
%if 'method' in item:
	<li>Method: {{item[0]['method']}}</li>
%end

%if item[0]['concatop']:
	<li>steps of transformation : {{item[0]['concatop'][0]}}</li>
%end

%if 'datum_code' in item[0]:
	<li>Datum: <a href="/{{item[0]['datum_code']}}-datum/">{{item[0]['datum_code']}}-datum</a>
%end

%if item[0]['uom_code']:
	<li>Unit: <a href="/{{item[0]['uom_code']}}-units/">{{item[0]['uom']}}</a></li>
%end

%if item[0]['children_code']:
	<li>Coordinate system: <a href="/{{item[0]['children_code']}}-coordsys/">{{item[0]['children_code']}}</a></li>
	

%if item[0]['wkt'] != "":
	<ul>
		<li><a href="/{{item[0]['code']}}-{{item[0]['code_trans']}}/prettywkt">PrettyWKT</a>
		<li><a href="/{{item[0]['code']}}-{{item[0]['code_trans']}}/esriwkt">ESRI WKT</a>
		<li><a href="/{{item[0]['code']}}-{{item[0]['code_trans']}}/proj4">Proj4</a>
	</ul>
%end
		
</body>
</html>
