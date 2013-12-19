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

</br>
<form action= "/{{url_coords}}/coordinates/" method="get">
From WGS84 to {{resultcrs['name']}} <input type="text" name="wgs" placeholder="{{coord_lat}} {{coord_lon}}" style="width: 200px" value="{{coord_lat}} {{coord_lon}}"/>
		<input type="submit" value="Transform coordinates">
</form>

</br>
</br>

<form action= "/{{url_coords}}/coordinates/" method="get">
From {{resultcrs['name']}} to WGS84	<input type="text" name="other" placeholder="{{coord_lat_other}} {{coord_lon_other}}" style="width: 200px" value="{{coord_lat_other}} {{coord_lon_other}}"/>
		<input type="submit" value="Transform coordinates">
</form>
</br>
</br>
%if trans_wgs:
	transformation from wgs to {{resultcrs['name']}} = {{trans_wgs[0]}}, {{trans_wgs[1]}}, {{trans_wgs[2]}}</li>
	<div id=image>
	<img src="/css/crosshair.png" id="crosshair" alt=""/>
	<img src="https://maps.googleapis.com/maps/api/staticmap?size=235x190&scale=2&zoom=10&sensor=false&visual_refresh=true&center={{coord_lat}},{{coord_lon}}&path=color:0xff0000ff|fillcolor:0xff000022|weight:2" alt="SimpleMap" height="190" width="235">
	</div>
%elif trans_other:
	transformation from {{resultcrs['name']}} to wgs= {{trans_other[0]}}, {{trans_other[1]}}, {{trans_other[2]}}</li>
	<div id=image>
	<img src="/css/crosshair.png" id="crosshair" alt=""/>
	<img src="https://maps.googleapis.com/maps/api/staticmap?size=235x190&scale=2&zoom=10&sensor=false&visual_refresh=true&center={{trans_other[0]}},{{trans_other[1]}}&path=color:0xff0000ff|fillcolor:0xff000022|weight:2" alt="SimpleMap" height="190" width="235">
	</div>
%else:
<b>!!!INSERT COORDINATES!!!</b>
%end
</br>
</br>
<a href="/{{url_coords}}/">Back to detail </a>
</body>
</html>