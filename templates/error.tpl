<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"  lang="en" xml:lang="en">
  <head>  
    <meta charset="utf-8"/>
    <title>EPSG.io: Coordinate Systems Worldwide</title>
    <meta content="width=device-width, initial-scale=1, maximum-scale=1" name="viewport" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="keywords" content="EPSG.io" />
    <meta name="robots" content="ALL,FOLLOW" />
    <meta property="og:image" content="http://epsg.io/img/epsg-banner-440x280-2.png"/>
    <link rel="stylesheet" href="/css/main.css" type="text/css" />
    <link rel="shortcut icon" href="/favicon.ico" />

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
 
 <body id="errorpage" data-role="page">
   <div id="head">
     <p id="logo-container">
       <a href="http://epsg.io" title=""><span>Epsg.io</span> Coordinate Systems Worldwide</a>
     </p>
     <ul id="menu-top">
       <li><a href="/about" title="">About</a></li>
     </ul>
   </div>
   
   <div id="layout-container">
      %if error == 404:
        <h1>Sorry, that page cannot be found.</h1>
      %else:
        <h1>Something went wrong.</h1>
        <p>{{error}}</p>
      %end
      
      %if try_url:
        <h2>Try to searching below or go to <a href="{{try_url}}">GML</a></h2>
      %else:
        <h2>Try to searching below or go to <a href="http://epsg.io">epsg.io</a></h2>
      %end
     
     <div id="error-content-container">
       <div id="search-container">
         <form action="/" method="get">
           <p><input id="q" name="q" type="search" placeholder="Country, code or name of a coordinate system" /> <input type="submit" name="" value="search" /></p>
         </form>
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
        <p id="mzk-logo">
          <a href="http://www.mzk.cz/" title=""><img src="./img/hzk-logo.png" alt="" /></a>
        </p>
        <p>Find a coordinate system and get position on a map.</p>
        <p id="copyright">Copyright &copy; 2014</p>
      </div>
    </div>

  </body>

</html>