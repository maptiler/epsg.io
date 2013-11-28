<html>
<head>
	<title>EPSG.io - Coordinate systems for spatial reference worldwide</title>

</head>
<body><h1>EPSG.io</h1> <h2>Coordinate systems for spatial reference worldwide</h2>
</br>
Number of results : {{num_results}}
</br>
<a href= / >Back to the new query</a>
</br>
</br>
%for key, value in groups.iteritems(): 
	%if status == None:
	<li>Group: <a href= /?q={{query}}&kind="{{key}}" >{{key}}</a> : {{value}}</li>
	%else:
	<li>Group: <a href= /?q={{query}}&valid={{status}}&kind="{{key}}" >{{key}}</a> : {{value}}</li>
	%end

%end

%for r in result:
	<ul><h2>EPSG:{{r['code']}} &nbsp;&nbsp; {{r['name']}}</h2>
		<ul>
			%if r['code_trans'] != 0:
			<li>
				
					<h3>Transformation: EPSG:{{r['code_trans']}} &nbsp;&nbsp; {{r['trans']}}</h3>
					<ul>
						Remarks: {{r['trans_remarks']}}
					</ul>
				%else:
					%pass
			</li>
			%end	
			
			<li>
				<h4>Area of use: {{r['area']}} </h4>
			</li>

			<li>
			%if r['primary'] == 0:
				<a href= /{{r['code']}}-{{r['code_trans']}}/ >Detail information</a>
			%else:
				<a href= /{{r['code']}}/ >Detail information</a>
			%end
				
			</li>

			
		</ul>	
	</ul>
%end

<hr>


</body>
</html>