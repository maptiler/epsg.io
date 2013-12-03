<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">

<html lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>detailed_word</title>
	<meta name="generator" content="TextMate http://macromates.com/">
	<meta name="author" content="Tomas Pohanka">
	<!-- Date: 2013-11-30 -->
</head>
<body>

	<a href=/about>About</a> &nbsp; &nbsp; <a href=/>Search</a>

	<h1>EPSG.io</h1>

	<h2>Find coordinate systems for spatial reference worldwide</h2>
	<hr>

	<h3>{{item[0]['kind']}}</h3>
	EPSG:{{item[0]['code']}}
	<h1>{{item[0]['name']}}
		%if item[0]['alt_name']:
			({{item[0]['alt_name']}})
		%end 
	</h1>
</br>
generally:
<li>Remarks: {{item[0]['remarks']}}</li>
<li>Information source: {{item[0]['information_source']}}</li>
<li>Revision date: {{item[0]['revision_date']}}</li>
<li>Data source: {{item[0]['data_source']}}</li>
</br>


</br>
Specific:
%if item[0]['scope']:
	<li>Scope: {{item[0]['scope']}}</li>
%end
%if item[0]['area']:
	<li>Area of use: <a href="{{detail[0]['url_area']}}"> {{item[0]['area']}}</a></li>
%end


%if item[0]['target_uom']: 
	<li>Target uom: <a href="{{detail[0]['url_uom']}}">{{item[0]['target_uom']}}</a></li>	
%end

%if item[0]['uom_code']:
	<li>Unit: <a href="/{{item[0]['uom_code']}}-units/">{{item[0]['uom']}}</a></li>
%end



%if item[0]['files']:
	<li>File: {{item[0]['files']}}</li>
%end


%if item[0]['orientation']:
	<li>Orientation: {{item[0]['orientation']}}</li>
%end

%if item[0]['abbreviation']:
	<li>Abrev: {{item[0]['abbreviation']}}</li>
%end

%if item[0]['order']:
	<li>Axis order: {{item[0]['order']}}.</li>
%end
%if item[0]['description']:
	<li>description: {{item[0]['description']}}</li>
%end



%if item[0]['greenwich_longitude']:
	<li>Greenwich longitude difference: {{item[0]['greenwich_longitude']}}</li>
%end



%if detail[0]['url_prime']:
	<li>Prime meridian: <a href="/{{detail[0]['url_prime']}}">{{item[0]['prime_meridian']}}-primemeridian</a></li>
%end
%if detail[0]['url_children']:
	<li>Link to : <a href="/{{detail[0]['url_children']}}">{{detail[0]['url_children']}} </a></li>
%end
%if detail[0]['url_axis']:
	<li>Link to axis : <a href="/{{detail[0]['url_axis'][0]}}/">{{detail[0]['url_axis'][0]}} </a></li>
	<li>Link to axis : <a href="/{{detail[0]['url_axis'][1]}}/">{{detail[0]['url_axis'][1]}} </a></li>
%end


</body>
</html>
