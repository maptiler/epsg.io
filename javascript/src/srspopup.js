/**
 *
 * @author petr.sloup@klokantech.com (Petr Sloup)
 *
 * Copyright 2015 Klokan Technologies Gmbh (www.klokantech.com)
 */

goog.provide('epsg.io.SRSPopup');
goog.provide('epsg.io.SRSPopup.EventType');

goog.require('goog.dom');
goog.require('goog.dom.classlist');
goog.require('goog.events.EventTarget');
goog.require('goog.events.KeyCodes');
goog.require('goog.net.Jsonp');
goog.require('kt.Popup');



/**
 * @constructor
 * @extends {goog.events.EventTarget}
 */
epsg.io.SRSPopup = function() {
  goog.base(this);

  /**
   * @type {!kt.Popup}
   * @private
   */
  this.popup_ = new kt.Popup('Coordinate system', true, true);

  /**
   * @type {!Element}
   * @private
   */
  this.inputEl_ = goog.dom.createDom(goog.dom.TagName.INPUT, 'srsdialog-input');

  var searchBtn = goog.dom.createDom(goog.dom.TagName.INPUT, {
    'type': 'submit',
    'class': 'srsdialog-table',
    'value': 'Search'
  });

  /**
   * @type {!Element}
   * @private
   */
  this.tableEl_ = goog.dom.createDom(goog.dom.TagName.TABLE, 'srsdialog-table');

  var tableHead = goog.dom.createDom(goog.dom.TagName.TR, undefined,
      goog.dom.createDom(goog.dom.TagName.TH, undefined, 'Code'),
      goog.dom.createDom(goog.dom.TagName.TH, undefined, 'Name'),
      goog.dom.createDom(goog.dom.TagName.TH, undefined, 'Area'),
      goog.dom.createDom(goog.dom.TagName.TH, undefined, 'Accuracy'));
  goog.dom.appendChild(this.tableEl_, tableHead);

  /**
   * @type {!Element}
   * @private
   */
  this.formEl_ = goog.dom.createDom(goog.dom.TagName.FORM, 'srsdialog-form');

  goog.events.listen(this.formEl_, goog.events.EventType.SUBMIT, function(e) {
    this.search_();
    e.preventDefault();
  }, false, this);

  goog.dom.append(this.formEl_, this.inputEl_, searchBtn, this.tableEl_);

  this.popup_.append(this.formEl_);

  var selectBtn = goog.dom.createDom(goog.dom.TagName.DIV,
                                     'btn-light', 'Select');
  var cancelBtn = goog.dom.createDom(goog.dom.TagName.DIV,
                                     'btn-dark', 'Cancel');
  this.popup_.appendActions(cancelBtn, selectBtn);

  /**
   * @type {?Object}
   * @private
   */
  this.selectedRowData_ = null;

  /**
   * @type {!Array.<!Element>}
   * @private
   */
  this.tableRows_ = [];

  goog.events.listen(selectBtn, goog.events.EventType.CLICK, function(e) {
    this.handleSelect_();
    e.preventDefault();
  }, false, this);

  goog.events.listen(cancelBtn, goog.events.EventType.CLICK, function(e) {
    this.popup_.setVisible(false);
    e.preventDefault();
  }, false, this);

  /**
   * @type {!goog.net.Jsonp}
   * @private
   */
  this.jsonp_ = new goog.net.Jsonp(epsg.io.SRSPopup.SERVICE_URL);

  goog.events.listen(this.inputEl_, goog.events.EventType.KEYDOWN, function(e) {
    if (e.keyCode == goog.events.KeyCodes.ESC) this.popup_.setVisible(false);
    e.stopPropagation();
  }, false, this);
};
goog.inherits(epsg.io.SRSPopup, goog.events.EventTarget);


/**
 * @define {string} URL of the service to direct the jsonp requests to.
 */
epsg.io.SRSPopup.SERVICE_URL = '/';


/**
 * Shows the dialog.
 */
epsg.io.SRSPopup.prototype.show = function() {
  this.popup_.setVisible(true);
  this.inputEl_.value = '';
  this.inputEl_.focus();
  this.clearTable_();
};


/**
 * Gets the SRS (loads it's data) without showing the dialog.
 * @param {string} code Code possibly with transform id separated by minus sign.
 * @param {function(Object)} callback
 */
epsg.io.SRSPopup.prototype.getSRS = function(code, callback) {
  var parts = code.split('-');
  if (parts.length < 1) return;
  var system = parts[0];
  var trans = (parts.length > 1) ? parseInt(parts[1], 10) : null;

  var params = {
    'format': 'json',
    'q': system
  };
  if (!goog.isNull(trans)) {
    params['trans'] = '1';
  }
  this.jsonp_.send(params, function(e) {
    var result = e['results'][0];
    if (!goog.isNull(trans)) {
      goog.array.forEach(result['trans'], function(el) {
        if (el['code_trans'] == trans) {
          el['code'] = result['code'] + '-' + trans;
          el['name'] = result['name'];
          result = el;
        }
      });
    }
    callback(result);
  });
};


/**
 * @private
 */
epsg.io.SRSPopup.prototype.clearTable_ = function() {
  goog.array.forEach(this.tableRows_, goog.dom.removeNode);
  goog.array.forEach(this.tableRows_,
      /** @type {function(Element)} */(goog.events.removeAll));
  this.tableRows_ = [];
  this.selectedRowData_ = null;
};


/**
 * @private
 */
epsg.io.SRSPopup.prototype.search_ = function() {
  this.clearTable_();

  var token = this.inputEl_.value;

  this.jsonp_.send({
    'format': 'json',
    'trans': '1',
    'q': token},
  goog.bind(function(e) {
    var addRow = goog.bind(function(className, data, code, name) {
      var area = data['area'];
      var accuracy = data['accuracy'].toString() + ' m';
      var row = goog.dom.createDom(goog.dom.TagName.TR, className,
          goog.dom.createDom(goog.dom.TagName.TD, undefined, code),
          goog.dom.createDom(goog.dom.TagName.TD, undefined, name),
          goog.dom.createDom(goog.dom.TagName.TD, undefined, area),
          goog.dom.createDom(goog.dom.TagName.TD, undefined, accuracy));
      this.tableRows_.push(row);

      goog.dom.appendChild(this.tableEl_, row);

      goog.events.listen(row, goog.events.EventType.CLICK, function(e) {
        this.selectRow_(row, data);
        e.preventDefault();
      }, false, this);

      return row;
    }, this);

    this.clearTable_();

    var code, name, area, accuracy;
    var results = e['results'];
    goog.array.forEach(results, function(result) {
      var transes = result['trans'];
      var defaultTrans = result['default_trans'];

      var transShower = goog.dom.createDom(goog.dom.TagName.SPAN,
          'srsdialog-transshower', '>');

      code = goog.dom.createDom(goog.dom.TagName.SPAN, undefined,
          transShower, result['code']);
      name = result['name'];

      var systemRow = addRow(
          'system' + (transes.length > 0 ? ' expandable' : ''),
          result, code, name);

      var transRows = [];

      goog.array.forEach(transes, function(trans) {
        var code_trans = trans['code_trans'];
        trans['code'] = result['code'] + '-' + code_trans;
        trans['name'] = result['name'];
        code = '  ' + code_trans;

        if (defaultTrans == code_trans) {
          result['bbox'] = trans['bbox'];
        }

        var transRow = addRow(
            'trans hidden' + (defaultTrans == code_trans ? ' default' : ''),
            trans, code, '');
        transRows.push(transRow);
      }, this);

      goog.events.listen(transShower, goog.events.EventType.CLICK, function(e) {
        goog.array.forEach(transRows, function(el) {
          goog.dom.classlist.toggle(el, 'hidden');
        }, this);
        e.preventDefault();
      }, false, this);

    }, this);
  }, this));
};


/**
 * @param {Element} row
 * @param {Object} data
 * @private
 */
epsg.io.SRSPopup.prototype.selectRow_ = function(row, data) {
  goog.array.forEach(this.tableRows_, function(el) {
    goog.dom.classlist.enable(el, 'selected', el == row);
  }, this);
  this.selectedRowData_ = data;
};


/**
 * @private
 */
epsg.io.SRSPopup.prototype.handleSelect_ = function() {
  this.dispatchEvent({
    type: epsg.io.SRSPopup.EventType.SRS_SELECTED,
    data: this.selectedRowData_
  });
  this.popup_.setVisible(false);
};


/** @enum {string} */
epsg.io.SRSPopup.EventType = {
  SRS_SELECTED: 'selected'
};
