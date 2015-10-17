<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"  lang="en" xml:lang="en">
    <head>    
        <meta charset="utf-8"/>
        <title>WGS84 and {{name}} - transform coordinates for position on a map - converting latitude / longitude degrees</title>
        <meta content="width=device-width, initial-scale=1, maximum-scale=1" name="viewport" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="description" content="Transform coordinates for position on a map - converting latitude / longitude degrees" />
        <meta name="keywords" content="EPSG.io" />
        <meta name="robots" content="ALL,FOLLOW" />
        <link rel="stylesheet" href="/css/main.css" type="text/css" />
        <link rel="shortcut icon" href="//epsg.io/favicon.ico" />
        <link rel="search" href="/opensearch.xml" title="EPSG.io" type="application/opensearchdescription+xml"/>
        <script src="https://maps.googleapis.com/maps/api/js?sensor=false&amp;libraries=places"></script>
        <script src="/js/ZeroClipboard.min.js"></script>
        <script src="/js/index.js"></script>
    </head>
    <body id="mappage" data-role="page">
        <div id="map"></div>
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
            <div id="search-lat-lg-container">
                <div id="search-container">
                    <p><input type="search" name="geocoder" id="geocoder" placeholder="Place or address" /> <input type="submit" name="send" value="search" /></p>
                </div>
                <div id="lat-lg-container">
                    <form id="lonlat_form" method="post" action="#">
                    <p id="lg"><label for="longitude">Longitude:</labeL> <input id="longitude" name="longitude" value="0" /></p>
                    <p id="lat"><label for="latitude">Latitude:</label> <input id="latitude" name="latitude" value="0" /></p>
                    <input type="submit" id="lonlat_submit" value="">
                    </form>
                </div>
            </div>
        </div>
        <div id="map-clipboard-container">
                <div id="mc-info-container">
                    <h1>EPSG:{{code}} {{name}}</h1>
                    <p>
                        <a href="//epsg.io/" title="">Change coordinate system</a>
                        <a class="right" href="//epsg.io/{{url_coords}}" title="">Show details</a>
                    </p>
                </div>
                <div id="copy-clipboard-container">
                    <p>
                        <form id="eastnorth_form" method="post" action="#">
                        <input id="easting" type="text" name="easting" value="" />
                        <input id="northing" type="text" name="northing" value="" />
                        <a id="eastnorth_copy" href="#" title="">Copy to clipboard</a>
                        <input type="submit" id="lonlat_submit" value="">
                        </form>
                    </p>
                </div>
            </div>
        </div>
    <script type="text/javascript">
    
map_init('{{url_coords}}', {{bbox}}, {{center[1]}}, {{center[0]}});</script>
    </body>
</html>
