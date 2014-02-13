<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"  lang="en" xml:lang="en">
  <head>  
    <meta charset="utf-8"/>
    
    %if pagenum == 1:
      <title>{{title}}</title>
    %else:
      <title>{{title}}, page {{pagenum}}</title>
    %end
    
    <meta content="width=device-width, initial-scale=1, maximum-scale=1" name="viewport" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="description" content="EPSG.io" />
    <meta name="keywords" content="EPSG.io" />
    <meta name="robots" content="ALL,FOLLOW" />
    <meta property="og:image" content="http://epsg.io/img/epsg-banner-440x280-2.png"/>
    <link rel="stylesheet" href="/css/main.css" type="text/css" />
    <link rel="shortcut icon" href="http://epsg.io/favicon.ico" />
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','__gaTracker');

      __gaTracker('create', 'UA-47718358-1', 'epsg.io');
      __gaTracker('send', 'pageview');
    </script>
  </head>
  
  <body id="resultspage" data-role="page">
    
    <div id="head">
      <p id="logo-container">
        <a href="/" title=""><span>Epsg.io</span> Coordinate Systems Worldwide</a>
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
      <div id="title-container">
        %if pagenum == 1:
          <h1>{{title}}</h1>
        %else:
          <h1>{{title}}, page {{pagenum}}</h1>
        %end
      
        <p>
          %if deprecated == 1:
            Found {{num_results}} deprecated records
            %if num_results>0:
             and {{num_deprecated[0]}} <a href="{{num_deprecated[1]}}">valid</a> records
            %end
              (in {{elapsed}} seconds)
          %else:  
            Found {{num_results}} valid records
            %if num_deprecated[0]>0:
              and {{num_deprecated[0]}}  <a href="{{num_deprecated[1]}}">deprecated</a> records 
            %end  
              (in {{elapsed}} seconds)
          %end
        </p>
      </div>
      
      <div id="result-content-container">
        <div id="results-container">
          <ul class="results">
            %if num_results != 0:
              %for r in result:
                <li>
                  <h2>
                    <a href="/{{r['link']}}" title="">{{r['name']}} 
                    %if 'alt_title' in r['r']:
                      %if r['r']['alt_title'] and r['r']['name']!= r['r']['alt_title']:
                        - {{r['r']['alt_title']}}
                      %end
                    %end
                    </a></h2>
                  <p>
                    {{r['type_epsg']}}:{{r['short_code'][0]}}
                    %if r['r']['code_trans'] != 0:
                      with transformation: {{r['r']['code_trans']}}
                    %end
                  </p>
                  <p class="area">
                    %if r['r']['area_trans']:
                      %if r['r']['accuracy'] == "":
                        Area of use: {{r['area']}} (accuracy: unknown)
                      %else:  
                        Area of use: {{r['area']}} (accuracy: {{r['r']['accuracy']}})
                      %end
                    %else:
                      %if r['area']:
                        Area of use: {{r['area']}}
                      %end
                    %end
                  </p>
                  %if r['url_map'] != "":
                    <a href="{{r['url_map']}}">Coordinates on a map</a>
                  %end
                </li>
              %end
            %elif num_kind != 0:
              "{{kind_low[0]}}" is not in {{kind_low[1]}}, please select other kind
              <li>
              %for i in [0,8,12,16,17,18,19,24,25,26]:
                %if facets_list[i][4] != 0:
                  <h2><a href="{{facets_list[i][5]}}" title="">{{facets_list[i][6]}}s ({{!facets_list[i][4]}}) </a></h2>
                %end
              %end
              </li>
            %else:
              Please change your query.
            %end
            %if deprecated != 1 and num_deprecated[0]>0:
              <li><a href="{{num_deprecated[1]}}">Search deprecated ({{num_deprecated[0]}})</a></li>
            %elif deprecated == 1 and num_results>0:
              <li><a href="{{num_deprecated[1]}}">Search valid ({{num_deprecated[0]}})</a></li>
            %end 
          </ul>
          
          <ul class="paginator">
            %if (pagenum-1) > 0:
              <li class="prev"><a href="/?q={{query}}&amp;page={{pagenum-1}}" title="">Prev</a></li>
            %end

            %for i in paging:
              %if i == pagenum:
                <li><span>{{ i }}</span></li>
              %else:
                <li><a href="/?q={{query}}&amp;page={{i}}" title="">{{i}}</a></li>
              %end
            %end

            %if (pagenum+1) in paging:
              <li class="next"><a href="/?q={{query}}&amp;page={{pagenum+1}}" title="">Next</a></li>
            %end
          </ul>
        </div>
        
        <div id="side-container">
          %if show_alt_search:
            <h3>Type of results</h3>
              <ul id="alt-search">
                %colored_head = False
                %for i in range(0,len(facets_list)):
                  %if facets_list[i][4] != 0:
                    %if facets_list[i][2] == "":
                      %if selected_kind_index == i:
                        <li class="head-of-group"><a class="colored" href="{{facets_list[i][5]}}">{{facets_list[i][3]}} ({{facets_list[i][4]}})</a></li>
                        %colored_head = True
                      %else:
                        <li class="head-of-group"><a href="{{facets_list[i][5]}}">{{facets_list[i][3]}} ({{facets_list[i][4]}})</a></li>
                        %colored_head = False
                      %end
                    %else:
                      %if selected_kind_index == i or colored_head == True:
                        <li>{{!facets_list[i][2]}}<a class="colored" href="{{facets_list[i][5]}}">{{facets_list[i][3]}} ({{facets_list[i][4]}})</a></li>
                      %else:
                        <li>{{!facets_list[i][2]}}<a href="{{facets_list[i][5]}}">{{facets_list[i][3]}} ({{facets_list[i][4]}})</a></li>
                      %end
                    %end
                  %end
                %end
              </ul>
          %end
        </div>
      </div>
   </div>
   <div id="spacer"><p></p></div>

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
