<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<link rel="stylesheet" type="text/css" href="/css/style.css">
	<title>EPSG.io - Coordinate systems for spatial reference worldwide</title>

</head>

<body>
<div id ="mysearchabout"><a href=/about>About</a> &nbsp; &nbsp; <a href=/>Search</a></div>
<h1>EPSG.io</h1>
<h2>Coordinate systems for spatial reference worldwide</h2>

<form action= "/" method="get">
  		<div id="mysearchbox"><input type="text" name="q" placeholder="country, code or name of a coordinate system" style="width: 300px" value="{{query}}"/></div>
		<input type="checkbox" value="0" name="valid" checked> Valid
		<select name="kind">
				<option value = "CRS-*"selected>Coordinate reference systems</option>
		</select>
	<input type="text" name="page" value = "{{pagenum}}">
	<input type="text" name="perpage" value = "{{pagelen}}">
  <input type="submit" value="Submit form">
</form>

%if status == "1":
	Found {{num_results}} deprecated records in category {{category}} 
	, ({{res_facets.runtime}} seconds)
%else:	
Found {{num_results}} valid records in category {{category}}
, ({{elapsed}} seconds)
%end

<div id="category">
Results in other categories:
<ul>
%for key,value in sorted(groups.iteritems()):	
	<li>
	%if status == None:
		<a href= /?q={{url_query}}&kind="{{key}}" >{{key}}</a> : 
		 {{value}}

	%else:
		<a href= /?q={{url_query}}&valid={{status}}&kind="{{key}}" >{{key}}</a> : {{value}}
	%end
	</li>	
%end
<hr>
%for key,value in status_groups.iteritems():
<li>
%if key == "f":
	<a href="/?q={{url_query}}&valid=0&kind={{category}}">Show valid</a> : {{value}}
	
%else:
<a href="/?q={{url_query}}&valid=1&kind={{category}}">Show invalid</a> : {{value}}
	
</li>
%end
</ul>
</div>
<hr>
%for r in result:
	
		<b> <a href="/{{r['link']}}/">{{r['r']['name']}} 
			%#if r['r']['alt_name']:
			%#	({{r['r']['alt_name']}})
			%#end
		</a></b>
		</br>
		EPSG:{{r['r']['code']}}
	
		%if r['r']['code_trans'] != 0 and r['r']['primary'] == 1:
			with transformation: {{r['r']['code_trans']}} (default)
		%elif r['r']['code_trans'] == 0 and r['r']['primary'] == 1:
			(default)
		%elif r['r']['code_trans'] != 0:
			with transformation: {{r['r']['code_trans']}}

		%end
		</br>
		%if r['r']['area_trans']:
			%if r['r']['accuracy'] == "":
				<b>Area of use: {{r['r']['area_trans']}} (accuracy: unknown)</b>
			%else:	
				<b>Area of use: {{r['r']['area_trans']}} (accuracy: {{r['r']['accuracy']}})</b>
			%end
		
		%end
</br>
</br>	
%end
</body>
</html>