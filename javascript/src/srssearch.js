/**
 *
 * @author petr.sloup@klokantech.com (Petr Sloup)
 *
 * Copyright 2015 Klokan Technologies Gmbh (www.klokantech.com)
 */

goog.provide('epsg.io.SRSSearch');
goog.provide('epsg.io.SRSSearch.EventType');

goog.require('goog.dom');
goog.require('goog.events.EventTarget');
goog.require('goog.net.Jsonp');
goog.require('goog.ui.ac.AutoComplete');
goog.require('goog.ui.ac.InputHandler');
goog.require('goog.ui.ac.Renderer');



/**
 * @param {!Element|string} inputElement
 * @param {string=} opt_rendererClass Class to add to the rendered list.
 * @param {boolean=} opt_upsideDown
 * @constructor
 * @extends {goog.events.EventTarget}
 */
epsg.io.SRSSearch = function(inputElement, opt_rendererClass, opt_upsideDown) {
  goog.base(this);

  /**
   * @type {!Element}
   * @private
   */
  this.inputEl_ = /** @type {!Element} */(goog.dom.getElement(inputElement));

  /**
   * @type {!goog.net.Jsonp}
   * @private
   */
  this.jsonp_ = new goog.net.Jsonp(epsg.io.SRSSearch.SERVICE_URL);

  /**
   * @type {!goog.ui.ac.Renderer}
   * @private
   */
  this.renderer_ = new goog.ui.ac.Renderer(null, this);
  if (opt_rendererClass) this.renderer_.className += ' ' + opt_rendererClass;

  /**
   * @type {!goog.ui.ac.InputHandler}
   * @private
   */
  this.handler_ = new goog.ui.ac.InputHandler(null, null, false);

  /**
   * @type {goog.ui.ac.AutoComplete}
   * @private
   */
  this.autocomplete_ = new goog.ui.ac.AutoComplete(
      this, this.renderer_, this.handler_);

  this.handler_.setThrottleTime(300);
  this.handler_.attachAutoComplete(this.autocomplete_);
  this.handler_.attachInputs(this.inputEl_);

  this.renderer_.setTopAlign(opt_upsideDown || false);
  this.handler_.setUpsideDown(opt_upsideDown || false);

  goog.events.listen(this.autocomplete_,
      goog.ui.ac.AutoComplete.EventType.UPDATE, function(e) {
        this.dispatchEvent({
          type: epsg.io.SRSSearch.EventType.SRS_SELECTED,
          data: e.row
        });
        this.show(false);
      }, false, this);

  //goog.events.listen(this.inputEl_, goog.events.EventType.BLUR, function(e) {
  //  this.show(false);
  //}, false, this);

  goog.events.listen(this.inputEl_, goog.events.EventType.KEYDOWN, function(e) {
    if (e.keyCode == goog.events.KeyCodes.ESC) this.show(false);
    e.stopPropagation();
  }, false, this);

  this.show(false);
};
goog.inherits(epsg.io.SRSSearch, goog.events.EventTarget);


/**
 * @define {string} URL of the service to direct the jsonp requests to.
 */
epsg.io.SRSSearch.SERVICE_URL = '//epsg.io/';


/**
 * @param {string} value
 */
epsg.io.SRSSearch.prototype.select = function(value) {
  this.jsonp_.send({'format': 'json', 'q': value}, goog.bind(function(e) {
    this.dispatchEvent({
      type: epsg.io.SRSSearch.EventType.SRS_SELECTED,
      data: e['results'][0]
    });
  }, this));
};


/**
 * Shows the dialog.
 * @param {boolean} show
 */
epsg.io.SRSSearch.prototype.show = function(show) {
  this.renderer_.dismiss();
  this.inputEl_.value = '';
  this.inputEl_.focus();
};


/**
 * @param {string} token
 * @param {number} maxMatches
 * @param {Function} matchCallback
 * @protected
 */
epsg.io.SRSSearch.prototype.requestMatchingRows =
    function(token, maxMatches, matchCallback) {
  if (token.length < 2) matchCallback([]);
  this.jsonp_.send({'format': 'json', 'q': token}, function(e) {
    matchCallback(token, e['results']);
  });
};


/**
 * @param {Object} row
 * @param {string} token
 * @param {Node} node
 * @protected
 */
epsg.io.SRSSearch.prototype.renderRow = function(row, token, node) {
  node.innerHTML = row.data['name'] + '&nbsp;(EPSG:' + row.data['code'] + ')';
  /* render:
  goog.dom.appendChild(node, goog.dom.createTextNode(
    row.data['formatted_address']));
  goog.dom.appendChild(node, goog.dom.createDom("span", "ac-type",
      goog.dom.createTextNode(row.data['type'])));
  */
};


/** @enum {string} */
epsg.io.SRSSearch.EventType = {
  SRS_SELECTED: 'selected'
};
