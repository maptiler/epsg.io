goog.provide('epsg.io');

goog.require('goog.array');
goog.require('goog.events');
goog.require('goog.events.EventType');
goog.require('goog.dom.classlist');
goog.require('goog.net.Jsonp');
goog.require('goog.style');


var socials_icons_init = function() {
  function popup(pageURL, w, h) {
    var left = (screen.width / 2) - (w / 2);
    var top = (screen.height / 2) - (h / 2);
    var targetWin = window.open(pageURL, '_blank', 'toolbar=no,' +
        'location=no, directories=no, status=no, menubar=no, scrollbars=no,' +
        'resizable=no, copyhistory=no, width=' + w + ', height=' + h +
        ', top=' + top + ', left=' + left);
  }
  // OnClick facebook
  var shf = goog.dom.getElement('share_facebook');
  if (shf) {
    goog.events.listen(shf, goog.events.EventType.CLICK, function(e) {
      e.preventDefault();
      popup(this.href, 645, 353);
    });
  }
  // OnClick twitter
  var sht = goog.dom.getElement('share_twitterb');
  if (sht) {
    goog.events.listen(sht, goog.events.EventType.CLICK, function(e) {
      e.preventDefault();
      popup(this.href, 450, 257);
    });
  }
  // OnClick pinterest
  var shp = goog.dom.getElement('share_pinterest');
  if (shp) {
    goog.events.listen(shp, goog.events.EventType.CLICK, function(e) {
      e.preventDefault();
      popup(this.href, 620, 280);
    });
  }
  // OnClick G+
  var shg = goog.dom.getElement('share_gplusdark');
  if (shg) {
    goog.events.listen(shg, goog.events.EventType.CLICK, function(e) {
      e.preventDefault();
      popup(this.href, 610, 315);
    });
  }
};


/**
 * The Home page javascript
 */
epsg.io.home_init = function() {

  // Cursor into search box
  var qi = goog.dom.getElement('q');
  if (qi) qi.focus();

  // Client side GeoIP country detection with
  // http://freegeoip.net/json/?callback=asfasd
  if (goog.dom.getElement('countryLinkWrapper')) {
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
  }
  var soc = goog.dom.getElementByClass('socialicons');
  if (soc) {
    socials_icons_init();
  }

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

  // Show / hide deprecated transformations
  var tdl = goog.dom.getElement('trans_deprecated_link');
  if (tdl) {
    goog.events.listen(tdl, goog.events.EventType.CLICK, function(e) {
      e.preventDefault();
      var d = goog.dom.getElement('trans_deprecated');
      if (d.style.display == 'block') {
        d.style.display = 'none';
        tdl.innerHTML = 'Show deprecated transformations';
      } else {
        d.style.display = 'block';
        tdl.innerHTML = 'Hide deprecated transfortmations';
      }
    });
  }


  var switcherClicked = function(e) {
    e.preventDefault();
    var future_switcher = e.target; // Clicked element
    var future_code = goog.dom.getElement(future_switcher.id + '_code');
    var old_switcher = goog.dom.getElementByClass('switcher_selected');
    var old_code = goog.dom.getElementByClass('code_visible');
    goog.dom.classlist.remove(old_switcher, 'switcher_selected');
    goog.dom.classlist.remove(old_code, 'code_visible');
    goog.dom.classlist.add(future_switcher, 'switcher_selected');
    goog.dom.classlist.add(future_code, 'code_visible');
  };
  goog.array.forEach(goog.dom.getElementsByClass('switcher'), function(e) {
    goog.events.listen(e, goog.events.EventType.CLICK, switcherClicked);
  });

  var ZeroClipboard = window['ZeroClipboard'];
  ZeroClipboard['config']({ 'moviePath': '/js/ZeroClipboard.swf' });

  // Put zeroclipboard on all elements with "zeroclipboard" class
  goog.array.forEach(goog.dom.getElementsByClass('zeroclipboard'),
      function(element) { new ZeroClipboard(element); });

  var soc = goog.dom.getElementByClass('socialicons');
  if (soc) {
    socials_icons_init();
  }

};



goog.exportSymbol('home_init', epsg.io.home_init);
goog.exportSymbol('results_init', epsg.io.results_init);
goog.exportSymbol('detail_init', epsg.io.detail_init);
