<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"  lang="en" xml:lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>Transform coordinates for position on a map - converting latitude / longitude degrees</title>
    <meta content="width=device-width, initial-scale=1, maximum-scale=1" name="viewport" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="description" content="Transform coordinates for position on a map - converting latitude / longitude degrees" />
    <meta name="keywords" content="EPSG.io" />
    <meta name="robots" content="ALL,FOLLOW" />
    <link rel="stylesheet" href="/css/main.css" type="text/css" />
    <link rel="shortcut icon" href="//epsg.io/favicon.ico" />
    <link rel="search" href="/opensearch.xml" title="EPSG.io" type="application/opensearchdescription+xml"/>
    <script src="/js/ZeroClipboard.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/proj4js/2.3.12/proj4.js"></script>
    <script src="/js/map.js"></script>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?v=3.3&sensor=false"></script>
  </head>
  <body id="mappage" data-role="page">
    <div id="map"></div>
    <div id="map-plus">+</div>
    <div id="map-minus">-</div>
    <div id="map-search">q</div>
    <div id="search-container">
      <p><form><input type="search" name="geocoder" id="geocoder" placeholder="Place or address" /></form></p>
    </div>
    <select id="mapType">
      <option value="mqosm">OSM MapQuest</option>
      <option value="osm" data-tilejson="http://klokantech.tileserver.com/osm-bright/index.json?key=ITnCvdev3U2WlYotXxrX">OSM Bright</option>
      <option value="satellite" data-tilejson="https://api.tiles.mapbox.com/v4/epsg.og9084kh.json?access_token=pk.eyJ1IjoiZXBzZyIsImEiOiJjaWloNjQybjgwMDA2dm5tMGE3eTk3eXVuIn0.OuKrtb4M8Fca6cO3waqqWg">MapBox Satellite</option>
      <option value="gmaps-roadmap">Google Maps Streets</option>
      <option value="gmaps-satellite">Google Maps Satellite</option>
      <option value="gmaps-hybrid">Google Maps Hybrid</option>
    </select>
    <div id="mapsight"></div>
    <div id="head">
      <div id="head-top">
        <p id="logo-container">
          <a href="//epsg.io" title=""><span>Epsg.io</span> Coordinate Systems Worldwide</a>
        </p>
        <ul id="menu-top">
          <li><a href="/about" title="">About</a></li>
        </ul>
      </div>
    </div>
    <div id="reproject_map_container">
      <input type="checkbox" id="reproject_map" /><label for="reproject_map">Reproject Map <span class="beta">beta</span></label>
    </div>
    <div id="map-clipboard-container">
      <div id="mc-info-container">
        <h1 id="crs-title">Choose coordinate system</h1>
        <p>
          <a href="#" id="crs-change" class="btn">Change</a>
          <a id="crs-detail-link" class="btn-dark" href="#" title="">Details</a>
          <a id="crs-transform-link" class="btn-dark" href="/transform" title="">Transform</a>
        </p>
      </div>
      <div id="copy-clipboard-container">
        <p>
          <form id="eastnorth_form" method="post" action="#">
            <input id="easting" type="text" name="easting" value="" />
            <input id="northing" type="text" name="northing" value="" />
            <a id="eastnorth_copy" href="#" title="">Copy<span> to clipboard</span></a>
            <input type="submit" id="eastnorth_submit" value="">
          </form>
        </p>
      </div>
    </div>
    </div>
    <script type="text/javascript">
      new MapPage;
    </script>
  </body>
</html>
