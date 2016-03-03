<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Transform coordinates - GPS online convertor</title>
    <meta content="width=device-width, initial-scale=1, maximum-scale=1" name="viewport" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="description" content="Transform your coordinates online easily with epsg.io" />
    <meta name="keywords" content="transform, coordinates, projection, geographic, geodethic, srs, crs, epsg.io" />
    <meta name="robots" content="ALL,FOLLOW" />
    <link rel="stylesheet" href="/css/main.css" type="text/css" />
    <link rel="shortcut icon" href="//epsg.io/favicon.ico" />
    <script>
      (function(i, s, o, g, r, a, m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)}, i[r].l = 1 * new Date(); a = s.createElement(o),
              m = s.getElementsByTagName(o)[0]; a.async = 1; a.src = g; m.parentNode.insertBefore(a, m)
      })(window, document, 'script', '//www.google-analytics.com/analytics.js', '__gaTracker');
      __gaTracker('create', 'UA-47718358-1', 'epsg.io');
      __gaTracker('send', 'pageview');</script>
    <script src="/js/transform.js"></script>
  </head>
  <body id="detailpage" data-role="page">
    <div id="head">
      <p id="logo-container">
        <a href="/" title=""><span>Epsg.io</span> Coordinate Systems Worldwide</a>
      </p>
      <ul id="menu-top">
        <li><a href="/map" title="">Map</a></li>
        <li><a href="/transform" title="">Transform</a></li>
        <li><a href="/about" title="">About</a></li>
      </ul>
    </div>

    <div id="layout-container">
      <div id="detail-content-container">

        <h1>Transform coordinates</h1>
        <h2>Online convertor for lat & long coordinates, geodetic datums and projected systems</h2>
        <br /><br />
        <div class="trans-box">
          <h3 class="underline-style">Input coordinate system</h3>
          <span id="srs-in-name">Not selected</span>
          <a href="#"n id="srs-in-change" class="">Change</a>
          <br><br>

          <h3 class="underline-style">Input coordinates <a href="#" style="display: none;">Batch</a></h3>
          <form id="srs-in-form">
            <input type="submit" value="Transform" class="btn" />
            <input type="button" id="srs-swap" value="Swap &#x21C4;"  class="btn-dark" />
            <label for="srs-in-x" data-value="X:" data-value-degrees="Longitude:">X:</label>
            <input type="text" id="srs-in-x" data-placeholder="Decimal value of X coordinate"
                   data-placeholder-degrees="e.g. 8°33'10&quot;, 8.55, 8 33 10" />
            <input type="button" id="srs-in-format" class="btn-dark small" style="display:none;" value="Format: D°M'S&quot;" />
            <br />
            <label for="srs-in-y" data-value="Y:" data-value-degrees="Latitude:">Y:</label>
            <input type="text" id="srs-in-y" data-placeholder="Decimal value of Y coordinate"
                   data-placeholder-degrees="e.g. 47°22'00&quot;, 47.36666, 47 22 00" />
            <textarea name="batch-in" style="display: none;"></textarea>
            <br /><br />
            <a id="srs-in-map-link" href="#" style="display:none;">Show position on a map</a>
            <br><br />

            <div id="srs-in-details" style="display:none;">
              <span class="caption">Unit: </span><span id="srs-in-unit"></span><br />
              <span class="caption">Area of use: </span><span id="srs-in-area"></span><br />
              <span class="caption">Accuracy: </span><span id="srs-in-accuracy"></span>
            </div>
            <br>
            <a id="srs-in-details-link" href="#" target="_blank">More details</a><br /><br />
          </form>
        </div>

        <div class="trans-box right">
          <h3 class="underline-style">Output coordinate system</h3>
          <span id="srs-out-name">Not selected</span>
          <a href="#"n id="srs-out-change">Change</a>
          <br><br>

          <h3 class="underline-style">Output coordinates</h3>

          <label for="srs-out-x" data-value="X:" data-value-degrees="Longitude:">X:</label>
          <input type="text" id="srs-out-x" data-placeholder="" data-placeholder-degrees="" readonly="readonly" />
          <input type="button" id="srs-out-format" class="btn-dark small" style="display:none;" value="Format: D°M'S&quot;" />
          <br />
          <label for="srs-out-y" data-value="Y:" data-value-degrees="Latitude:">Y:</label>
          <input type="text" id="srs-out-y" data-placeholder="" data-placeholder-degrees="" readonly="readonly" />
          <textarea name="batch-out" style="display: none;"></textarea>
          <br><br>
          <a id="srs-out-map-link" href="#" style="display:none;">Show position on a map</a>
          <br><br>

          <div id="srs-out-details" style="display:none;">
            <span class="caption">Unit: </span><span id="srs-out-unit"></span><br />
            <span class="caption">Area of use: </span><span id="srs-out-area"></span><br />
            <span class="caption">Accuracy: </span><span id="srs-out-accuracy"></span>
          </div>
          <br>
          <a id="srs-out-details-link" href="#" target="_blank">More details</a><br /><br />
        </div>
      </div>
      <script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
      <!-- EPSG.io -->
      <ins class="adsbygoogle"
           style="display:inline-block; width: 98%; max-width:728px;height:90px"
           data-ad-client="ca-pub-0328423815528922"
           data-ad-slot="6564733120"></ins>
      <script>
      (adsbygoogle = window.adsbygoogle || []).push({});
       </script>

    </div>

    <div id="footer">

      <div id="foot">
        <p id="klokan-logo">
          <a href="//www.klokantech.com/" title=""><img src="./img/klokan-logo-grey.png" alt="" /></a>
        </p>
        <p id="mzk-logo">
          <a href="//www.mzk.cz/" title=""><img src="./img/hzk-logo.png" alt="" /></a>
        </p>
        <p>Find a coordinate system and get position on a map. Powered by EPSG database {{version}}</p>
        <p id="copyright">Copyright &copy; 2016</p>
      </div>
    </div>
    <script type="text/javascript">
      new TransformPage;
    </script>
  </body>
</html>
