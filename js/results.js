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
        center: {lat: 0, lng: 0}
      });
      document.getElementById('results-map').className = 'active';
      document.getElementById('noresults').className = 'hidden';
      var position = results[0].geometry.location;
      var hash = '#x=' + position.lng() + '&y=' + position.lat() + '&z=8';
      document.getElementById('map-link').href += hash;
      map.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        map: map,
        position: results[0].geometry.location
      });
    }
  });
}