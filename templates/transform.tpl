<!DOCTYPE html>
<html lang="en">
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
      (function(i, s, o, g, r, a, m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)}, i[r].l = 1 * new Date(); a = s.createElement(o),
              m = s.getElementsByTagName(o)[0]; a.async = 1; a.src = g; m.parentNode.insertBefore(a, m)
      })(window, document, 'script', '//www.google-analytics.com/analytics.js', '__gaTracker');
              __gaTracker('create', 'UA-47718358-1', 'epsg.io');
              __gaTracker('send', 'pageview');</script>
    <script src="/js/transform.js"></script>
    <style>
      .trans-box{
        width: 40%;
        margin: 0 10% 0 0;
        display: inline-block;
        float: left;
      }
      .trans-box.right{
        margin: 0 0 0 10%;
      }
      input, textarea{
        margin: 5px 0;
        display: inline-block;
        padding: 4px 5px;
      }
      input[type=text] {
        width:220px;
      }
      h3.underline-style{
        margin: 15px 0 10px 0;
      }

      #srs-in-form input[type=submit] {
        float:right;
        margin-top:-145px;
        margin-right: -150px;
      }
      #srs-swap {
        float:right;
        margin-right: -142px;
        margin-top:-100px;
      }

      #srs-in-change, #srs-out-change, #srs-in-details-link, #srs-out-details-link { color:#4295c5; }

      @media(max-width: 800px){
        .trans-box, .trans-box.right{
          width: 92%;
          margin: 0 2% 0 2%;
          display: inline-block;
          float: left;
        }
        #srs-in-form input[type=submit] {
          float: none;
          margin-top: 25px;
          margin-right: 0;
          display: block;
        }
        #srs-swap { float: none; margin-right: 0; margin-top: 0; display: block; margin: 8px;}
      }

      .srsdialog-input{
        margin: 0 10px 20px 0;
        padding: 0 10px;
        height: 28px;
        width: 200px;
        font-size: 11px;
        color: #989898;
        float: left;
        border: solid 1px #cacaca;
        border-radius: 15px;
      }

      .popup-bg{ position:fixed;top:0;bottom:0;left:0;right:0;background-color:rgba(55,55,55,0.8);z-index:101}
      .popup{ z-index:111;position:absolute;width:400px;min-height:100px;top:15%;left:50%;margin-left:-200px;padding:25px;background:#fff}
      .popup .popup-title{ display:block;padding:0 0 10px 0;font-size:26px;color: #000;font-family: OpenSansBold, Arial, "Geneva CE", lucida, sans-serif;font-weight: normal;}
      .popup .popup-close{ position:absolute;top:10px;right:10px;font-family:'epsg';cursor:pointer;color:#898989}
      .popup .popup-close:hover{ text-decoration:none;color:#565656; }
      .popup .popup-content{ display:block }
      .popup .popup-actions{ display:block;margin-top:20px }
      .popup .popup-actions div{ margin-right:10px }

      .srsdialog-table, .srsdialog-table td { border:1px solid #ccc;border-spacing:0;border-collapse:collapse;padding: 2px 5px;}
      .srsdialog-table tr { cursor:pointer;}
      .srsdialog-table tr.hidden { display:none;}
      .srsdialog-table tr:not(.expandable) .srsdialog-transshower { display:none;}
      .srsdialog-table tr.selected * { background:#4295c5;color:#fff;}
      .srsdialog-table tr.trans :first-child { padding-left:10px;}
      .srsdialog-table tr.trans.default { font-weight:bold;}
      .srsdialog-form{
        overflow-y: auto;
        height: 300px;
      }
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

        <h1>Transform coordinates</h1>
        <br /><br />
        <div class="trans-box">
          <h3 class="underline-style">Input coordinates</h3>
          <form id="srs-in-form">
            <label for="srs-in-x" data-value="X:" data-value-degrees="Longitude:">X:</label>
            <input type="text" id="srs-in-x" data-placeholder="Decimal value of X coordinate"
                   data-placeholder-degrees="e.g. 8°33'10&quot;, 8.55, 8 33 10" />
            <br>

            <label for="srs-in-y" data-value="Y:" data-value-degrees="Latitude:">Y:</label>
            <input type="text" id="srs-in-y" data-placeholder="Decimal value of Y coordinate"
                   data-placeholder-degrees="e.g. 47°22'00&quot;, 47.36666, 47 22 00" /><br /><br />



            <h3 class="underline-style">Input coordinate system</h3>
            <span id="srs-in-name">Not selected</span>
            <a href="#"n id="srs-in-change">Change</a>

            <div id="srs-in-details" style="display:none;">
              <h3 class="underline-style">Details</h3>
              <a id="srs-in-details-link" href="#" target="_blank">show more details</a><br /><br />
              <span class="caption">Unit: </span><span id="srs-in-unit"></span><br />
              <span class="caption">Area of use: </span><span id="srs-in-area"></span><br />
              <span class="caption">Accuracy: </span><span id="srs-in-accuracy"></span>
            </div>
            <input type="submit" value="Transform" class="btn" />
            <input type="button" id="srs-swap" value="Swap &#x21C4;"  class="btn-dark" />
          </form>


        </div>
        <div class="trans-box right">
          <h3 class="underline-style">Output</h3>

          <label for="srs-out-x" data-value="X:" data-value-degrees="Longitude:">X:</label>
          <input type="text" id="srs-out-x" data-placeholder="" data-placeholder-degrees="" readonly="readonly" />
          <br />

          <label for="srs-out-y" data-value="Y:" data-value-degrees="Latitude:">Y:</label>
          <input type="text" id="srs-out-y" data-placeholder="" data-placeholder-degrees="" readonly="readonly" />
          <br /><br />

          <h3 class="underline-style">Output coordinate system</h3>
          <span id="srs-out-name">Not selected</span>
          <a href="#"n id="srs-out-change">Change</a>

          <div id="srs-out-details" style="display:none;">
            <h3 class="underline-style">Details</h3>
            <a id="srs-out-details-link" href="#" target="_blank">show more details</a><br /><br />
            <span class="caption">Unit: </span><span id="srs-out-unit"></span><br />
            <span class="caption">Area of use: </span><span id="srs-out-area"></span><br />
            <span class="caption">Accuracy: </span><span id="srs-out-accuracy"></span>
          </div>
        </div>
      </div>

      <div id="spacer"><p></p></div>

    </div>

    <div id="footer">

      <script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
      <!-- EPSG.io -->
      <ins class="adsbygoogle"
           style="display:inline-block; width: 98%; max-width:728px;height:90px"
           data-ad-client="ca-pub-0328423815528922"
           data-ad-slot="6564733120"></ins>
      <script>
              (adsbygoogle = window.adsbygoogle || []).push({});</script>

      <div id="foot">
        <p id="klokan-logo">
          <a href="//www.klokantech.com/" title=""><img src="./img/klokan-logo-grey.png" alt="" /></a>
        </p>
        <p id="mzk-logo">
          <a href="//www.mzk.cz/" title=""><img src="./img/hzk-logo.png" alt="" /></a>
        </p>
        <p>Find a coordinate system and get position on a map. Powered by EPSG database {{version}}</p>
        <p id="copyright">Copyright &copy; 2015</p>
      </div>
    </div>
    <script type="text/javascript">
              new TransformPage;
    </script>
  </body>
</html>
