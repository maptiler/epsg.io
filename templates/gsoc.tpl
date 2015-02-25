<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"  lang="en" xml:lang="en">
  <head>  
    <meta charset="utf-8"/>
    <title>EPSG.io - Google Summer of Code Ideas</title>
    <meta content="width=device-width, initial-scale=1, maximum-scale=1" name="viewport" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="description" content="EPSG.io" />
    <meta name="keywords" content="EPSG.io" />
    <meta name="robots" content="ALL,FOLLOW" />
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
    <style>
    a { color: #4295c5 !important; }
    </style>
  </head>
  
  <body id="detailpage" data-role="page">
    <div id="head">
      <p id="logo-container">
        <a href="/" title=""><span>Epsg.io</span> Coordinate Systems Worldwide</a>
      </p>
      <ul id="menu-top">
        <li><a href="/about" title="">About</a></li>
      </ul>
    </div>
    
    <div id="layout-container">
		<div id="detail-content-container">
			<div class="detail-content-inner-wide">
				<h1>Google Summer of Code 2015 - Ideas</h1>
				<p></p>
				<p>
					Klokan Technologies GmbH, Switzerland (<a href="http://www.klokantech.com/">http://www.klokantech.com/</a>) propose improvement of the open-source EPSG.io project (<a href="http://epsg.io/">http://epsg.io/</a>) - the web service with a database of coordinates systems used in maps worldwide.
				</p>
				<p>
					EPSG.io (<a href="http://epsg.io/">http://epsg.io/</a>) simplifies discovery of coordinate reference systems utilized all over the world for creating maps and geodata and for identifying geo-position. It is a practical tool for anybody interested in cartography and digital map making, who needs to know exact latitude and longitude values for numerical coordinates in different spatial reference systems. Included map application powered by Google Maps API allows to show the precise location anywhere on the planet also visually. The functionality of the portal is exposed via an API. Read more <a href="http://epsg.io/about">about the service</a> and explore the source code on <a href="http://www.github.com/klokantech/epsg.io/">GitHub</a>.
				</p>
				<p>
                EPSG.io is available under Simplified BSD License.</br>
				</p>
				<p>
				</p>
				<p>
					<h4>Idea #1: EPSG.io improvements</h4>
					<p>Requirements: practical knowledge of programming in Python and JavaScript (experience with Closure Tools, Google OpenLayers V3 and Google Maps API is welcome).</p>
					<p>The student will work on a set of tasks improving the open-source EPSG.io project and adding new exciting functionality to the online service.</p>
					<p></p>
					<ul>
						<li><img src="https://cloud.githubusercontent.com/assets/59284/6268870/09afd3b6-b850-11e4-92e2-f4ece69197fe.png" border="0" width="250"><br/>Overview map for each coordinate system - with visual representation of map projection, meridian, etc. Details in: <a href="https://github.com/klokantech/epsg.io/issues/62">#62</a></li>
						<li>Automate the update of the EPSG database to ensure the latest version is always indexed <a href="https://github.com/klokantech/epsg.io/issues/77">#77</a></li>
                        <li>Deploy via Docker - allowing an easy one-command start by anybody, even offline <a href="https://github.com/klokantech/epsg.io/issues/75">#75</a></li>
                        <li>Grid transformation and related Proj4js improment <a href="https://github.com/klokantech/epsg.io/issues/6">#6</a></li>
                        <li>Import ESRI specific codes <a href="https://github.com/klokantech/epsg.io/issues/24">#24</a></li>
                        <li>User-defined SRS indexing <a href="https://github.com/klokantech/epsg.io/issues/78">#78</a></li>
					</ul>
                    New ideas and inputs from the student are very welcome. See and use <a href="https://github.com/klokantech/epsg.io/milestones/gsoc">GitHub Issues</a>.
				</p>
				<p>
					<h4>The mentorship provided by Klokan Technologies GmbH</h4>
				    <ul>
						<li>Petr Pridal, Ph.D. (<a href="http://linkedin.com/in/klokan">CV</a>)</li>
						<li>Vaclav Klusak</li>
						<li>Petr Sloup</li>
					</ul>
				</p>
				<p>
				
				</p>
				<p>
				
				</p>
			</div>
			<div class="covered-area-container">
                <p>
                <a href="http://www.klokantech.com/"><img src="http://www.klokantech.com/img/klokantech.png" width="260" border="0"></a>
                </p>
				<p style="text-align:center"><a href="http://www.klokantech.com/">www.klokantech.com</a></p>
                <p>
				<a href="https://www.google-melange.com/gsoc/homepage/google/gsoc2015"><img src="./press/gsoc2015-300x270.jpg" width="260" border="0"></a>
                </p>
				<p style="text-align:center"><a href="https://www.google-melange.com/gsoc/homepage/google/gsoc2015">Google Summer of Code 2015</a></p>
				<p></p>
				<p>
					<span class="caption">EPSG.io identity</span>
				</p>
				<ul>Logo
				<a href="./press/epsg-banner-1400-560-2.png"><img src="./press/epsg-banner-1400-560-2.png" height="90" width="205"></a>
				</ul>
				<ul>Main page
				<a href="./press/main-page-pr.png"><img src="./press/main-page-pr.png" height="115" width="205"></a>
				</ul>
				<ul>Result page
				<a href="./press/results-pr.png"><img src="./press/results-pr.png" height="115" width="205"></a>
				</ul>
				<ul>Detail page
				<a href="./press/detail-pr.png"><img src="./press/detail-pr.png" height="115" width="205"></a>
				</ul>
				<ul>Map page
				<a href="./press/map-pr.png"><img src="./press/map-pr.png" height="115" width="205"></a>
				</ul>
			</div>
		</div>
	</div>

    <div id="spacer"><p></p></div>

     <div id="footer">

       <div id="foot">
         <p id="klokan-logo">
           <a href="http://www.klokantech.com/" title=""><img src="./img/klokan-logo-grey.png" alt="" /></a>
		 </p>
         <p id="mzk-logo">
           <a href="http://www.mzk.cz/" title=""><img src="./img/hzk-logo.png" alt="" /></a>
         </p>
         <p>Find a coordinate system and get position on a map. Powered by EPSG database {{version}}</p>
         <p id="copyright">Copyright &copy; 2015</p>
       </div>
     </div>

   </body>

 </html>
