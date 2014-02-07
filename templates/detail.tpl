<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"  lang="en" xml:lang="en">
  <head>  
    <meta charset="utf-8"/>
%if alt_title:
    <title>{{name}} - {{alt_title}} - {{type_epsg}}:{{item['code']}}</title>
%else:
    <title>{{name}} - {{type_epsg}}:{{item['code']}}</title>
%end    
    
    
    <meta content="width=device-width, initial-scale=1, maximum-scale=1" name="viewport" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="description" content="EPSG:{{item['code']}} {{kind}} for {{item['area']}} {{item['remarks']}} {{item['scope']}}" />
    <meta name="keywords" content="EPSG.io" />
    <meta name="robots" content="ALL,FOLLOW" />
    <link rel="stylesheet" href="/css/main.css" type="text/css" />
    <link rel="shortcut icon" href="http://epsg.io/favicon.ico" />
    <script src="/js/ZeroClipboard.min.js"></script>
    <script src="/js/index.js"></script>
    
  </head>
  
  <body id="detailpage" data-role="page">
    
    <div id="head">
      <p id="logo-container">
        <a href="http://epsg.io" title=""><span>Epsg.io</span> Coordinate systems worldwide</a>
      </p>
      <ul id="menu-top">
        <li><a href="http://epsg.io/about" title="">About</a></li>
      </ul>
    </div>
    
    <div id="layout-container">
      
      %if item['deprecated'] == 1:
        <h1>{{type_epsg}}:{{code_short[0]}} DEPRECATED</h1>
      %else:
        <h1>{{type_epsg}}:{{code_short[0]}}</h1>
      %end

      <p>
        <a href="{{url_kind}}">{{kind}} </a>
      </p>

      <h2>{{name}}<br /> {{alt_title}}</h2>

      <p>
        %if 'scope' in item:
          %if item['scope']:
            Scope: {{item['scope']}}<br />
          %end
        %end

        %if detail:
          %if detail[0]['url_area'] == "":
            Area of use: <a href="{{detail[0]['url_area']}}"> {{item['area']}}</a><br />
          %end
        %else:
          %if item['area']:
            Area of use: <a href="{{url_area}}">{{area_item}}</a><br />
          %end
        %end

        %if 'remarks' in item:
          %if item['remarks']:
            Remarks: {{item['remarks']}}<br />
          %end
        %end

        %if 'information_source' in item:
          %if item['information_source']:
            Information source: {{item['information_source']}}<br />
          %end
        %end

        %if 'revision_date' in item:
          %if item['revision_date']:
            Revision date: {{item['revision_date']}}<br />
          %end
        %end

        %if 'concatop' in item:
          %if item['concatop']:
            Steps of transformation: {{item['concatop']}}<br />
          %end
        %end

        %if nadgrid:
          NadGrid file: {{nadgrid}}<br />
        %end

        %if 'geogcrs' in item:
          %if item['geogcrs']:
            Geodetic coordinate reference system: <a href="/{{item['geogcrs'][0]}}" title="">{{item['geogcrs'][1]}}</a><br />
          %end
        %end

        %if 'datum' in item:
          %if item['datum'] != 0 and item['datum'] :
            Datum: <a href="/{{item['datum'][0]}}-datum/" title="">{{item['datum'][1]}}</a><br />
          %end
        %end

        %if 'cs' in item:
          %if item['cs']:
            Coordinate system: <a href="/{{item['cs'][0]}}-cs">{{item['cs'][1]}}</a><br />
          %end
        %end

        %if item['target_uom']:
          %if int(code_short[0]) != int(item['target_uom'][0]):
            Target uom: <a href="/{{item['target_uom'][0]}}-units">{{item['target_uom'][1]}}</a><br />
          %end
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

        %if 'description' in item:
          %if item['description']:
            Description: {{item['description']}}<br />
          %end
        %end

        %if 'ellipsoid' in item:
          %if item['ellipsoid']:
            %if item['ellipsoid'][0] != "None":
              Ellipsoid: <a href="/{{item['ellipsoid'][0]}}-ellipsoid">{{item['ellipsoid'][1]}}</a><br />
            %end
          %end
        %end

        %if "method" in item:
          %if item['method']:
            Method: <a href="/{{item['method'][0]}}-method" title="">{{item['method'][1]}}</a><br />
          %end
        %end

        %if 'data_source' in item:
          %if item['data_source']:
            Data source: {{item['data_source']}} <br />
          %end
        %end

        %if 'primem' in item:
          %if item['primem']:
            Prime meridian: <a href="/{{item['primem'][0]}}-primem">{{item['primem'][1]}}</a>
            %if 'greenwich_longitude' in item:
              %if item['primem'][0] != 8901 and detail != [] and item['greenwich_longitude'] !=0:
                ({{item['greenwich_longitude']}} degree from Greenwich)<br />
              %else:
                <br />
              %end
            %else:
              <br />
            %end
          %end
        %end

        %if detail != []:
          %if 'greenwich_longitude' in item:
            %if item['greenwich_longitude'] != 0 and item['greenwich_longitude']:
              {{item['greenwich_longitude']}} degree from Greenwich<br />
            %end
          %end
        %end

        %if detail != []:
          %if detail[0]['url_axis']:
            %for a in detail[0]['url_axis']:
              Link to axis : <a href="/{{a['axis_code']}}-axis">{{a['axis_name']}}</a><br />
            %end
          %end
        %end

        %found_alt = False
        %if 'alt_description' in item:
          %if item['alt_description']:
            %if wkt:
              Alternative description: {{!item['alt_description']}}<br />
            %else:
              %found_alt = True
              %if export_html:
                <div id="description-message">{{!export_html}} </div>
              %else:
                <div id="description-message">{{!item['alt_description']}} </div>
              %end
            %end
          %end
        %end

        %if 'alt_code' in item:
          %if item['alt_code'] != ['']:
            Alternatives codes : 
            %for a in item['alt_code']:
              <a href="/{{a}}">{{a}}</a>
            %end
          %end
        %end
      </p>
      
      <div id="detail-content-container">
        <div class="map-container">
          %no_map = False
          %if item['bbox']:
            %if center:
              %if trans_lat:
                <div id="mini-map">
                  <a href="{{url_format}}/map">
                    <img src="/img/epsg-target-small.png" id="crosshair" alt="" />
                      <img src="http://maps.googleapis.com/maps/api/staticmap?size=235x190&amp;scale=2&amp;sensor=false&amp;visual_refresh=true&amp;center={{center[0]}},{{center[1]}}&amp;path=color:0xff0000ff|fillcolor:0xff000022|weight:2|{{g_coords}}" alt="SimpleMap" height="190" width="235">
              
                  </a>
                </div>
              %else:
                <div id="mini-map">
                  <img src="/img/epsg-target-small.png" id="crosshair" alt="" />
                    <img src="http://maps.googleapis.com/maps/api/staticmap?size=235x190&amp;scale=2&amp;sensor=false&amp;visual_refresh=true&amp;center={{center[0]}},{{center[1]}}&amp;path=color:0xff0000ff|fillcolor:0xff000022|weight:2|{{g_coords}}" alt="SimpleMap" height="190" width="235">
                </div>
              %end
            %end
          %else:
            %no_map = True
            <p>NO MAP AVAILABLE</p>
          %end

          %if trans_lat and trans_lon:
            <p>
              Center coordinates<br />
              <span>{{trans_lat}}</span>  <span>{{trans_lon}}</span> <br />
              <p>Projected bounds<br />
                {{bbox_coords[3]}} {{bbox_coords[2]}}<br />
                {{bbox_coords[1]}} {{bbox_coords[0]}}<br />
              </p>
              <p>
                %if default_trans:
                  WGS84 bounds<br />
                  {{default_trans['bbox'][1]}} {{default_trans['bbox'][2]}}<br />
                  {{default_trans['bbox'][3]}} {{default_trans['bbox'][0]}}
                %else:
                  WGS84 bounds<br />
                  {{item['bbox'][1]}} {{item['bbox'][2]}}<br />
                  {{item['bbox'][3]}} {{item['bbox'][0]}}
                %end
            
              </p> 
            </p>
          %end
          
          %if bbox_coords and not (trans_lat or trans_lon):
            <p>WGS84 bounds: {{bbox_coords[3]}} {{bbox_coords[2]}}, {{bbox_coords[1]}} {{bbox_coords[0]}}</p>
          %end

        </div>

        <div class="transformations-container">        
          %no_trans = False
          %if trans:
            <h3>Available transformations:</h3>
            <ul>
              % i = 0
              %for r in trans:
                %if r['link'] == "" and r['deprecated'] == 0 and r['area_trans']:
                  <li> {{area_trans_item}}
                
                  %if r['accuracy']:
                    , accuracy {{r['accuracy']}} m, 
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
                    <a href="/{{r['link']}}" title = "{{r['trans_remarks']}}">{{area_trans_item}}, accuracy {{r['accuracy']}} m, code {{r['code_trans']}} 
                  
                    %if r['default'] == True:
                      DEFAULT
                    %end
                    </a>
                    %i+=1
                  </li>
                %end
              %end
            
            %if deprecated_available == 1:
              %if i == 0:
                <div id="trans_deprecated">
              %else:
                <a href="#" id="trans_deprecated_link">Show deprecated transformations</a><p></p>
                <div id="trans_deprecated">
              %end

              %for r in trans:
                %if r['deprecated'] == 1:
                  %if r['link'] == "":
                    <li>{{r['area_trans']}}, accuracy {{r['accuracy']}} m, code {{area_trans_item}} DEPRECATED
                  
                    %if r['default'] == True:
                      DEFAULT
                    %end
                    </li>
                  %else:
                    <li>
                      <a href="/{{r['link']}}" title = "{{r['trans_remarks']}}">{{area_trans_item}}, accuracy {{r['accuracy']}} m,  code {{r['code_trans']}} DEPRECATED
     
                    %if r['default'] == True:
                      DEFAULT
                    %end
                      </a>
                    </li>
                  %end
                %end
              %end
              
              </div>
            %else:
              <!--<a href="#" id="trans_deprecated_link"></a><p></p>-->
            %end
            
            </ul>
            
          %else:
            %no_trans = True
            <!--<a href="#" id="trans_deprecated_link"></a><br />-->
          %end
          <div id="projected-link">
            %if projcrs_by_gcrs:
              %if kind == "Projected coordinate system":
                <h3>Coordinates with same geodetic base (<a href="/{{item['geogcrs'][0]}}">{{item['geogcrs'][1]}}</a>):</h3>
              %else:
                <h3>Coordinates using this {{kind.lower()}}:</h3>
              %end
            %end

            %for r in projcrs_by_gcrs:
              <a href="/{{r['result']['code']}}">EPSG:{{r['result']['code']}} {{r['result']['name']}}</a>
              %if r['result']['code_trans']:
                <a href="{{r['result']['code']}}/map"> (map)</a> <br />
              %else:
                <br />
              %end
            %end

            %if more_gcrs_result:
              <a href="{{more_gcrs_result}}">More</a>
            %end
          </div>
        </div>
        <div class="location-data-container">
          %found = False
          %if trans:
            %for r in trans:
              %if r['link'] == "" and r['area_trans'] and not found:
                  %found = True
                  <h2>
                {{area_trans_item}} <br />
                
                %if r['code_trans'] != 0:
                  {{type_epsg}}: <a href="/{{r['code_trans']}}">{{r['code_trans']}}</a>
                %end

                %if r['default'] == True:
                  DEFAULT
                %end
                </h2>
                %if r['accuracy']:
                  Accuracy {{r['accuracy']}} m 
                %end
              %end
            %end
          %end
          
          %no_default = False
          %if not found:
            %no_default = True
            %if not no_trans:
              <p>NO DEFAULT TRANSFORMATION</p>
            %end
          %end

          %if center and trans_lat and trans_lon:
            <p class="btn-link-container">
              <a href="{{url_format}}/map"><i></i>Get position on a map</a>
            </p>
          %end
          
          %if trans and default_trans:
            <p>
              %if default_trans['method']:
                Method: <a href="/{{default_trans['method'][0]}}-method">{{default_trans['method'][1]}}</a><br />
              %end
                Area of use: <a href="{{url_area_trans}}">{{default_trans['area']}}</a><br />
                Remarks: {{default_trans['remarks']}}<br />
                Information source: {{default_trans['information_source']}}<br />
                Revision date: {{default_trans['revision_date']}}<br />
                
              %if url_concatop != []:
                Steps of transformation: 
                %for url in url_concatop:
                  <a href="{{url}}">{{url}} </a>
                %end
              %end
            </p>
          %end
        
        </div>
        
        

      </div>
      %if no_map and no_trans and no_default and not found_alt:
        %if 'alt_description' in item:
          %if item['alt_description']:
            <div id="description-message">{{!item['alt_description']}}</div>
          %end
        %end
      %end

      <div id="edit-box-container">
        %if url_format and error_code == 0:
        <div id="eb-menu-container">
          <h4>Export</h4>
          <ul id="eb-menu">
            <li><a class="switcher switcher_selected" id="s_html" href="{{url_format}}.html">Well Known Text as HTML<i></i></a></li>
            <li><a class="switcher" id="s_wkt" href="{{url_format}}.wkt">OGC WKT<i></i></a></li>
            <!-- <li><a class="switcher" id="s_prettywkt" href="{{url_format}}.prettywkt">PrettyWKT<i></i></a></li>-->
            <li><a class="switcher" id="s_esriwkt" href="{{url_format}}.esriwkt">ESRI WKT<i></i></a></li>
            <li><a class="switcher" id="s_proj4" href="{{url_format}}.proj4">PROJ.4<i></i></a></li>
            <li><a class="switcher" id="s_proj4js" href="{{url_format}}.proj4js">JavaScript (PROJ.4)<i></i></a></li>
            <li><a class="switcher" id="s_gml" href="{{url_format}}.gml">OGC GML<i></i></a></li>
            <li><a class="switcher" id="s_xml" href="{{url_format}}.xml">XML<i></i></a></li>
            <li><a class="switcher" id="s_geoserver" href="{{url_format}}.geoserver">GeoServer<i></i></a></li>
            <li><a class="switcher" id="s_mapfile" href="{{url_format}}.mapfile">MapServer<i></i></a></li>
            <!-- <li><a class="switcher" id="s_mapserverpython" href="{{url_format}}.mapserverpython">MapSever - Python<i></i></a></li> -->
            <li><a class="switcher" id="s_mapnik" href="{{url_format}}.mapnik">Mapnik<i></i></a></li>
            <!-- <li><a class="switcher" id="s_mapnikpython" href="{{url_format}}.mapnikpython">Mapnik - Python<i></i></a></li> -->
            <li><a class="switcher" id="s_postgis" href="{{url_format}}.sql">SQL (PostGIS)<i></i></a></li>
            <!-- <li><a class="switcher" id="s_json" href="{{url_format}}.json">JSON<i></i></a></li> -->
            <li><a class="switcher" id="s_usgs" href="{{url_format}}.usgs">USGS<i></i></a></li>
          </ul>
        </div>
        
        <div class="code-definition-container code_visible" id="s_html_code">
          <p>Definition: Well Known Text (WKT)</p>
          <ul>
            <li><a href="{{url_format}}.prettywkt">Open</a></li>
            <li><a id="s_html_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.prettywkt" href="#">Copy URL</a></li>
            <li><a id="s_html_copyText" class="zeroclipboard" data-clipboard-target="s_html_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.prettywkt?download">Download</a></li>
            
          </ul>
          <div class="syntax">
            {{!export_html}}
          </div>
          <div class="syntax" id="s_html_text">
            <pre>{{export['prettywkt']}}</pre>
          </div>
        </div>

        <div class="code-definition-container" id="s_esriwkt_code">
          <p>Definition: ESRI WKT</p>
          <ul>
            <li><a href="{{url_format}}.esriwkt">Open</a></li>
            <li><a id="s_esriwkt_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.esriwkt" href="#">Copy URL</a></li>
            <li><a id="s_esriwkt_copyText" class="zeroclipboard" data-clipboard-target="s_esriwkt_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.esriwkt?download">Download</a></li>
          
          </ul>
          <div id="s_esriwkt_text" class="syntax">
            <pre>{{export['esriwkt']}}</pre>
            
          </div>
        </div>
        
        <div class="code-definition-container" id="s_proj4_code">
          <p>Definition: PROJ.4</p>
          <ul>
            <li><a href="{{url_format}}.proj4">Open</a></li>
            <li><a id="s_proj4_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.proj4" href="#">Copy URL</a></li>
            <li><a id="s_proj4_copyText" class="zeroclipboard" data-clipboard-target="s_proj4_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.proj4?download">Download</a></li>
            
          </ul>
          <div id="s_proj4_text" class="syntax">
            <pre>{{export['proj4']}}</pre>
          </div>
        </div>
        
        <div class="code-definition-container" id="s_proj4js_code">
          <p>Definition: JavaScript (PROJ.4) </p>
          <ul>
            <li><a href="{{url_format}}.js">Open</a></li>
            <li><a id="s_proj4js_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.js" href="#">Copy URL</a></li>
            <li><a id="s_proj4js_copyText" class="zeroclipboard" data-clipboard-target="s_proj4js_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.js?download">Download</a></li>
            
          </ul>
          <div id="s_proj4js_text" class="syntax">
            <pre>{{export['proj4js']}}</pre>
          </div>
        </div>
        
        <div class="code-definition-container" id="s_gml_code">
          <p>Definition: OGC GML</p>
          <ul>
            <li><a href="{{url_format}}.gml">Open</a></li>
            <li><a id="s_gml_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.gml" href="#">Copy URL</a></li>
            <li><a id="s_gml_copyText" class="zeroclipboard" data-clipboard-target="s_gml_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.gml?download">Download</a></li>

          </ul>
          <div class="syntax">
            {{!ogpxml_highlight}}
          </div>
          <div class="syntax" id="s_gml_text">
            {{ogpxml}}
          </div>
        </div>

        
        <div class="code-definition-container" id="s_xml_code">
          <p>Definition: XML</p>
          <ul>
            <li><a href="{{url_format}}.xml">Open</a></li>
            <li><a id="s_xml_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.xml" href="#">Copy URL</a></li>
            <li><a id="s_xml_copyText" class="zeroclipboard" data-clipboard-target="s_xml_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.xml?download">Download</a></li>
            
          </ul>
          <div class="syntax">
            {{!xml_highlight}}
          </div>
          <div class="syntax" id="s_xml_text">
            <pre>{{export['xml']}}</pre>
          </div>
        </div>
        
        <div class="code-definition-container" id="s_geoserver_code">
          <p>Definition: GeoServer</p>
          <ul>
            <li><a href="{{url_format}}.geoserver">Open</a></li>
            <li><a id="s_geoserver_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.geoserver" href="#">Copy URL</a></li>
            <li><a id="s_geoserver_copyText" class="zeroclipboard" data-clipboard-target="s_geoserver_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.geoserver?download">Download</a></li>
            
          </ul>
          <div id="s_geoserver_text" class="syntax">
            <pre>{{export['geoserver']}}</pre>
          </div>
        </div>
        
        <div class="code-definition-container" id="s_mapfile_code">
          <p>Definition: MapServer - MAPfile</p>
          <ul>
            <li><a href="{{url_format}}.mapfile">Open</a></li>
            <li><a id="s_mapfile_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.mapfile" href="#">Copy URL</a></li>
            <li><a id="s_mapfile_copyText" class="zeroclipboard" data-clipboard-target="s_mapfile_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.mapfile?download">Download</a></li>
            
          </ul>
          <div id="s_mapfile_text" class="syntax">
            <pre>{{!export['mapfile']}}</pre>
          </div>
     <!--</div>
        <div class="code-definition-container" id="s_mapserverpython_code"> -->
          <p>Definition: MapServer - Python</p>
          <ul>
            <li><a href="{{url_format}}.mapserverpython">Open</a></li>
            <li><a id="s_mapserverpython_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.mapserverpython" href="#">Copy URL</a></li>
            <li><a id="s_mapserverpython_copyText" class="zeroclipboard" data-clipboard-target="s_mapserverpython_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.mapserverpython?download">Download</a></li>
            
          </ul>
          <div id="s_mapserverpython_text" class="syntax">
            <pre>{{!export['mapserverpython']}}</pre>
          </div>
        </div>
        
        <div class="code-definition-container" id="s_mapnik_code">
          <p>Definition: Mapnik</p>
          <ul>
            <li><a href="{{url_format}}.mapnik">Open in new page</a></li>
            <li><a id="s_mapnik_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.mapnik" href="#">Copy URL</a></li>
            <li><a id="s_mapnik_copyText" class="zeroclipboard" data-clipboard-target="s_mapnik_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.mapnik?download">Download</a></li>
            
          </ul>
          <div id="s_mapnik_text" class="syntax">
            <pre>{{export['mapnik']}}</pre>
          </div>
     <!--</div>
        <div class="code-definition-container" id="s_mapnikpython_code"> -->
          <p>Definition: Mapnik - Python</p>
          <ul>
            <li><a href="{{url_format}}.mapnikpython">Open</a></li>
            <li><a id="s_mapnikpython_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.mapnikpython" href="#">Copy URL</a></li>
            <li><a id="s_mapnikpython_copyText" class="zeroclipboard" data-clipboard-target="s_mapnikpython_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.mapnikpython?download">Download</a></li>
            
          </ul>
          <div class="syntax">
            <pre>{{!export['mapnikpython']}}</pre>
          </div>
        </div>
        
        <div class="code-definition-container" id="s_postgis_code">
          <p>Definition: SQL (PostGIS)</p>
          <ul>
            <li><a href="{{url_format}}.sql">Open</a></li>
            <li><a id="s_postgis_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.sql" href="#">Copy URL</a></li>
            <li><a id="s_postgis_copyText" class="zeroclipboard" data-clipboard-target="s_postgis_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.sql?download">Download</a></li>
            
          </ul>
          <div id="s_postgis_text" class="syntax">
            <pre>{{!export['postgis']}}</pre>
          </div>
        </div>

        <div class="code-definition-container" id="s_wkt_code">
          <p>Definition: OGC WKT</p>
          <ul>
            <li><a href="{{url_format}}.wkt">Open</a></li>
            <li><a id="s_wkt_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.wkt" href="#">Copy URL</a></li>
            <li><a id="s_wkt_copyText" class="zeroclipboard" data-clipboard-target="s_wkt_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.wkt?download">Download</a></li>
            
          </ul>
          <div id="s_wkt_text" class="syntax">
            <pre>{{!export['ogcwkt']}}</pre>
          </div>
        </div>
        
        <div class="code-definition-container" id="s_usgs_code">
          <p>Definition: USGS</p>
          <ul>
            <li><a href="{{url_format}}.usgs">Open</a></li>
            <li><a id="s_usgs_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.usgs" href="#">Copy URL</a></li>
            <li><a id="s_usgs_copyText" class="zeroclipboard" data-clipboard-target="s_usgs_text" href="#">Copy TEXT</a></li>
            <li><a href="{{url_format}}.usgs?download">Download</a></li>
            
          </ul>
          <div id="s_usgs_text" class="syntax">
            <pre>{{!export['usgs']}}</pre>
          </div>
        </div>
        %elif ogpxml:
          <div id="eb-menu-container">
            <h4>Export</h4>
            <ul id="eb-menu">
              <li><a class="switcher switcher_selected" id="s_gml" href="{{url_format}}.gml">OGP XML<i></i></a></li>
            </ul>
          </div>

          <div class="code-definition-container code_visible" id="s_gml_code">
            <p>Definition: OGP XML</p>
            <ul>
              <li><a href="{{url_format}}.gml">Open</a></li>
              <li><a id="s_gml_copyUrl" class="zeroclipboard" data-clipboard-text="http://epsg.io{{url_format}}.gml" href="#">Copy URL</a></li>
              <li><a id="s_gml_copyText" class="zeroclipboard" data-clipboard-target="s_gml_text" href="#">Copy TEXT</a></li>
              <li><a href="{{url_format}}.gml?download">Download</a></li>

            </ul>
            <div class="syntax">
              {{!ogpxml_highlight}}
            </div>
            <div class="syntax" id="s_gml_text">
              {{ogpxml}}
            </div>
          </div>




        %end
      </div>
    </div>
      
       <div id="spacer"><p></p></div>
       <script type="text/javascript">detail_init();</script>

        <div id="footer">

          <script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
          <!-- EPSG.io -->
          <ins class="adsbygoogle"
               style="display:inline-block;width:728px;height:90px"
               data-ad-client="ca-pub-0328423815528922"
               data-ad-slot="6564733120"></ins>
          <script>
          (adsbygoogle = window.adsbygoogle || []).push({});
          </script>

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
  </body>
</html>
