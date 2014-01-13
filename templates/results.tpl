<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"  lang="en" xml:lang="en">
  <head>  
    <meta charset="utf-8"/>
    <title>EPSG.io</title>
    <meta content="width=device-width, initial-scale=1, maximum-scale=1" name="viewport" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="description" content="EPSG.io" />
    <meta name="keywords" content="EPSG.io" />
    <meta name="robots" content="ALL,FOLLOW" />
    <link rel="stylesheet" href="/css/main.css" type="text/css" />
    <link rel="shortcut icon" href="http://epsg.io/favicon.ico" />

  </head>
  <body id="resultspage" data-role="page">
    <div id="head">
      <p id="logo-container">
        <a href="/" title=""><span>Epsg.io</span> Coordinate systems worldwide</a>
      </p>
      <ul id="menu-top">
        <li><a href="/about" title="">About</a></li>
      </ul>
    </div>
    <div id="layout-container">
      <div id="search-container">
        <form action="/" method="get">
          <p><input type="search" name="q" value="{{query}}" /> <input type="submit" name="" value="search" /></p>
        </form>
      </div>
      <h1>Find a coordinate system and get coordinates through a map.</h1>
      <p>
%if deprecated == 1:
          Found {{num_results}} deprecated records (in {{elapsed}} seconds)
%else:  
          Found {{num_results}} valid records (in {{elapsed}} seconds)
%end
      </p>
      
      <div id="result-content-container">
        <div id="results-container">
          <ul class="results">
%for r in result:
            <li>
              <h2><a href="/{{r['link']}}" title="">{{r['r']['name']}}</a></h2>
              <p>
                EPSG:{{r['r']['code']}}
  %if r['r']['code_trans'] != 0 and r['r']['primary'] == 1:
                  with transformation: {{r['r']['code_trans']}} (default)
  %elif r['r']['code_trans'] == 0 and r['r']['primary'] == 1:
                  (default)
  %elif r['r']['code_trans'] != 0:
                  with transformation: {{r['r']['code_trans']}}
  %end
              </p>
              <p class="area">
  %if r['r']['area_trans']:
    %if r['r']['accuracy'] == "":
                    Area of use: {{r['r']['area_trans']}} (accuracy: unknown)
    %else:  
                    Area of use: {{r['r']['area_trans']}} (accuracy: {{r['r']['accuracy']}})
    %end
  %end
              </p>
            </li>
%end
          </ul>
          
          <ul class="paginator">
  
  
%if (pagenum-1) > 0:
              <li class="prev"><a href="/?q={{query}}&page={{pagenum-1}}" title="">Prev</a></li>
%end

%for i in paging:
  %if i == pagenum:
              <li><span>{{ i }}</span></li>
  %else:
              <li><a href="/?q={{query}}&page={{i}}" title="">{{i}}</a></li>
  %end
%end

%if (pagenum+1) in paging:
              <li class="next"><a href="/?q={{query}}&page={{pagenum+1}}" title="">Next</a></li>
%end
          </ul>
        </div>
        <div id="side-container">
          <h3>Alternatives search</h3>
          <ul id="alt-search">
%for i in range(0,len(facets_list)):
  %if facets_list[i][4] != 0:
            

            <li class="selected">{{!facets_list[i][2]}}<a href="{{facets_list[i][5]}}" title="">{{facets_list[i][3]}} ({{facets_list[i][4]}})</a>
  %end
%end
            </li>
%for key,value in status_groups.iteritems():
            <li class="last">
  %if key == "f":
              <a href="{{url_facet_statquery}}" title="">Show invalid ({{value}})</a>
  %elif key == "t":
              <a href="{{url_facet_statquery}}" title="">Show deprecated ({{value}})</a>
            </li>
  %end
%end            
          </ul>
        </div>
      </div>
      <div id="foot">
        <p id="mzk-logo">
          <a href="http://www.mzk.cz/" title=""><img src="./img/hzk-logo.png" alt="" /></a>
        </p>
        <p>Find a coordinate system and get position on a map.</p>
        <p id="copyright">Copyright &copy; 2014</p>
      </div>
    </div>
  </body>
</html>
