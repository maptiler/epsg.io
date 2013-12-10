<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
	<link rel="stylesheet" type="text/css" href="/css/style.css">
	<title>{{item['kind']}}:{{item['code']}}</title>
</head>
<body>

	<div id ="mysearchabout"><a href=/about>About</a> &nbsp; &nbsp; <a href=/>Search</a></div>

	<h1>EPSG.io</h1>

	<h2>Find coordinate systems for spatial reference worldwide</h2>
	<hr>

	<h3>{{item['kind']}}</h3>
	EPSG:{{item['code']}}
	<div id="topic">{{item['name']}}
		%if item['alt_name']:
			({{item['alt_name']}})
		%end 
	</div>
</br>
generally:
<li>Remarks: {{item['remarks']}}</li>
<li>Information source: {{item['information_source']}}</li>
<li>Revision date: {{item['revision_date']}}</li>
<li>Data source: {{item['data_source']}}</li>
</br>


</br>
Specific:
%if item['scope']:
	<li>Scope: {{item['scope']}}</li>
%end
%if item['area']:
	<li>Area of use: <a href="{{detail[0]['url_area']}}"> {{item['area']}}</a></li>
%end


%if item['target_uom']: 
	<li>Target uom: <a href="{{detail[0]['url_uom']}}">{{item['target_uom']}}</a></li>	
%end

%if item['uom_code']:
	<li>Unit: <a href="/{{item['uom_code']}}-units/">{{item['uom']}}</a></li>
%end



%if item['files']:
	<li>File: {{item['files']}}</li>
%end


%if item['orientation']:
	<li>Orientation: {{item['orientation']}}</li>
%end

%if item['abbreviation']:
	<li>Abrev: {{item['abbreviation']}}</li>
%end

%if item['order']:
	<li>Axis order: {{item['order']}}.</li>
%end
%if item['description']:
	<li>description: {{item['description']}}</li>
%end



%if item['greenwich_longitude']:
	<li>Greenwich longitude difference: {{item['greenwich_longitude']}}</li>
%end



%if detail[0]['url_prime']:
	<li>Prime meridian: <a href="/{{detail[0]['url_prime']}}">{{item['prime_meridian']}}-primemeridian</a></li>
%end
%if detail[0]['url_children']:
	<li>Link to : <a href="/{{detail[0]['url_children']}}">{{detail[0]['url_children']}} </a></li>
%end
%if detail[0]['url_axis']:
	%for a in detail[0]['url_axis']:
		<li>Link to axis : <a href="/{{a}}/">{{a}} </a></li>
	%end
%end


</body>
</html>
