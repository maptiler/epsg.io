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
  <body id="detailpage" data-role="page">
    <div id="head">
      <p id="logo-container">
        <a href="/" title=""><span>Epsg.io</span> Coordinate systems worldwide</a>
      </p>
      <ul id="menu-top">
        <li><a href="/about" title="">About</a></li>
      </ul>
    </div>
    <div id="layout-container">
      
      <h1>EPSG:{{item['code']}}</h1>
      <p>
%for i in range(0,len(facets_list)):
  %if facets_list[i][0] == item['kind']:
    {{facets_list[i][3]}} - {{facets_list[i][1]}}
  %end
%end
      </p>
      
      <h2>{{item['name']}}</h2>
      
      <p>
        Scope: {{item['scope']}}<br />
%if detail:
        Area of use: <a href="{{detail[0]['url_area']}}"> {{item['area']}}</a><br />
%else:
        Area of use: <a href="{{url_area}}">{{item['area']}}</a><br />
%end
        Remarks: {{item['remarks']}}<br />
        Information source: {{item['information_source']}}<br />
        Revision date: {{item['revision_date']}}<br />
%if item['concatop']:
        Steps of transformation: {{item['concatop']}}<br />
%end
%if nadgrid:
        NadGrid file: {{nadgrid}}<br />
%end
%if 'source_geogcrs' in item:
  %if item['source_geogcrs']:
        Geodetic coordinate reference system: <a href="/{{item['source_geogcrs']}}/" title="">{{item['source_geogcrs']}}</a><br />

%end
%end
%if 'datum_code' in item:
  %if item['datum_code'] != 0 :
        Datum: <a href="/{{item['datum_code']}}-datum/" title="">{{item['datum_code']}}-datum</a><br />
  %end
%end
%if not detail:
%if 'children_code' in item:
  %if item['children_code'] != 0 :
        Coordinate System: <a href="/{{item['children_code']}}-coordsys/" title="">{{item['children_code']}}-coordsys</a><br />
  %end
%end
%end

%if item['target_uom']:
        Target uom: <a href="{{detail[0]['url_uom']}}">{{item['target_uom']}}</a><br />
%end

%if item['uom_code']:
        Unit: <a href="/{{item['uom_code']}}-units/">{{item['uom']}}</a><br />
%end

%if item['files']:
        File: {{item['files']}}<br />
%end

%if item['orientation']:
        Orientation: {{item['orientation']}}<br />
%end

%if item['abbreviation']:
        Abrev: {{item['abbreviation']}}<br />
%end

%if item['order']:
        Axis order: {{item['order']}}.<br />
%end
%if item['description']:
        Description: {{item['description']}}<br />
%end

%if item['greenwich_longitude']:
        Greenwich longitude difference: {{item['greenwich_longitude']}}<br />
%end
%if detail != []:
%if detail[0]['url_prime']:
        Prime meridian: <a href="/{{detail[0]['url_prime']}}">{{item['prime_meridian']}}-primemeridian</a><br />
%end
%end
%if detail != []:
%if detail[0]['url_children']:
        Link to : <a href="/{{detail[0]['url_children']}}">{{detail[0]['url_children']}}</a><br />
%end
%end
%if detail != []:
%if detail[0]['url_axis']:
        
  %for a in detail[0]['url_axis']:
        Link to axis : <a href="/{{a}}/">{{a}}</a><br />
  %end
        
%end
%end
      </p>
      
      <div id="detail-content-container">
        <div class="map-container">
%if center:
          <div id="mini-map">
            <img src="/img/epsg-target-small.png" id="crosshair" alt="" />
            <img src="https://maps.googleapis.com/maps/api/staticmap?size=235x190&scale=2&sensor=false&visual_refresh=true&center={{center[0]}},{{center[1]}}&path=color:0xff0000ff|fillcolor:0xff000022|weight:2|{{g_coords}}" alt="SimpleMap" height="190" width="235">
%end
          </div>
%if trans_lat and trans_lon:
          <p>
            Center coordinates<br />
            <span>{{trans_lat}}</span>  <span>{{trans_lon}}</span>
          </p>
%end
        </div>
        <div class="location-data-container">
%if trans:
%for r in trans:
          <h2>
  %if r['link'] == "" and r['area_trans']:
              {{r['area_trans']}} <br />
    %if r['code_trans'] != 0:
              code {{r['code_trans']}} 
    %end
    %if r['default'] == True:
              DEFAULT
    %end    
          </h2>
              
    %if r['accuracy']:
              Accuracy {{r['accuracy']}}m 
    %end

  %end
%end
%end
%if center and trans_lat and trans_lon:
          <p class="btn-link-container">
            <a href="{{url_format}}/coordinates/?wgs={{center[0]}}%20{{center[1]}}" title=""><i></i>Get position on a map</a>
          </p>
%end
%if trans and default_trans:
          <p>
            Method: {{default_trans['method']}}<br />
            Area of use: <a href="{{url_area_trans}}" title-"">{{default_trans['area']}}</a><br />
            Remarks: {{default_trans['remarks']}}<br />
            Information source: <br />
            Revision date: {{default_trans['revision_date']}}<br />
%if url_concatop != []:
            Steps of transformation: 
  %for url in url_concatop:
            <a href="{{url}}" title="">{{url}}</a>
  %end
%end
          </p>
%end
        </div>
%if trans:
        <div class="transformations-container">
          <h3>Available transformations:</h3>
          <ul>
% i = 0
%for r in trans:
  %if r['link'] == "" and r['deprecated'] == 0 and r['area_trans']:
            <li> {{r['area_trans']}}
    %if r['accuracy']:
            , accuracy {{r['accuracy']}}m, 
    %end
    %if r['code_trans'] != 0:
            code {{r['code_trans']}} 
    %end
    %if r['default'] == True:
            DEFAULT
    %end
    % i +=1
            </li>
  %elif r['deprecated'] == 0 and r['area_trans']:
            <li>
            <a href="/{{r['link']}}/" title = "{{r['trans_remarks']}}">{{r['area_trans']}}, accuracy 
            {{r['accuracy']}}m, code {{r['code_trans']}} 
    %if r['default'] == True:
            DEFAULT
    %end
            </a>
    %i+=1
            </li>

  %end
%end

            <a href="#" onClick="javascript:document.getElementById('trans_deprecated').style.display='block';return false">Show deprecated transformations</a>
            <div id="trans_deprecated" style="display:none">
%a = 0
%for r in trans:
  %if r['deprecated'] == 1:
    %if r['link'] == "":
            <li>{{r['area_trans']}}, accuracy {{r['accuracy']}}m, code {{r['code_trans']}} DEPRECATED
      %if r['default'] == True:
          DEFAULT
      %end
            </li>
    %else:
            <li>
            <a href="/{{r['link']}}/" title = "{{r['trans_remarks']}}">{{r['area_trans']}}, accuracy {{r['accuracy']}}m,  code {{r['code_trans']}} DEPRECATED
      %if r['default'] == True:
          DEFAULT
      %end
            </a>
            </li>
    %end
    %a+=1
  %end
%end
          </ul>
        </div>
%end
      </div>
%if url_format and error_code == 0:
      <div id="edit-box-container">
        <div id="eb-menu-container">
          <h4>Export</h4>
          <ul id="eb-menu">
            <li><a class="selected" href="" title="" onClick="javascript:document.getElementById('code-definition-container-html').style.display='block'; return false">Well Known Text as HTML<i></i></a></li>
            <li><a href="" title="" onClick="javascript:document.getElementById('code-definition-container-prettywkt').style.display='block'; return false">PrettyWKT <i></i></a></li>
            <li><a href="" title="" onClick="javascript:document.getElementById('code-definition-container-esriwkt').style.display='block'; return false">ESRI WKT <i></i></a></li>
            <li><a href="{{url_format}}/prj" title="">Download file {{item['code']}}.prj <i></i></a></li>
            <li><a href="" title="" onClick="javascript:document.getElementById('code-definition-container-proj4').style.display='block'; return false">PROJ.4 <i></i></a></li>
            <li><a href="" title="" onClick="javascript:document.getElementById('code-definition-container-gml').style.display='block'; return false">OGC GML <i></i></a></li>
            <li><a href="" title="" onClick="javascript:document.getElementById('code-definition-container-geoserver').style.display='block'; return false">GeoServer <i></i></a></li>
            <li><a href="" title="" onClick="javascript:document.getElementById('code-definition-container-mapfile').style.display='block'; return false">MAPfile <i></i></a></li>
            <li><a href="" title="" onClick="javascript:document.getElementById('code-definition-container-mapserverpython').style.display='block'; return false">MapSever - Python <i></i></a></li>
            <li><a href="" title="" onClick="javascript:document.getElementById('code-definition-container-mapnik').style.display='block'; return false">mapnik <i></i></a></li>
            <li><a href="" title="" onClick="javascript:document.getElementById('code-definition-container-mapnikpython').style.display='block'; return false">mapnik - Python <i></i></a></li>
            <li><a href="" title="" onClick="javascript:document.getElementById('code-definition-container-postgis').style.display='block'; return false">PostGIS <i></i></a></li>
            <li><a href="" title="" onClick="javascript:document.getElementById('code-definition-container-json').style.display='block'; return false">JSON <i></i></a></li>
            <li><a href="" title="" onClick="javascript:document.getElementById('code-definition-container-ogcwkt').style.display='block'; return false">OGC WKT <i></i></a></li>
            <li><a href="" title="" onClick="javascript:document.getElementById('code-definition-container-usgs').style.display='block'; return false">USGS <i></i></a></li>
          </ul>
        </div>
        <div class="code-definition-container" id="code-html">
          <p>Definition: Well Known Text as HTML</p>
          <ul>
            <li><a href="{{url_format}}/html" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{!export_html}}
          </div>
        </div>
        <div class="code-definition-container" id="code-prettywkt">
          <p>Definition: PrettyWKT</p>
          <ul>
            <li><a href="{{url_format}}/prettywkt" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{!export['prettywkt']}}
          </div>
        </div>
        <div class="code-definition-container" id="code-esriwkt">
          <p>Definition: ESRI WKT</p>
          <ul>
            <li><a href="{{url_format}}/esriwkt" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{export['esriwkt']}}
            
          </div>
        </div>
        <div class="code-definition-container" id="code-prj">
          <p>Definition: Download file {{item['code']}}.prj</p>          
          <ul>
            <li><a href="{{url_format}}/prj" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{!export}}
          </div>
        </div>
        <div class="code-definition-container-proj4">
          <p>Definition: PROJ.4</p>
          <ul id="cd-tabs">
            <li><a href="{{url_format}}/proj4" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{export['proj4']}}
          </div>
        </div>
        <div class="code-definition-container-gml">
          <p>Definition: OGC GML</p>
          <ul id="cd-tabs">
            <li><a href="{{url_format}}/gml" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{export['gml']}}
          </div>
        </div>
        <div class="code-definition-container-geoserver">
          <p>Definition: GeoServer</p>
          <ul id="cd-tabs">
            <li><a href="{{url_format}}/geoserver" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{export['geoserver']}}
          </div>
        </div>
        <div class="code-definition-container-mapfile">
          <p>Definition: MAPfile</p>
          <ul class="cd-tabs">
            <li><a href="{{url_format}}/mapfile" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{!export['mapfile']}}
          </div>
        </div>
        <div class="code-definition-container-mapserverpython">
          <p>Definition: MapSever - Python</p>
          <ul id="cd-tabs">
            <li><a href="{{url_format}}/mapserverpython" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{!export['mapserverpython']}}
          </div>
        </div>
        <div class="code-definition-container-mapnik">
          <p>Definition: mapnik</p>
          <ul id="cd-tabs">
            <li><a href="{{url_format}}/mapnik" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{!export['mapnik']}}
          </div>
        </div>
        <div class="code-definition-container-mapnikpython">
          <p>Definition: mapnik - Python</p>
          <ul id="cd-tabs">
            <li><a href="{{url_format}}/mapnikpython" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{!export['mapnikpython']}}
          </div>
        </div>
        <div class="code-definition-container-postgis">
          <p>Definition: PostGIS</p>
          <ul id="cd-tabs">
            <li><a href="{{url_format}}/postgis" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{!export['postgis']}}
          </div>
        </div>
        <div class="code-definition-container-json">
          <p>Definition: JSON</p>
          <ul id="cd-tabs">
            <li><a href="{{url_format}}/json" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{!export['json']}}
          </div>
        </div>
        <div class="code-definition-container-ogcwkt">
          <p>Definition: OGC WKT</p>
          <ul id="cd-tabs">
            <li><a href="{{url_format}}/ogcwkt" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{!export['ogcwkt']}}
          </div>
        </div>
        <div class="code-definition-container-usgs">
          <p>Definition: USGS</p>
          <ul id="cd-tabs">
            <li><a href="{{url_format}}/usgs" title="">Open in new page</a></li>
            <li><a href="#" title="">Copy URL to clipboard</a></li>
            <li><a href="#" title="">Copy TEXT to clipboard</a></li>
          </ul>
          <div class="syntax">
            {{!export['usgs']}}
          </div>
        </div>        
      </div>
%end
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
