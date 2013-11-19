
<html>
<head>
	<title>epsg.io</title>

</head>
<body>
<h1>TRY TO FIND YOUR PROJECTION</h1>
<form action= "/epsg" method="post">
Query on EPSG (code, name, type, area): <input type="text" name="fulltext"><br>
<input type="submit" value="submit">
<input type="checkbox" value="1" name="valid" checked>
<select name="type">
	<option value = "*">All</option>
	
	<option value = "projected">Projected</option>
	<option value = '"geographic 2D"'>Geographic 2D</option>
	<option value = '"geographic 3D"'>Geographic 3D</option>
	<option value = "geocentric">Geocentric</option>
		
</select>
</form>
</body>
</html>
