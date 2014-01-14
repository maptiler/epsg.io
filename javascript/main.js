goog.provide('epsg.io.main');

goog.require('epsg.io.Coordinates');

goog.require('goog.net.Jsonp');


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
