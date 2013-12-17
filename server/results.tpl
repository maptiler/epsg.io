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
  <input type="submit" value="SEARCH">
</form>


%if deprecated == 1:
	Found {{num_results}} deprecated records ({{elapsed}} seconds)
%else:	
Found {{num_results}} valid records ({{elapsed}} seconds)
%end


<div id="category">
Results in other categories:
<ul>
%for i in range(0,len(facets_list)):
%if facets_list[i][4] != 0:
	<li>{{!facets_list[i][2]}}<a href="{{facets_list[i][5]}}">{{facets_list[i][3]}}</a> : {{facets_list[i][4]}}</li>
%end
%end

<hr>

%for key,value in status_groups.iteritems():
<li>
%if key == "f":
	<a href="{{url_facet_statquery}}">Show valid</a> : {{value}}</li>
	
%elif key == "t":
	<a href="{{url_facet_statquery}}">Show deprecated</a> : {{value}}</li>

%end
</ul>
%end
</div>

<hr>

%for r in result:
	
		<b> <a href="/{{r['link']}}/">{{r['r']['name']}}</a></b>
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


%if (pagenum-1) > 0:
  <a href="/?q={{query}}&page={{pagenum-1}}">Prev</a>
%end

%for i in paging:
	%if i == pagenum:
	{{ i }}
	%else:
	<a href="/?q={{query}}&page={{i}}">{{i}}</a>
	%end
%end

%if (pagenum+1) in paging:
  <a href="/?q={{query}}&page={{pagenum+1}}">Next</a>
%end

</body>
</html>