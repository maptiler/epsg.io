<html>
<head>
	<title>detailed</title>

</head>
<body>
	
%for r in result:
	<ul><h2>EPSG:{{r['code']}} &nbsp;&nbsp; {{r['name']}}</h2>
		<ul>
			<li>
				<h3>Transformation: EPSG:{{r['code_trans']}} &nbsp;&nbsp; {{r['trans']}}</h3>
				<ul>
					Remarks: {{r['trans_remarks']}}
				</ul>	
			</li>
			<li>
				<h4>Area of use: {{r['area']}} </h4>
			</li>
			<li>
				Scope: {{r['scope']}}
			</li>
			<li>
				Remarks: {{r['remarks']}}
			</li>	
			<li>
				Information: {{r['information_source']}}
			</li>
			<li>
				Revision date: {{r['revision_date']}}
			</li>
			<li>
				Type: {{r['kind']}}
			</li>
			<li>
				wkt: {{r['wkt']}}
			</li>
			
			<ul>
				<li><a href="prettywkt">PrettyWKT</a>
				<li><a href="esriwkt">ESRI WKT</a>
				<li><a href="proj4">Proj4</a>
			</ul>
			<li>
				popularity: {{r['popularity']}}
			</li>
			%"""
		%if r['datum_code'] and r['datum_name'] :  	
			<li>
				<ul>
					<h3>Datum</h3> {{r['datum_code']}} &nbsp;&nbsp;{{r['datum_name']}}
					%if r['ellipsoid_name']:
						<h3>Ellipsoid</h3>{{r['ellipsoid_code']}} &nbsp;&nbsp; {{r['ellipsoid_name']}}
						
					%end
				</ul>
				
			</li>
		%end
		%"""
		</ul>	
	
	</ul>
	%for r in result:
		<li>{{r}}</li>
	%end
<hr>

%end

</body>
</html>
