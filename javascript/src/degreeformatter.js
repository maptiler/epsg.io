/**
 *
 * @author petr.sloup@klokantech.com (Petr Sloup)
 *
 * Copyright 2015 Klokan Technologies Gmbh (www.klokantech.com)
 */

goog.provide('epsg.io.DegreeFormatter');
goog.provide('epsg.io.DegreeFormatter.EventType');
goog.provide('epsg.io.DegreeFormatter.Format');

goog.require('goog.events.EventTarget');
goog.require('goog.events.EventType');



/**
 * @constructor
 * @extends {goog.events.EventTarget}
 */
epsg.io.DegreeFormatter = function() {
  goog.base(this);

  /**
   * @type {!HTMLSelectElement}
   * @private
   */
  this.formatElement_ = /** @type {!HTMLSelectElement} */
                        (goog.dom.getElement('lonlat_format'));

  /**
   * @type {epsg.io.DegreeFormatter.Format}
   * @private
   */
  this.format_ = epsg.io.DegreeFormatter.Format.DECIMAL;

  /**
   * @type {!HTMLSelectElement}
   * @private
   */
  this.lonSignEl_ = /** @type {!HTMLSelectElement} */
      (goog.dom.getElement('longitude_sign'));

  /**
   * @type {!HTMLSelectElement}
   * @private
   */
  this.latSignEl_ = /** @type {!HTMLSelectElement} */
      (goog.dom.getElement('latitude_sign'));

  /**
   * @type {!HTMLInputElement}
   * @private
   */
  this.lonDegEl_ = /** @type {!HTMLInputElement} */
                   (goog.dom.getElement('longitude_d'));

  /**
   * @type {!HTMLInputElement}
   * @private
   */
  this.latDegEl_ = /** @type {!HTMLInputElement} */
                   (goog.dom.getElement('latitude_d'));

  /**
   * @type {!HTMLInputElement}
   * @private
   */
  this.lonMinEl_ = /** @type {!HTMLInputElement} */
                   (goog.dom.getElement('longitude_m'));

  /**
   * @type {!HTMLInputElement}
   * @private
   */
  this.latMinEl_ = /** @type {!HTMLInputElement} */
                   (goog.dom.getElement('latitude_m'));

  /**
   * @type {!HTMLInputElement}
   * @private
   */
  this.lonSecEl_ = /** @type {!HTMLInputElement} */
                   (goog.dom.getElement('longitude_s'));

  /**
   * @type {!HTMLInputElement}
   * @private
   */
  this.latSecEl_ = /** @type {!HTMLInputElement} */
                   (goog.dom.getElement('latitude_s'));

  this.lonlatFormElement_ = goog.dom.getElement('lonlat_form');
  goog.events.listen(this.lonlatFormElement_, goog.events.EventType.SUBMIT,
      function(e) {
        this.dispatchChange_();
        e.preventDefault();
      }, false, this);

  [
    this.lonSignEl_, this.lonDegEl_, this.lonMinEl_, this.lonSecEl_,
    this.latSignEl_, this.latDegEl_, this.latMinEl_, this.latSecEl_
  ].forEach(function(el) {
    goog.events.listen(el, [goog.events.EventType.CHANGE,
                            goog.events.EventType.INPUT], function(e) {
      this.dispatchChange_();
      e.preventDefault();
    }, false, this);
  }, this);


  goog.events.listen(this.formatElement_, goog.events.EventType.CHANGE,
      function(e) {
        this.updateFormat_();
        this.dispatchEvent(epsg.io.DegreeFormatter.EventType.FORMAT_CHANGE);
      }, false, this);
  this.updateFormat_();
};
goog.inherits(epsg.io.DegreeFormatter, goog.events.EventTarget);


/**
 * @param {?number} lon
 * @param {?number} lat
 */
epsg.io.DegreeFormatter.prototype.setLonLat = function(lon, lat) {
  if (this.format_ == epsg.io.DegreeFormatter.Format.DECIMAL ||
      goog.isNull(lon) || goog.isNull(lat)) {
    this.lonDegEl_.value = goog.isNull(lon) ? '' : lon.toFixed(7);
    this.latDegEl_.value = goog.isNull(lat) ? '' : lat.toFixed(7);
    this.lonMinEl_.value = '';
    this.latMinEl_.value = '';
    this.lonSecEl_.value = '';
    this.latSecEl_.value = '';
  } else {
    this.lonSignEl_.value = lon > 0 ? '+' : '-';
    this.latSignEl_.value = lat > 0 ? '+' : '-';
    lon = Math.abs(lon);
    lat = Math.abs(lat);
    this.lonDegEl_.value = Math.floor(lon).toFixed(0);
    this.latDegEl_.value = Math.floor(lat).toFixed(0);
    lon = 60 * (lon % 1);
    lat = 60 * (lat % 1);
    if (this.format_ == epsg.io.DegreeFormatter.Format.DM) {
      this.lonMinEl_.value = lon.toFixed(6);
      this.latMinEl_.value = lat.toFixed(6);
      this.lonSecEl_.value = '';
      this.latSecEl_.value = '';
    } else {
      this.lonMinEl_.value = Math.floor(lon).toFixed(0);
      this.latMinEl_.value = Math.floor(lat).toFixed(0);
      this.lonSecEl_.value = (60 * (lon % 1)).toFixed(2);
      this.latSecEl_.value = (60 * (lat % 1)).toFixed(2);
    }
  }
};


/**
 * @return {Array.<number>}
 */
epsg.io.DegreeFormatter.prototype.getLonLat = function() {
  var longitude = goog.string.toNumber(this.lonDegEl_.value);
  var latitude = goog.string.toNumber(this.latDegEl_.value);

  if (this.format_ !== epsg.io.DegreeFormatter.Format.DECIMAL) {
    longitude += goog.string.toNumber(this.lonMinEl_.value) / 60;
    latitude += goog.string.toNumber(this.latMinEl_.value) / 60;

    if (this.format_ == epsg.io.DegreeFormatter.Format.DMS) {
      longitude += goog.string.toNumber(this.lonSecEl_.value) / 3600;
      latitude += goog.string.toNumber(this.latSecEl_.value) / 3600;
    }

    if (this.lonSignEl_.value == '-') longitude *= -1;
    if (this.latSignEl_.value == '-') latitude *= -1;
  }
  return [longitude, latitude];
};


/**
 * @return {epsg.io.DegreeFormatter.Format}
 */
epsg.io.DegreeFormatter.prototype.getFormat = function() {
  return this.format_;
};


/**
 * @param {epsg.io.DegreeFormatter.Format} format
 */
epsg.io.DegreeFormatter.prototype.setFormat = function(format) {
  this.formatElement_.value = format;
  this.updateFormat_();
};


/**
 * @private
 */
epsg.io.DegreeFormatter.prototype.dispatchChange_ = function() {
  var ll = this.getLonLat();
  if (!isNaN(ll[0]) && !isNaN(ll[1])) {
    this.dispatchEvent({
      type: epsg.io.DegreeFormatter.EventType.CHANGE,
      lonlat: ll
    });
  }
};


/**
 * @private
 */
epsg.io.DegreeFormatter.prototype.updateFormat_ = function() {
  var lonlat = this.getLonLat();

  this.format_ =
      /** @type {epsg.io.DegreeFormatter.Format} */
      (this.formatElement_.value || epsg.io.DegreeFormatter.Format.DECIMAL);
  goog.dom.classlist.set(this.lonlatFormElement_, this.format_);
  var showSecs = this.format_ == epsg.io.DegreeFormatter.Format.DMS;
  var showMins = showSecs || this.format_ == epsg.io.DegreeFormatter.Format.DM;

  goog.style.setElementShown(this.lonSecEl_, showSecs);
  goog.style.setElementShown(this.latSecEl_, showSecs);
  goog.style.setElementShown(this.lonMinEl_, showMins);
  goog.style.setElementShown(this.latMinEl_, showMins);

  this.setLonLat(lonlat[0], lonlat[1]);
};


/**
 * @enum {string}
 */
epsg.io.DegreeFormatter.EventType = {
  CHANGE: goog.events.EventType.CHANGE,
  FORMAT_CHANGE: 'format_change'
};


/**
 * @enum {string}
 */
epsg.io.DegreeFormatter.Format = {
  DECIMAL: 'dec',
  DM: 'dm',
  DMS: 'dms'
};
