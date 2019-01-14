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
    <link rel="shortcut icon" href="//epsg.io/favicon.ico" />
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','__gaTracker');

      __gaTracker('create', 'UA-47718358-1', 'epsg.io');
      __gaTracker('send', 'pageview');
    </script>
  </head>

  <body id="detailpage" data-role="page">
    <div id="head">
      <p id="logo-container">
        <a href="/" title=""><span>Epsg.io</span>From MapTiler team</a>
      </p>
      <ul id="menu-top">
        <li> <a href="/">Search</a></li>
        <li><a href="/map" title="">Map</a></li>
        <li><a href="/transform" title="">Transform</a></li>
        <li><a href="/about" title="">About</a></li>
      </ul>
    </div>

    <div id="layout-container">
		<div id="detail-content-container">
			<div class="detail-content-inner-wide">
				<h1>EPSG.io: Find Coordinate Systems Worldwide</h1>
				<p></p>
				<p>
					<a href="//www.klokantech.com/">Klokan Technologies GmbH, Switzerland (www.klokantech.com/)</a> is pleased to announce a new open-source web service with a database of coordinates systems used in maps worldwide.
				</p>
				<p>
					EPSG.io (<a href="//epsg.io/">http://epsg.io/</a>) simplifies discovery of coordinate reference systems utilized all over the world for creating maps and geodata and for identifying geo-position. It is a practical tool for anybody interested in cartography and digital map making, who needs to know exact latitude and longitude values for numerical coordinates in different spatial reference systems. Included map application allows to show the precise location anywhere on the planet also visually.
				</p>
				<p>
					The website comes with a fulltext search indexing over 6000 coordinate systems. The search starts by typing the name of the system, name of covered country, state or any of the combinations of these. Searching for EPSG and ESRI codes is supported as well.
				</p>
				<p>
					Each coordinates system and transformation has a short permanent link and is exportable in various formats (WKT, XML, OGC GML, Proj.4, JavaScript, SQL).
				</p>
				<p>
					The web has also API allowing integration of the search functionality and transformations in third party applications.
				</p>
				<p>
					Soon this functionality will be used the by the MapTiler (<a href="//www.maptiler.com">http://www.maptiler.com</a>) to simplify the transformation or existing raster geodata and images into Google Maps and OGC WMTS compatible tiles. MapTiler is the easiest way how to prepare custom maps for mobile devices and web presentation.
				</p>
				<p>
					Georeferencer (<a href="//www.klokantech.com/georeferencer/">http://www.klokantech.com/georeferencer/</a>), the online service for turning scanned maps into geodata in a web browser, will soon utilize EPSG.io service as well - allowing a user-friendly selection of any coordinate system and map projection during the georeferencing process.
				</p>
				<p>
					The EPSG.io website is built around the official EPSG database maintained by OGP Geomatics Committee (<a href="http://www.epsg.org/">http://www.epsg.org/</a>). The database comprises of very detailed geodetic parameters from a range of sources and authorities. EPSG.io simplifies access to exact parameters for thousands of spatial reference systems, transformations and conversions, datums, ellipsoids, meridians, units, etc.
				</p>
				<p>
					The whole project is open-source - with complete source code available on GitHub: <a href="https://github.com/klokantech/epsg.io">https://github.com/klokantech/epsg.io</a>
					Contribution from the online community is very welcome. New features, fixes of bugs and additional functionality can be easily developed by anybody who is interested in improvement of the system.
				</p>
				<p>
				The web supports OpenSearch protocol. In Chrome web browser it is possible to type into address bar "epsg.io" then <tab> and your search phrase. Firefox can add the system to the list of supported search engines as well. Web site is available as Google Chrome OS application (<a href="http://goo.gl/frnJxu">http://goo.gl/frnJxu</a>). The website availability and performance is improved by a CDN with over 20 caching servers worldwide.
				</p>
				<p>
					The initial version of this open-source project has been developed by the Moravian Library in Brno, Czech Republic (<a href="//www.mzk.cz/">http://www.mzk.cz/</a>) thanks to support from the Programme of Applied Research and Development of the National and Cultural Identity (NAKI) from the Ministry of Culture of the Czech Republic, project No. DF11P01OVV003 - TEMAP - Technology for access to Czech map collections: methodology and software for protection and re-use of national cartographic heritage (<a href="//www.temap.cz/en/">http://www.temap.cz/en/</a>).
				</p>
				<p>
					<h4>The main features</h4>
					<ul>
						<li>Fulltext search for the complete database of coordinate systems from EPSG</li>
						<li>Short rememberable URLs, i.e. <a href="//epsg.io/4326">http://epsg.io/4326</a></li>
						<li>Type GPS latitude/longitude and get projected coordinates or vice versa</li>
						<li>Precise numerical location on a map / aerial photo for any place on the planet</li>
						<li>Export definitions in various formats, including WKT, OGC GML, XML, Proj.4, SQL, JS, etc.</li>
						<li>Facets for retrieval of alternative record types from the official EPSG database</li>
						<li>API for the search in EPSG database and for transformations</li>
					</ul>
				</p>
				<p>
					<h4>Frequently answered questions</h4>
					<i>How does the system differ from spatialreference.org and epsg-registry.org?</i>
					<p></p>
					<p>
					It is much easier to find the coordinate systems (for example query "utm wgs norway" gives list of all UTM zones with WGS covering area of Norway).
					All available transformations for selected coordinate reference system are visible and applicable (it is possible to find alternative 7 parameter transformation for Proj4js replacing a default grid transformation, or choose a transformation with higher accuracy for a selected area).
					Preview location for any numerical coordinates on a detailed map - with copy&paste functionality.
					Complete EPSG database with codes for datums, units, transformations, etc is indexed and searchable, and the individual EPSG records are linked from every detail page.
					</p>
				</p>
				<p>
					<h4>Main contributors</h4>
				    <ul>
            <li><a href="https://www.maptiler.com">MapTiler Team</a></li>
						<li>Petr Pridal (managing director KlokanTech.com, work done as part of PhD thesis at Czech Technical University of Technology - Geodesy and Cartography)</li>
						<li>Tomas Pohanka (internship at KlokanTech.com, Masters degree candidate at Palacky University Olomouc - Geoinformatics)</li>
						<li>Radim Kacer (designer at KlokanTech.com)</li>
					</ul>
				</p>
				<p>

				</p>
				<p>

				</p>
			</div>
			<div class="covered-area-container">
				<p>
					<span class="caption">Downloadable content</span>
				</p>
				<ul>
				<a href="./press/announcement-epsg_io.zip">Download all content in a one .zip archive</a>
				</ul>
				<p></p>
				<p>
					<span class="caption">Pictures</span>
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
    <script type="text/javascript">home_init();</script>

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
         <div id="maptiler-logo">
           <a href="https://www.maptiler.com/" title=""><img src="/img/maptiler-logo.png" alt="" /></a>
         <p id="copyright">Copyright &copy; 2018</p>
       </div>
       </div>
     </div>

   </body>

 </html>
