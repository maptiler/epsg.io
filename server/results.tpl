<html>
<head>
	<title>EPSG.io - Coordinate systems for spatial reference worldwide</title>

</head>

<body>
<a href=/about>About</a> &nbsp; &nbsp; <a href=/>Search</a>
<h1>EPSG.io</h1>
<h2>Coordinate systems for spatial reference worldwide</h2>

Number of results : {{num_results}}
</br>
%for key, value in groups.iteritems(): 
	<li>
	%if status == None:
		<a href= /?q={{url_query}}&kind="{{key}}" >{{key}}</a> : {{value}}
	%else:
		<a href= /?q={{url_query}}&valid={{status}}&kind="{{key}}" >{{key}}</a> : {{value}}
	%end
	</li>
%end

%for r in result:
	<ul>
		<b> <a href="/{{r['link']}}/">{{r['r']['name']}} 
			%if r['r']['alt_name']:
				({{r['r']['alt_name']}})
			%end
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
		%if r['r']['area']:
			%if r['r']['accuracy'] == "":
				<b>Area of use: {{r['r']['area']}} (accuracy: unknown)</b>
			%else:	
				<b>Area of use: {{r['r']['area']}} (accuracy: {{r['r']['accuracy']}})</b>
			%end
		%end	
	</ul>
%end
</body>
</html>