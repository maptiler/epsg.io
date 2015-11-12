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
        if (this.srsIn_ && this.srsOut_) {
          this.jsonp_.send({
            'x': parseFloat(this.srsInX_.value),
            'y': parseFloat(this.srsInY_.value),
            's_srs': this.srsIn_['code'],
            't_srs': this.srsOut_['code']
          }, goog.bind(function(data) {
            this.srsOutX_.value = data['x'];
            this.srsOutY_.value = data['y'];
          }, this));
        } else {
          kt.alert('Select coordinate systems before transforming!', 'Error');
        }

        e.preventDefault();
      }, false, this);
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

  this.srsOutX_.value = '';
  this.srsOutY_.value = '';
};


goog.exportSymbol('TransformPage', epsg.io.TransformPage);
