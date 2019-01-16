<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>EPSG.io: Coordinate Systems Worldwide</title>
    <meta content="width=device-width, initial-scale=1, maximum-scale=1" name="viewport" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="description" content="EPSG.io: Coordinate systems worldwide (EPSG/ESRI), preview location on a map, get transformation, WKT, OGC GML, Proj.4. http://EPSG.io/ made by @klokantech" />
    <meta name="keywords" content="EPSG.io" />
    <meta name="robots" content="ALL,FOLLOW" />
    <meta property="og:image" content="//epsg.io/img/epsg-banner-440x280-2.png"/>
    <link rel="stylesheet" href="/css/main.css" type="text/css" />
    <link rel="shortcut icon" href="//epsg.io/favicon.ico" />
    <link rel="search" href="/opensearch.xml" title="EPSG.io" type="application/opensearchdescription+xml"/>
    <script src="/js/index.js"></script>
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','__gaTracker');

              __gaTracker('create', 'UA-47718358-1', 'epsg.io');
      __gaTracker('send', 'pageview');
    </script>
  </head>
  <ul id="menu-top">
    <li> <a href="/">Search</a></li>
    <li><a href="/map" title="">Map</a></li>
    <li><a href="/transform" title="">Transform</a></li>
    <li><a href="/about" title="">About</a></li>
  </ul>
  <body id="homepage" data-role="page">
    <div id="layout-container">
      <p id="logo-container">
        <a href="/"><span>Epsg.io</span>From MapTiler Team</a>
      </p>
      <h1>Coordinate Systems Worldwide</h1>

      <div id="search-container">

        <form action="/" method="get">
          <p><input id="q" name="q" type="search" placeholder="Country, code or name of a coordinate system ..." /> <input type="submit" name="" value="search" /></p>
        </form>

        <div class="home-action">
        <a class="home-search-img" href="/transform"><img src="/img/coordinates.png" alt="Coordinates"></a>
          <a class="home-search-img" href="/map"><img src="/img/position.png" alt="Position"></a>
          <a class="btn" href="/transform">Transform&nbsp;coordinates</a>
          <a class="btn" href="/map">Get&nbsp;position&nbsp;on&nbsp;a&nbsp;map</a>
        </div>

        <!--div id="countryLinkWrapper">
          <a href="/?q=Czech%20Republic" id="countryLink">Click to see the coordinates systems of <span id="country">Czech Republic</span></a>
        </div-->

        <div class="socialicons">
          <p>Share on</p>
          <a id="share_twitterb" href="https://twitter.com/share?original_referer=//epsg.io&amp;text=EPSG.io: Coordinate systems worldwide, view location on a map, get transformation, WKT, Proj.4. made by @klokantech"><span class="icon-epsg-twiter"></span></a>
          <a id="share_pinterest" href="https://pinterest.com/pin/create/button/?url=http%3A%2F%2Fepsg.io&amp;media=%2F%2Fdirect.epsg.io%2Fimg%2Fepsg-banner-440x280-2.png&description=EPSG.io:%20Coordinate%20systems%20worldwide%20(EPSG/ESRI),%20preview%20location%20on%20a%20map,%20get%20transformation,%20WKT,%20OGC%20GML,%20Proj.4.%20http://EPSG.io/%20made%20by%20@klokantech"><span class="icon-epsg-pinterest"></span></a>
          <a id="share_gplusdark" href="https://plus.google.com/share?url=//epsg.io/"><span class="icon-epsg-googleplus"></span></a>
        </div>
      </div>


    <div id="home-maptiler">
      <div class="maptiler-col-r">
        <img src="/img/maptiler-logo-icon.png" alt="MapTiler logo">
      </div>

      <div class="maptiler-col-l">
   <h3>Transform raster data with MapTiler</h3>
   <div>
   <p>MapTiler is Desktop app designed to turn large raster datasets into zoomable maps for your website. MapTiler use EPSG.IO database and has support for any coordinate system.</p>
 </div>
   <a href="https://www.maptiler.com/desktop/" class="btn">More information</a>
  </div>
</div>


      <h3 class="coordinate-systems">Picked coordinate systems</h3>

    <div id="home-menu-container">
      <div class="hm-column lft">
        <h2>World coordinate systems</h2>
        <ul>
          <li><a href="/4326" title="">WGS84 - World Geodetic System 1984, used in GPS </a></li>
          <li><a href="/3857" title="">Spherical Mercator, Google Maps Projection, OpenStreetMap, Bing</a></li>
          <li><a href="/?q=UTM" title="">UTM - Universal Transverse Mercator</a></li>
          <li><a href="/?q=etrs" title="">ETRS - European Terrestrial Reference System</a></li>
        </ul>
      </div>
      <div class="hm-column lft">
        <h2>Europe coordinate systems</h2>
        <ul>
          <li><a href="/?q=United%20Kingdom" title="">United Kingdom</a></li>
          <li><a href="/?q=France" title="">France</a></li>
          <li><a href="/?q=Czech%20Republic" title="">Czech Republic</a></li>
          <li><a href="/?q=Germany" title="">Germany</a></li>
          <li><a href="/?q=Netherlands" title="">Netherlands</a></li>
          <li><a href="/?q=Switzerland" title="">Switzerland</a></li>
        </ul>
      </div>
      <div class="hm-column lft last">
        <h2>Other coordinate systems</h2>
        <ul>
          <li><a href="/?q=Brazil" title="">Brazil</a></li>
          <li><a href="/?q=New%20Zealand" title="">New Zealand</a></li>
          <li><a href="/?q=Australia" title="">Australia</a></li>
        </ul>
      </div>
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
          <p>Find a coordinate system and get position on a map. Powered by EPSG database {{version}}</p>
        <p id="copyright">Copyright &copy; 2019</p>
      </div>
      </div>
    </div>
  </body>
</html>
