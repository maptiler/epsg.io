goog.provide('epsg.io');

goog.require('epsg.io.Coordinates');
goog.require('goog.array');
goog.require('goog.dom.classes');
goog.require('goog.net.Jsonp');
goog.require('goog.style');


/**
 * The Home page javascript
 */
epsg.io.home_init = function() {

  // Cursor into search box
  var qi = goog.dom.getElement('q');
  if (qi) qi.focus();

  // Client side GeoIP country detection with
  // http://freegeoip.net/json/?callback=asfasd
  var jsonp = new goog.net.Jsonp('http://freegeoip.net/json/');
  jsonp.send({}, function(result) {
    if (!result['country_name']) return;
    var q = result['country_name'];
    if (result['country_code'] == 'US') q = result['region_name'];
    goog.dom.getElement('country').innerHTML = q;
    goog.dom.getElement('countryLink').href =
        'http://epsg.io/?q=' + encodeURIComponent(q);
    goog.dom.getElement('countryLink').style.display = 'inline';
  });

};


/**
 * The Results page javascript
 */
epsg.io.results_init = function() {
};


/**
 * The Detail page javascript
 */
epsg.io.detail_init = function() {

  // Show / hide deprecated transformations
  var tdl = goog.dom.getElement('trans_deprecated_link');
  if (tdl) {
    goog.events.listen(tdl, goog.events.EventType.CLICK, function(e) {
      e.preventDefault();
      var d = goog.dom.getElement('trans_deprecated');
      if (d.style.display == 'block') {
        d.style.display = 'none';
        tdl.innerHTML = 'Show deprecated transformations';
      } else {
        d.style.display = 'block';
        tdl.innerHTML = 'Hide deprecated transfortmations';
      }
    });
  }


  var switcherClicked = function(e) {
    e.preventDefault();
    var future_switcher = e.target; // Clicked element
    var future_code = goog.dom.getElement(future_switcher.id + '_code');
    var old_switcher = goog.dom.getElementByClass('switcher_selected');
    var old_code = goog.dom.getElementByClass('code_visible');
    goog.dom.classes.remove(old_switcher, 'switcher_selected');
    goog.dom.classes.remove(old_code, 'code_visible');
    goog.dom.classes.add(future_switcher, 'switcher_selected');
    goog.dom.classes.add(future_code, 'code_visible');
  };
  goog.array.forEach(goog.dom.getElementsByClass('switcher'), function(e) {
    goog.events.listen(e, goog.events.EventType.CLICK, switcherClicked);
  });

  var ZeroClipboard = window['ZeroClipboard'];
  ZeroClipboard['config']({ 'moviePath': '/js/ZeroClipboard.swf' });

  // Put zeroclipboard on all elements with "zeroclipboard" class
  goog.array.forEach(goog.dom.getElementsByClass('zeroclipboard'),
      function(element) { new ZeroClipboard(element); });

};


/**
 * The Map page javascript
 * @param {!string} srs Spatial Reference System (usually EPSG code)
 * @param {number=} opt_lon Longitude of map center (defaults to 0)
 * @param {number=} opt_lat Latitude of map center (defaults to 0)
 */
epsg.io.map_init = function(srs, opt_lon, opt_lat) {
  new epsg.io.Coordinates(srs, opt_lon, opt_lat);
};

goog.exportSymbol('home_init', epsg.io.home_init);
goog.exportSymbol('results_init', epsg.io.results_init);
goog.exportSymbol('detail_init', epsg.io.detail_init);
goog.exportSymbol('map_init', epsg.io.map_init);
