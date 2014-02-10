/**
 * EPSG.io Coordinates JavaScript App
 * ----------------------------------
 * Copyright (C) 2013 - Moravian Library, http://www.mzk.cz/
 * Copyright (C) 2014 - Klokan Technologies GmbH, http://www.klokantech.com/
 * All rights reserved.
 */

goog.provide('epsg.io.Coordinates');

goog.require('goog.Timer');
goog.require('goog.dom');
goog.require('goog.net.Jsonp');


/**
 * @type {string}
 * @const
 */
epsg.io.TRANS_SERVICE_URL = 'http://epsg.io/trans';



/**
 * The main Coordinates object
 * @param {!string} srs Spatial Reference System (usually EPSG code)
 * @param {Array.<number>} bbox [n,w,s,e]
 * @param {number=} opt_lon Longitude of map center (defaults to 0)
 * @param {number=} opt_lat Latitude of map center (defaults to 0)
 * @constructor
 */
epsg.io.Coordinates = function(srs, bbox, opt_lon, opt_lat) {

  // srs
  this.srs_ = srs || '4326';
  // lonlat - longitude and latitude
  this.lon_ = opt_lon || 0;
  this.lat_ = opt_lat || 0;
  // eastnoth
  this.east_ = 0;
  this.north_ = 0;

  // LOAD ALL THE EXPECTED ELEMENTS ON THE PAGE

  this.mapElement = /** @type {!Element} */(goog.dom.getElement('map'));

  this.geocoderElement = /** @type {!HTMLInputElement} */
      (goog.dom.getElement('geocoder'));

  this.latitudeElement = goog.dom.getElement('latitude');
  this.longitudeElement = goog.dom.getElement('longitude');
  this.lonlatFormElement = goog.dom.getElement('lonlat_form');

  this.eastingElement = goog.dom.getElement('easting');
  this.northingElement = goog.dom.getElement('northing');
  this.eastNorthFormElement = goog.dom.getElement('eastnorth_form');
  this.eastNorthCopyElement = goog.dom.getElement('eastnorth_copy');

  // Force preservation of user typed values on recalculation
  this.forceLonLat = false;
  this.forceEastNorth = false;

  /**
   * @type {?number}
   * @private
   */
  this.queryTimer_ = null;

  /**
   * @type {!goog.net.Jsonp}
   * @private
   */
  this.jsonp_ = new goog.net.Jsonp(epsg.io.TRANS_SERVICE_URL);

  var latlng = new google.maps.LatLng(this.lat_, this.lon_);
  // BoundingBox
  var swlatlng = new google.maps.LatLng(bbox[2], bbox[1]);
  var nelatlng = new google.maps.LatLng(bbox[0], bbox[3]);
  var bounds = new google.maps.LatLngBounds(swlatlng, nelatlng);
  var myOptions = {
    zoom: 8,
    center: latlng,
    tilt: 0,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    disableDefaultUI: true,
    zoomControl: true,
    zoomControlOptions: {
      // style: google.maps.ZoomControlStyle.SMALL,
      position: google.maps.ControlPosition.LEFT_CENTER
    },
    mapTypeControl: true,
    mapTypeControlOptions: {
      style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
      position: google.maps.ControlPosition.RIGHT_BOTTOM
    }
  };

  this.map = new google.maps.Map(this.mapElement, myOptions);

  //this.map.setCenter(bounds.getCenter());
  this.map.fitBounds(bounds);
  this.map.setCenter(latlng);
  google.maps.event.addListener(this.map, 'center_changed',
      goog.bind(function() {
        var pos = this.map.getCenter();
        var latitude_element = this.latitudeElement;
        var longitude_element = this.longitudeElement;
        this.lat_ = pos.lat();
        this.lon_ = pos.lng();
        if (!this.forceLonLat) {
          latitude_element.value = this.lat_;
          longitude_element.value = this.lon_;
        } else {
          this.forceLonLat = false;
        }
        if (!this.forceEastNorth) {
          this.makeQuery();
        } else {
          this.forceEastNorth = false;
        }
      }, this));


  this.map.setCenter(latlng);

  // The user can type latitude / longitude and hit Enter
  goog.events.listen(this.lonlatFormElement, goog.events.EventType.SUBMIT,
      goog.bind(function(e) {
        e.preventDefault();
        var latitude = goog.string.toNumber(this.latitudeElement.value);
        var longitude = goog.string.toNumber(this.longitudeElement.value);
        if (isNaN(latitude) || isNaN(longitude)) return;
        this.lat_ = latitude;
        this.lon_ = longitude;
        var newlatlng = new google.maps.LatLng(latitude, longitude);
        this.forceLonLat = true;
        this.map.setCenter(newlatlng);
      }, this));

  // The user can type easting / northing and hit Enter
  goog.events.listen(this.eastNorthFormElement, goog.events.EventType.SUBMIT,
      goog.bind(function(e) {
        e.preventDefault();
        var easting = goog.string.toNumber(this.eastingElement.value);
        var northing = goog.string.toNumber(this.northingElement.value);
        if (isNaN(easting) || isNaN(northing)) return;
        this.east_ = easting;
        this.north_ = northing;
        // Make the query to epsg.io/trans to get new lat/lon
        this.latitudeElement.value = '';
        this.longitudeElement.value = '';
        this.jsonp_.send({
          'x': this.east_, 'y': this.north_, 's_srs': this.srs_
        }, goog.bind(function(result) {
          var latitude = goog.string.toNumber(result['y']);
          var longitude = goog.string.toNumber(result['x']);
          var newlatlng = new google.maps.LatLng(latitude, longitude);
          this.latitudeElement.value = latitude;
          this.longitudeElement.value = longitude;
          this.forceEastNorth = true;
          this.forceLonLat = true;
          this.map.setCenter(newlatlng);
        }, this));
      }, this));


  // Geocoder via Places Search Box
  var searchbox = new google.maps.places.SearchBox(this.geocoderElement);

  google.maps.event.addListener(searchbox, 'places_changed',
      goog.bind(function() {
        var place = searchbox.getPlaces()[0];
        if (!place.geometry) {
          // on Enter key we can't help the user
          return;
        }
        this.geocoderElement.value = '';
        // If the place has a geometry, then present it on a map.
        if (place.geometry.viewport) {
          this.map.fitBounds(place.geometry.viewport);
        } else {
          this.map.setZoom(17);
        }
        this.map.setCenter(place.geometry.location);
      }, this));

  // Bias the SearchBox results towards places that are within the bounds of the
  // current map's viewport.
  google.maps.event.addListener(this.map, 'bounds_changed',
      goog.bind(function() {
        var bounds = this.map.getBounds();
        searchbox.setBounds(bounds);
      }, this));

  // ZeroClipboard initialization
  var ZeroClipboard = window['ZeroClipboard'];
  ZeroClipboard['config']({ 'moviePath': '/js/ZeroClipboard.swf' });
  this.eastNorthZeroClipboard = new ZeroClipboard(this.eastNorthCopyElement);

  this.eastNorthZeroClipboard['on']('dataRequested',
      goog.bind(function(client, args) {
        var eastNorthText = this.eastingElement.value + '\t' +
            this.northingElement.value;
        client['setText'](eastNorthText);
      }, this));

};


/**
 * The throttled call for the coordinates transformation via JSONP
 * @protected
 */
epsg.io.Coordinates.prototype.makeQuery = function() {

  this.eastingElement.value = '';
  this.northingElement.value = '';

  // If the timer has a waiting query, then trash it -
  // it is obsolete, because we have a new one
  if (this.queryTimer_) {
    goog.Timer.clear(this.queryTimer_);
    this.queryTimer_ = null;
  }

  // Don't proceed with the JSONP query immediatelly,
  //   but wait for 500 ms if the user doesn't make a new one.
  this.queryTimer_ = goog.Timer.callOnce(function() {
    var data = { 'x': this.lon_, 'y': this.lat_, 't_srs': this.srs_ };
    if (this.srs_ == '4326') // no need to transform
      this.showResult(data);
    else
      this.jsonp_.send(data, goog.bind(this.showResult, this));
  }, 500, this);
};


/**
 * Display results
 * @param {Object} result
 */
epsg.io.Coordinates.prototype.showResult = function(result) {

  if (!this.forceEastNorth) {
    // SHOW THE RESULT
    this.eastingElement.value = result.x;
    this.northingElement.value = result.y;
  }

  // Stop the timer
  this.queryTimer_ = null;
};
