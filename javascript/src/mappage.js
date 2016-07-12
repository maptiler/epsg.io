/**
 * EPSG.io Coordinates JavaScript App
 * ----------------------------------
 * Copyright (C) 2013 - Moravian Library, http://www.mzk.cz/
 * Copyright (C) 2014 - Klokan Technologies GmbH, http://www.klokantech.com/
 * All rights reserved.
 */

goog.provide('epsg.io.MapPage');

goog.require('epsg.io.SRSPopup');
goog.require('goog.Timer');
goog.require('goog.Uri.QueryData');
goog.require('goog.dom');
goog.require('goog.net.Jsonp');
goog.require('kt.Nominatim');
goog.require('kt.alert');
goog.require('ol.Map');
goog.require('ol.View');
goog.require('ol.extent');
goog.require('ol.layer.Tile');
goog.require('ol.source.OSM');
goog.require('ol.source.TileJSON');


/**
 * @type {string}
 * @const
 */
epsg.io.TRANS_SERVICE_URL = '/trans';



/**
 * @constructor
 */
epsg.io.MapPage = function() {

  this.srsTitleEl_ = goog.dom.getElement('crs-title');
  this.srsSearchEl_ = goog.dom.getElement('crs-search');
  this.srsDetailLinkEl_ = goog.dom.getElement('crs-detail-link');
  this.copyClipboardContainerEl_ = /** @type {!Element} */
      (goog.dom.getElement('copy-clipboard-container'));

  goog.style.setElementShown(this.copyClipboardContainerEl_, false);
  goog.style.setElementShown(this.srsDetailLinkEl_, false);

  this.srs_ = null;

  this.srsPopup_ = new epsg.io.SRSPopup();
  this.srsPopup_.listen(epsg.io.SRSPopup.EventType.SRS_SELECTED,
      function(e) {
        if (e.data) {
          this.handleSRSChange_(e.data);
        }
      }, false, this);

  this.srsChange_ = goog.dom.getElement('crs-change');
  goog.events.listen(this.srsChange_, goog.events.EventType.CLICK,
      function(e) {
        this.srsPopup_.show();
        e.preventDefault();
      }, false, this);

  /**
   * @type {number}
   * @private
   */
  this.lon_ = 0;

  /**
   * @type {number}
   * @private
  */
  this.lat_ = 0;

  // LOAD ALL THE EXPECTED ELEMENTS ON THE PAGE
  this.mapElement = /** @type {!Element} */(goog.dom.getElement('map'));
  this.mapTypeElement_ = /** @type {!HTMLSelectElement} */
                         (goog.dom.getElement('mapType'));
  this.reprojectMapElement_ = /** @type {!HTMLInputElement} */
                              (goog.dom.getElement('reproject_map'));
  this.reprojectMapContainer_ = /** @type {!HTMLInputElement} */
      (goog.dom.getElement('reproject_map_container'));

  this.geocoderElement = /** @type {!HTMLInputElement} */
      (goog.dom.getElement('geocoder'));

  this.eastingElement = goog.dom.getElement('easting');
  this.northingElement = goog.dom.getElement('northing');
  this.eastNorthFormElement = goog.dom.getElement('eastnorth_form');
  this.eastNorthCopyElement = goog.dom.getElement('eastnorth_copy');

  this.lonLatMutex = false;

  // Force preservation of user typed values on recalculation
  this.keepHash = true;
  this.keepEastNorth = false;

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

  /**
   * @type {?google.maps.Map}
   * @private
   */
  this.gmapWrap_ = null;

  /**
   * @type {!Array}
   * @private
   */
  this.viewListenKeys_ = [];

  /**
   * @type {!Array}
   * @private
   */
  this.viewListenKeysForGmapWrap_ = [];

  this.map_ = new ol.Map({
    target: this.mapElement,
    view: null,
    layers: [],
    controls: [
      new ol.control.Attribution({
        collapsible: false,
        tipLabel: ''
      })]
  });

  /**
   * @type {boolean}
   * @private
   */
  this.reprojectionViewOn_ = false;

  goog.events.listen(this.reprojectMapElement_, goog.events.EventType.CHANGE,
      function(e) {
        if (this.gmapWrap_) {
          this.mapTypeElement_.value = 'streets';
          this.updateMapType_();
        }
        this.updateMapView_();
        this.updateHash_();
      }, false, this);
  this.updateMapView_();

  this.updateLonLat_([this.lon_, this.lat_]);

  this.parseHash_();

  goog.events.listen(this.mapTypeElement_, goog.events.EventType.CHANGE,
      function(e) {
        this.updateMapType_();
        this.updateHash_();
      }, false, this);
  this.updateMapType_();

  this.keepHash = false;

  var zoomBtn = function(map, delta, e) {
    if (!map) return;
    var view = map.getView(), curRes = view.getResolution();
    map.beforeRender(ol.animation.zoom({
      resolution: curRes,
      duration: 250,
      easing: ol.easing.easeOut
    }));
    view.setResolution(view.constrainResolution(curRes, delta));
    e.preventDefault();
  };
  var mapPlus = goog.dom.getElement('map-plus');
  var mapMinus = goog.dom.getElement('map-minus');
  if (mapPlus && mapMinus) {
    goog.events.listen(mapPlus, goog.events.EventType.CLICK,
        function(e) {zoomBtn(this.map_, 1, e);}, false, this);
    goog.events.listen(mapMinus, goog.events.EventType.CLICK,
        function(e) {zoomBtn(this.map_, -1, e);}, false, this);
  }
  var mapSearch = goog.dom.getElement('map-search');
  var searchContainer = goog.dom.getElement('search-container');
  if (mapSearch && searchContainer) {
    goog.events.listen(mapSearch, goog.events.EventType.CLICK, function(e) {
      if (goog.dom.classlist.toggle(searchContainer, 'visible') &&
          this.geocoderElement) {
        this.geocoderElement.focus();
      }
      e.preventDefault();
      e.stopPropagation();
    }, false, this);
  }
  this.map_.on(ol.MapBrowserEvent.EventType.SINGLECLICK,
      function(e) {
        var pan = ol.animation.pan({
          duration: 150,
          source: this.view_.getCenter()
        });
        this.map_.beforeRender(pan);
        this.view_.setCenter(e.coordinate);
        e.preventDefault();
      }, this);

  // The user can type easting / northing and hit Enter
  goog.events.listen(this.eastNorthFormElement, goog.events.EventType.SUBMIT,
      function(e) {
        if (!this.srs_) return;
        var easting = goog.string.toNumber(this.eastingElement.value);
        var northing = goog.string.toNumber(this.northingElement.value);
        if (!isNaN(easting) && !isNaN(northing)) {
          // Make the query to epsg.io/trans to get new lat/lon
          this.jsonp_.send({
            'x': easting,
            'y': northing,
            's_srs': this.srs_['code']
          }, goog.bind(function(result) {
            var latitude = goog.string.toNumber(result['y']);
            var longitude = goog.string.toNumber(result['x']);
            this.keepEastNorth = true;
            this.updateLonLat_([longitude, latitude]);
            this.keepEastNorth = false;
          }, this));
        }
        e.preventDefault();
      }, false, this);

  if (this.geocoderElement) {
    var nominatim = new kt.Nominatim(this.geocoderElement,
        'http://nominatim.klokantech.com/');
    nominatim.registerCallback(goog.bind(function(bnds) {
      this.geocoderElement.value = '';
      var size = this.map_.getSize();
      if (size && ol.extent.getArea(bnds) > 1e-5) {
        this.view_.fit(ol.proj.transformExtent(bnds,
            'EPSG:4326', this.view_.getProjection()), size);
      } else {
        this.view_.setCenter(ol.proj.transform(ol.extent.getCenter(bnds),
            'EPSG:4326', this.view_.getProjection()));
        this.view_.setZoom(15);
      }
    }, this));
  }


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
 * @param {Object} srsData
 * @param {boolean=} opt_dontCenter
 * @private
 */
epsg.io.MapPage.prototype.handleSRSChange_ = function(srsData, opt_dontCenter) {
  var firstSRS = !this.srs_ && !!srsData;
  this.srs_ = srsData;
  if (!this.srs_) return;

  this.keepEastNorth = false;
  this.makeQuery();

  this.srsTitleEl_.innerHTML =
      this.srs_['name'] + ' <span>' + 'EPSG:' + this.srs_['code'] + '</span>';
  this.srsDetailLinkEl_.href = '/' + this.srs_['code'];
  goog.style.setElementShown(this.copyClipboardContainerEl_, true);
  goog.style.setElementShown(this.srsDetailLinkEl_, true);

  var newProj;
  var bbox = this.srs_['bbox'];
  var code = this.srs_['code'];
  if (this.srs_['proj4'].length > 0 &&
      goog.isArray(bbox) && bbox.length == 4 &&
      code != '4326' && code != '3857') {
    var newProjCode = 'EPSG:' + code;
    proj4.defs(newProjCode, this.srs_['proj4']);
    newProj = ol.proj.get(newProjCode);
    var fromLonLat = ol.proj.getTransform('EPSG:4326', newProj);

    // very approximate calculation of projection extent
    var extent = ol.extent.applyTransform(
        [bbox[1], bbox[2], bbox[3], bbox[0]], fromLonLat);
    newProj.setExtent(extent);
  }

  if (!opt_dontCenter && firstSRS && goog.isArray(bbox) && bbox.length == 4) {
    var extent = ol.proj.transformExtent(
        [bbox[1], bbox[2],
         bbox[3], bbox[0]],
        'EPSG:4326', this.view_.getProjection());
    if (extent) {
      var size = goog.style.getContentBoxSize(this.mapElement);
      size = [size.width, size.height];
      if (size) {
        this.view_.fit(
            ol.extent.getIntersection(extent,
                this.view_.getProjection().getExtent()),
            size);
      }
    }
  }

  this.handleReprojectionConditionsChange_();

  this.updateHash_();
};


/**
 * @private
 */
epsg.io.MapPage.prototype.updateMapType_ = function() {
  if (this.gmapWrap_) {
    google.maps.event.clearInstanceListeners(this.gmapWrap_);
    goog.dom.removeChildren(this.mapElement);
    this.map_.setTarget(this.mapElement);
    delete this.gmapWrap_;
    goog.array.forEach(this.viewListenKeysForGmapWrap_,
                       ol.Observable.unByKey);
    this.viewListenKeysForGmapWrap_ = [];
  }

  this.mapElement.style.backgroundColor = '';

  var newLayers = [];

  var mapType = this.mapTypeElement_.value;
  var useGmaps = mapType.indexOf('gmaps-') === 0;
  if (useGmaps) {
    var olTarget = goog.dom.createDom('div',
                                      {'style': 'width:100%;height:100%'});
    this.map_.setTarget(olTarget);

    goog.dom.removeChildren(this.mapElement);

    var gmap = new google.maps.Map(this.mapElement, {
      disableDefaultUI: true,
      keyboardShortcuts: false,
      draggable: false,
      disableDoubleClickZoom: true,
      scrollwheel: false,
      streetViewControl: false,
      tilt: 0,
      mapTypeId: mapType.substr(6) // part after "gmaps-"
    });
    this.gmapWrap_ = gmap;
    gmap.controls[google.maps.ControlPosition.TOP_LEFT].push(olTarget);

    this.handleReprojectionConditionsChange_();

    var v = this.view_;
    this.viewListenKeysForGmapWrap_.push(v.on('change:center', function() {
      var center = ol.proj.transform(v.getCenter() || null,
                                     'EPSG:3857', 'EPSG:4326');
      gmap.setCenter(new google.maps.LatLng(center[1], center[0]));
    }));
    this.viewListenKeysForGmapWrap_.push(v.on('change:resolution', function() {
      gmap.setZoom(v.getZoom() || 0);
    }));

    var center = ol.proj.transform(v.getCenter() || null,
                                   'EPSG:3857', 'EPSG:4326');
    gmap.setCenter(new google.maps.LatLng(center[1], center[0]));
    gmap.setZoom(v.getZoom() || 0);

    google.maps.event.addListenerOnce(gmap, 'idle', goog.bind(function() {
      google.maps.event.trigger(gmap, 'resize');
      this.map_.updateSize();
    }, this));
  } else {
    var src;
    var tilejson = this.mapTypeElement_.options[
        this.mapTypeElement_.selectedIndex].getAttribute('data-tilejson');
    if (tilejson) {
      src = new ol.source.TileJSON({url: tilejson, useXhr: true});
    } else {
      if (mapType == 'osm') {
        src = new ol.source.OSM();
        (function() {src.opaque_ = false;})();
      }
    }
    //src.setRenderReprojectionEdges(true);
    newLayers = [new ol.layer.Tile({source: src})];
    this.handleReprojectionConditionsChange_();
  }

  this.map_.getLayerGroup().setLayers(new ol.Collection(newLayers));
  this.map_.updateSize();
};


/**
 * @private
 */
epsg.io.MapPage.prototype.handleReprojectionConditionsChange_ = function() {
  var possible = this.srs_ && ol.proj.get('EPSG:' + this.srs_['code']);
  goog.style.setElementShown(this.reprojectMapContainer_, possible);
  if (!possible || this.gmapWrap_) {
    this.reprojectMapElement_.checked = false;
  }
  if (this.reprojectionViewOn_) {
    this.updateMapView_();
  }
};


/**
 * @private
 */
epsg.io.MapPage.prototype.updateMapView_ = function() {
  if (this.viewListenKeys_.length) {
    goog.array.forEach(this.viewListenKeys_, goog.events.unlistenByKey);
    this.viewListenKeys_ = [];
    goog.array.forEach(this.viewListenKeysForGmapWrap_,
                       goog.events.unlistenByKey);
    this.viewListenKeysForGmapWrap_ = [];
  }

  var reprojectMap =
      this.reprojectMapElement_.checked && !!this.srs_ && !this.gmapWrap_;
  var projection = ol.proj.get(reprojectMap ?
      ('EPSG:' + this.srs_['code']) : 'EPSG:3857');
  var resolution = !this.view_ ? null : (this.view_.getResolution() *
      this.view_.getProjection().getMetersPerUnit());
  this.view_ = new ol.View({
    center: ol.proj.transform([this.lon_, this.lat_], 'EPSG:4326', projection),
    projection: projection,
    extent: projection.getExtent(),
    maxZoom: 21,
    zoom: reprojectMap ? 0 : 2
  });

  this.viewListenKeys_.push(this.view_.on('change:center', function(e) {
    var pos = ol.proj.transform(
        this.view_.getCenter(), this.view_.getProjection(), 'EPSG:4326');
    this.updateLonLat_(pos);
  }, this));

  this.viewListenKeys_.push(this.view_.on('change:resolution', function(e) {
    this.updateHash_();
  }, this));

  if (resolution) {
    this.view_.setResolution(this.view_.constrainResolution(
        resolution / this.view_.getProjection().getMetersPerUnit()));
  }
  this.view_.setCenter(this.view_.constrainCenter(this.view_.getCenter()));

  this.map_.setView(this.view_);
  this.reprojectionViewOn_ = reprojectMap;
};


/**
 * The throttled call for the coordinates transformation via JSONP
 * @protected
 */
epsg.io.MapPage.prototype.makeQuery = function() {
  this.eastingElement.value = '';
  this.northingElement.value = '';

  // If the timer has a waiting query, then trash it -
  // it is obsolete, because we have a new one
  if (this.queryTimer_) {
    goog.Timer.clear(this.queryTimer_);
    this.queryTimer_ = null;
  }
  if (!this.srs_) return;
  var code = this.srs_['code'];

  var updateTransformLink = goog.bind(function() {
    goog.dom.getElement('crs-transform-link').href =
        '/transform#s_srs=' + code +
        '&x=' + this.eastingElement.value +
        '&y=' + this.northingElement.value;
  }, this);

  var localProj = ol.proj.get('EPSG:' + code);
  var localTransform = localProj &&
                       ol.proj.getTransform('EPSG:4326', localProj);
  if (localTransform) {
    if (!this.keepEastNorth) {
      var result = localTransform([this.lon_, this.lat_]);
      this.eastingElement.value = result[0].toFixed(6);
      this.northingElement.value = result[1].toFixed(6);
      updateTransformLink();
      this.updateHash_();
    }
  } else {
    // Don't proceed with the JSONP query immediatelly,
    //   but wait for 500 ms if the user doesn't make a new one.
    this.queryTimer_ = goog.Timer.callOnce(function() {
      if (!this.srs_) return;

      var data = { 'x': this.lon_, 'y': this.lat_, 't_srs': code };
      this.jsonp_.send(data, goog.bind(function(result) {
        if (!this.keepEastNorth) {
          this.eastingElement.value = result.x;
          this.northingElement.value = result.y;
          updateTransformLink();
          this.updateHash_();
        }
        this.queryTimer_ = null;
      }, this));
    }, 500, this);
  }
};


/**
 * @param {ol.Coordinate} lonlat
 * @private
 */
epsg.io.MapPage.prototype.updateLonLat_ = function(lonlat) {
  if (this.lonLatMutex) return;
  this.lonLatMutex = true;
  this.lat_ = lonlat[1];
  this.lon_ = lonlat[0];
  if (!this.keepEastNorth) {
    this.makeQuery();
  }
  this.view_.setCenter(ol.proj.transform([this.lon_, this.lat_],
      'EPSG:4326', this.view_.getProjection()));
  this.lonLatMutex = false;

  this.updateHash_();
};


/**
 * @private
 */
epsg.io.MapPage.prototype.updateHash_ = function() {
  if (this.keepHash) return;
  var qd = new goog.Uri.QueryData();

  if (this.srs_) {
    qd.set('srs', this.srs_['code']);
    qd.set('x', this.eastingElement.value);
    qd.set('y', this.northingElement.value);
  } else {
    qd.remove('srs');
  }

  qd.set('z', this.view_.getZoom());

  if (this.reprojectionViewOn_) {
    qd.set('reproject', '1');
  }

  var layer = this.mapTypeElement_.value;
  if (layer != 'gmaps-roadmap') {
    // do not include default value to shorten the url
    qd.set('layer', this.mapTypeElement_.value);
  }

  window.location.hash = qd.toString();
};


/**
 * @private
 */
epsg.io.MapPage.prototype.parseHash_ = function() {
  var qd = new goog.Uri.QueryData(window.location.hash.substr(1));

  var srs = qd.get('srs') || '4326';
  var lon = parseFloat(qd.get('lon')), lat = parseFloat(qd.get('lat'));
  var x = parseFloat(qd.get('x')), y = parseFloat(qd.get('y'));
  var z = parseInt(qd.get('z'), 10);
  var reproject = qd.get('reproject') == '1';

  var isLonLat = goog.math.isFiniteNumber(lon) && goog.math.isFiniteNumber(lat);
  var isXY = goog.math.isFiniteNumber(x) && goog.math.isFiniteNumber(y);

  this.srsPopup_.getSRS(/** @type {string} */(srs),
      goog.bind(function(data) {
        this.handleSRSChange_(data, isLonLat || isXY);
        if (reproject) {
          this.reprojectMapElement_.checked = true;
          this.updateMapView_();
          if (goog.math.isFiniteNumber(z)) {
            this.view_.setZoom(z);
          }
          this.updateHash_();
        }
        if (isXY) {
          this.jsonp_.send({
            'x': x,
            'y': y,
            's_srs': srs
          }, goog.bind(function(result) {
            var latitude = goog.string.toNumber(result['y']);
            var longitude = goog.string.toNumber(result['x']);
            this.updateLonLat_([longitude, latitude]);
          }, this));
        }
      }, this));

  if (isLonLat) {
    this.updateLonLat_([lon, lat]);
  }
  if (!reproject && goog.math.isFiniteNumber(z)) {
    this.view_.setZoom(z);
  }

  var layer = qd.get('layer');
  if (layer) {
    this.mapTypeElement_.value = /** @type {string} */(layer);
    this.updateMapType_();
  }
};


goog.exportSymbol('MapPage', epsg.io.MapPage);
