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
goog.require('goog.net.cookies');
goog.require('goog.style');
goog.require('kt.CoordinateInput');
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

  this.srsInDetails_ = goog.dom.getElement('srs-in-details');
  this.srsInDetailsLink_ = goog.dom.getElement('srs-in-details-link');
  this.srsInUnit_ = goog.dom.getElement('srs-in-unit');
  this.srsInArea_ = goog.dom.getElement('srs-in-area');
  this.srsInAccuracy_ = goog.dom.getElement('srs-in-accuracy');


  this.srsOutName_ = goog.dom.getElement('srs-out-name');
  this.srsOutChange_ = goog.dom.getElement('srs-out-change');

  this.srsOutDetails_ = goog.dom.getElement('srs-out-details');
  this.srsOutDetailsLink_ = goog.dom.getElement('srs-out-details-link');
  this.srsOutUnit_ = goog.dom.getElement('srs-out-unit');
  this.srsOutArea_ = goog.dom.getElement('srs-out-area');
  this.srsOutAccuracy_ = goog.dom.getElement('srs-out-accuracy');


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


  this.srsInX_ = new kt.CoordinateInput('srs-in-x');
  this.srsInY_ = new kt.CoordinateInput('srs-in-y');
  this.srsOutX_ = new kt.CoordinateInput('srs-out-x');
  this.srsOutY_ = new kt.CoordinateInput('srs-out-y');

  this.srsInForm_ = goog.dom.getElement('srs-in-form');

  goog.events.listen(this.srsInForm_, goog.events.EventType.SUBMIT,
      function(e) {
        this.transform_(true);
        e.preventDefault();
      }, false, this);

  this.srsSwap_ = goog.dom.getElement('srs-swap');
  goog.events.listen(this.srsSwap_, goog.events.EventType.CLICK,
      function(e) {
        var tmpSrs = this.srsOut_;
        this.srsOut_ = this.srsIn_;
        this.srsIn_ = tmpSrs;

        this.srsInX_.setValue(this.srsOutX_.getValue());
        this.srsInY_.setValue(this.srsOutY_.getValue());

        this.handleSRSChange_();

        e.preventDefault();
      }, false, this);

  var formatOrder = [
    kt.CoordinateInput.DegreeFormat.DMS,
    kt.CoordinateInput.DegreeFormat.DM,
    kt.CoordinateInput.DegreeFormat.DECIMAL
  ];
  var inFormat = 0, outFormat = 0;
  this.srsInFormat_ = goog.dom.getElement('srs-in-format');
  this.srsOutFormat_ = goog.dom.getElement('srs-out-format');
  goog.events.listen(this.srsInFormat_, goog.events.EventType.CLICK,
      function(e) {
        inFormat = (inFormat + 1) % 3;
        var format = formatOrder[inFormat];
        this.srsInFormat_.value = 'Format: ' + format;
        this.srsInX_.setDegreeFormat(format);
        this.srsInY_.setDegreeFormat(format);
        e.preventDefault();
      }, false, this);
  goog.events.listen(this.srsOutFormat_, goog.events.EventType.CLICK,
      function(e) {
        outFormat = (outFormat + 1) % 3;
        var format = formatOrder[outFormat];
        this.srsOutFormat_.value = 'Format: ' + format;
        this.srsOutX_.setDegreeFormat(format);
        this.srsOutY_.setDegreeFormat(format);
        e.preventDefault();
      }, false, this);

  this.parseHash_(goog.bind(function() {
    this.keepHash_ = false;
    this.updateHash_();
  }, this));
};


/**
 * @private
 */
epsg.io.TransformPage.prototype.updateMapLinks_ = function() {
  var inLink = goog.dom.getElement('srs-in-map-link');
  if (this.srsIn_ && this.srsInX_.hasValue() && this.srsInY_.hasValue()) {
    inLink.href = '/map#srs=' + this.srsIn_['code'] +
                  '&x=' + this.srsInX_.getValue() +
                  '&y=' + this.srsInY_.getValue();
    inLink.style.display = '';
  } else {
    inLink.style.display = 'none';
  }

  var outLink = goog.dom.getElement('srs-out-map-link');
  if (this.srsOut_ && this.srsOutX_.hasValue() && this.srsOutY_.hasValue()) {
    outLink.href = '/map#srs=' + this.srsOut_['code'] +
        '&x=' + this.srsOutX_.getValue() +
        '&y=' + this.srsOutY_.getValue();
    outLink.style.display = '';
  } else {
    outLink.style.display = 'none';
  }
};


/**
 * @private
 */
epsg.io.TransformPage.prototype.handleSRSChange_ = function() {
  if (this.srsIn_) {
    goog.dom.setTextContent(this.srsInName_,
        'EPSG:' + this.srsIn_['code'] + ' ' + this.srsIn_['name']);
    var isDegrees = /^degree/.test(this.srsIn_['unit']);
    this.srsInX_.enableDegrees(isDegrees);
    this.srsInY_.enableDegrees(isDegrees);

    goog.style.setElementShown(this.srsInFormat_, isDegrees);

    this.srsInDetailsLink_.href = '/' + this.srsIn_['code'];
    goog.dom.setTextContent(this.srsInUnit_, this.srsIn_['unit']);
    goog.dom.setTextContent(this.srsInArea_, this.srsIn_['area']);
    var acc = this.srsIn_['accuracy'];
    goog.dom.setTextContent(this.srsInAccuracy_, acc ? acc + ' m' : 'Unknown');
  }
  goog.style.setElementShown(this.srsInDetails_, this.srsIn_);

  if (this.srsOut_) {
    goog.dom.setTextContent(this.srsOutName_,
        'EPSG:' + this.srsOut_['code'] + ' ' + this.srsOut_['name']);
    var isDegrees = /^degree/.test(this.srsOut_['unit']);
    this.srsOutX_.enableDegrees(isDegrees);
    this.srsOutY_.enableDegrees(isDegrees);

    goog.style.setElementShown(this.srsOutFormat_, isDegrees);

    this.srsOutDetailsLink_.href = '/' + this.srsOut_['code'];
    goog.dom.setTextContent(this.srsOutUnit_, this.srsOut_['unit']);
    goog.dom.setTextContent(this.srsOutArea_, this.srsOut_['area']);
    var acc = this.srsOut_['accuracy'];
    goog.dom.setTextContent(this.srsOutAccuracy_, acc ? acc + ' m' : 'Unknown');
  }
  goog.style.setElementShown(this.srsOutDetails_, this.srsOut_);

  this.srsSwap_.disabled = !(this.srsIn_ && this.srsOut_);

  this.transform_();
};


/**
 * @param {boolean=} opt_manual Did the user initiate this?
 * @private
 */
epsg.io.TransformPage.prototype.transform_ = function(opt_manual) {
  this.srsOutX_.setValue(NaN);
  this.srsOutY_.setValue(NaN);
  if (this.srsIn_ && this.srsOut_) {
    var x = this.srsInX_.getValue();
    var y = this.srsInY_.getValue();
    if (goog.math.isFiniteNumber(x) && goog.math.isFiniteNumber(y)) {
      this.jsonp_.send({
        'x': x,
        'y': y,
        's_srs': this.srsIn_['code'],
        't_srs': this.srsOut_['code']
      }, goog.bind(function(data) {
        if (opt_manual && data['status'] == 'error') {
          kt.alert(data['message'], 'Error (' + data['error_type'] + ')');
        }
        if (goog.isDef(data['x']) && goog.isDef(data['x'])) {
          this.srsOutX_.setValue(data['x']);
          this.srsOutY_.setValue(data['y']);
          this.updateMapLinks_();
        }
      }, this));
    } else if (opt_manual) {
      kt.alert('Please enter valid input coordinates!', 'Error');
    }
  } else if (opt_manual) {
    kt.alert('Select coordinate systems before transforming!', 'Error');
  }
  this.updateHash_();
  this.updateMapLinks_();

  this.srsInX_.reformatValue();
  this.srsInY_.reformatValue();
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
    goog.net.cookies.set('t_srs', this.srsOut_['code'], 365 * 24 * 60 * 60);
  }

  var x = this.srsInX_.getValue();
  var y = this.srsInY_.getValue();
  if (goog.math.isFiniteNumber(x) && goog.math.isFiniteNumber(y)) {
    qd.set('x', x.toFixed(7));
    qd.set('y', y.toFixed(7));
  }
  window.location.hash = qd.toString();
};


/**
 * @param {Function} callback Called when transforms from the hash are loaded.
 * @private
 */
epsg.io.TransformPage.prototype.parseHash_ = function(callback) {
  var qd = new goog.Uri.QueryData(window.location.hash.substr(1));

  var s_srs = qd.get('s_srs');
  var t_srs = qd.get('t_srs') || goog.net.cookies.get('t_srs');
  if (!t_srs && !s_srs) {
    s_srs = '4326';
    t_srs = '3857';
  } else if (!s_srs) {
    s_srs = (t_srs == '4326') ? '3857' : '4326';
  } else if (!t_srs) {
    t_srs = (s_srs == '4326') ? '3857' : '4326';
  }

  var toBeLoaded = 2;

  this.srsPopup_.getSRS(/** @type {string} */(s_srs),
      goog.bind(function(data) {
        this.srsIn_ = data;
        this.handleSRSChange_();
        if (--toBeLoaded <= 0) callback();
      }, this));
  this.srsPopup_.getSRS(/** @type {string} */(t_srs),
      goog.bind(function(data) {
        this.srsOut_ = data;
        this.handleSRSChange_();
        if (--toBeLoaded <= 0) callback();
      }, this));

  var x = parseFloat(qd.get('x')), y = parseFloat(qd.get('y'));
  if (goog.math.isFiniteNumber(x) && goog.math.isFiniteNumber(y)) {
    this.srsInX_.setValue(x);
    this.srsInY_.setValue(y);
  }
};

goog.exportSymbol('TransformPage', epsg.io.TransformPage);
