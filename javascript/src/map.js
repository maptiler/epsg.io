goog.provide('epsg.io.Map');

goog.require('epsg.io.Coordinates');


/**
 * The Map page javascript
 * @param {!string} srs Spatial Reference System (usually EPSG code)
 * @param {Array.<number>} bbox [n,w,s,e]
 * @param {number=} opt_lon Longitude of map center (defaults to 0)
 * @param {number=} opt_lat Latitude of map center (defaults to 0)
 */
epsg.io.Map.init = function(srs, bbox, opt_lon, opt_lat) {
  new epsg.io.Coordinates(srs, bbox, opt_lon, opt_lat);
};

goog.exportSymbol('map_init', epsg.io.Map.init);
