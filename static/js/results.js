/* Results geocoder */
function results(address) {
  var geocoder = new google.maps.Geocoder();
  geocodeAddress(geocoder, address);
}
function geocodeAddress(geocoder, address) {
  geocoder.geocode({'address': address}, function (results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      var map = new google.maps.Map(document.getElementById('results-map'), {
        zoom: 8,
        center: {lat: 0, lng: 0},
        draggable: false,
        zoomControl: false,
        scrollwheel: false,
        disableDoubleClickZoom: true,
        disableDefaultUI: true
      });
      document.getElementById('results-map-container').className = 'active';
      var geometry = results[0].geometry.location;
      var position = [
        Math.round(geometry.lng() * 100000000) / 100000000,
        Math.round(geometry.lat() * 100000000) / 100000000
      ];
      var resPosition = document.getElementById('results-map-position');
      resPosition.innerHTML = position[0] + ' ' + position[1];
      var hash = '#x=' + position[0] + '&y=' + position[1] + '&z=18';
      document.getElementById('results-map-btn').href += hash;
      map.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        map: map,
        position: results[0].geometry.location
      });
    }
  });
}
