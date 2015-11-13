/**
 *
 * @author petr.sloup@klokantech.com (Petr Sloup)
 *
 * Copyright 2015 Klokan Technologies Gmbh (www.klokantech.com)
 */

goog.provide('epsg.io.TransformPage');

goog.require('epsg.io.SRSPopup');
goog.require('goog.Uri.QueryData');
goog.require('goog.dom');
goog.require('goog.net.Jsonp');
goog.require('kt.alert');



/**
 * @constructor
 */
epsg.io.TransformPage = function() {
  /**
   * @type {!goog.net.Jsonp}
   * @private
   */
  this.jsonp_ = new goog.net.Jsonp('/trans');

  this.srsPopup_ = new epsg.io.SRSPopup();

  this.srsInName_ = goog.dom.getElement('srs-in-name');
  this.srsInChange_ = goog.dom.getElement('srs-in-change');
  this.srsOutName_ = goog.dom.getElement('srs-out-name');
  this.srsOutChange_ = goog.dom.getElement('srs-out-change');

  this.srsIn_ = null;
  this.srsOut_ = null;

  this.keepHash_ = true;

  goog.events.listen(this.srsInChange_, goog.events.EventType.CLICK,
      function(e) {
        goog.events.removeAll(this.srsPopup_);
        this.srsPopup_.listenOnce(epsg.io.SRSPopup.EventType.SRS_SELECTED,
            function(e) {
              if (e.data) {
                this.srsIn_ = e.data;
                this.handleSRSChange_();
              }
            }, false, this);
        this.srsPopup_.show();
        e.preventDefault();
      }, false, this);

  goog.events.listen(this.srsOutChange_, goog.events.EventType.CLICK,
      function(e) {
        goog.events.removeAll(this.srsPopup_);
        this.srsPopup_.listenOnce(epsg.io.SRSPopup.EventType.SRS_SELECTED,
            function(e) {
              if (e.data) {
                this.srsOut_ = e.data;
                this.handleSRSChange_();
              }
            }, false, this);
        this.srsPopup_.show();
        e.preventDefault();
      }, false, this);



  this.srsInX_ = goog.dom.getElement('srs-in-x');
  this.srsInY_ = goog.dom.getElement('srs-in-y');
  this.srsOutX_ = goog.dom.getElement('srs-out-x');
  this.srsOutY_ = goog.dom.getElement('srs-out-y');

  this.srsTransform_ = goog.dom.getElement('srs-transform');

  goog.events.listen(this.srsTransform_, goog.events.EventType.CLICK,
      function(e) {
        this.transform_(true);
        e.preventDefault();
      }, false, this);

  this.parseHash_(goog.bind(function() {
    this.keepHash_ = false;
  }, this));
};


/**
 * @private
 */
epsg.io.TransformPage.prototype.handleSRSChange_ = function() {
  if (this.srsIn_) {
    goog.dom.setTextContent(this.srsInName_, 'EPSG:' + this.srsIn_['code']);
  }

  if (this.srsOut_) {
    goog.dom.setTextContent(this.srsOutName_, 'EPSG:' + this.srsOut_['code']);
  }

  this.transform_();
};


/**
 * @param {boolean=} opt_manual Did the user initiate this?
 * @private
 */
epsg.io.TransformPage.prototype.transform_ = function(opt_manual) {
  this.srsOutX_.value = '';
  this.srsOutY_.value = '';
  if (this.srsIn_ && this.srsOut_) {
    var x = parseFloat(this.srsInX_.value);
    var y = parseFloat(this.srsInY_.value);
    if (goog.math.isFiniteNumber(x) && goog.math.isFiniteNumber(y)) {
      this.jsonp_.send({
        'x': x,
        'y': y,
        's_srs': this.srsIn_['code'],
        't_srs': this.srsOut_['code']
      }, goog.bind(function(data) {
        this.srsOutX_.value = data['x'];
        this.srsOutY_.value = data['y'];
      }, this));
    }
  } else if (opt_manual) {
    kt.alert('Select coordinate systems before transforming!', 'Error');
  }
  this.updateHash_();
};


/**
 * @private
 */
epsg.io.TransformPage.prototype.updateHash_ = function() {
  if (this.keepHash_) return;
  var qd = new goog.Uri.QueryData();

  if (this.srsIn_) {
    qd.set('s_srs', this.srsIn_['code']);
  }
  if (this.srsOut_) {
    qd.set('t_srs', this.srsOut_['code']);
  }

  var x = parseFloat(this.srsInX_.value);
  var y = parseFloat(this.srsInY_.value);
  if (goog.math.isFiniteNumber(x) && goog.math.isFiniteNumber(y)) {
    qd.set('x', x);
    qd.set('y', y);
  }
  window['console']['log'](qd.toString());
  window.location.hash = qd.toString();
};


/**
 * @param {Function} callback Called when transforms from the hash are loaded.
 * @private
 */
epsg.io.TransformPage.prototype.parseHash_ = function(callback) {
  var qd = new goog.Uri.QueryData(window.location.hash.substr(1));

  var toBeLoaded = 0;

  var s_srs = qd.get('s_srs');
  if (s_srs) {
    toBeLoaded++;
    this.srsPopup_.getSRS(/** @type {string} */(s_srs),
        goog.bind(function(data) {
          this.srsIn_ = data;
          this.handleSRSChange_();
          if (--toBeLoaded <= 0) callback();
        }, this));
  }
  var t_srs = qd.get('t_srs');
  if (t_srs) {
    toBeLoaded++;
    this.srsPopup_.getSRS(/** @type {string} */(t_srs),
        goog.bind(function(data) {
          this.srsOut_ = data;
          this.handleSRSChange_();
          if (--toBeLoaded <= 0) callback();
        }, this));
  }

  var x = parseFloat(qd.get('x')), y = parseFloat(qd.get('y'));
  if (goog.math.isFiniteNumber(x) && goog.math.isFiniteNumber(y)) {
    this.srsInX_.value = x;
    this.srsInY_.value = y;
  }
};

goog.exportSymbol('TransformPage', epsg.io.TransformPage);
