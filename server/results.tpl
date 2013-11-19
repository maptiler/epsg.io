<h1>The query is: {{query}}</h1>
</br>
Number of results : {{num_results}}
</br>
<a href= / >Back to the new query</a>

%for r in result:
	<ul><b>EPSG:{{r['code']}}</b> , with name: {{r['name']}}
		<ul>
			<li>
				Area of use: {{r['area']}}
			</li>

			<li>
				Transformation: {{r['trans']}}
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
				Type: {{r['type']}}
			</li>
			<li>
				Status: {{r['status']}}
			</li>
			
		</ul>	
	</ul>
%end
