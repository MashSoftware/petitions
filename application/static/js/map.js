var map = L.map('map').setView([54.525564, -3.921976], 5);

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="http://osm.org/copyright" target="_blank">OpenStreetMap</a> contributors. Powered by <a href="http://mapit.mysociety.org/" target="_blank">MapIt</a>'
}).addTo(map);

var myStyle = {
  color: "#2196f3",
  opacity: 1
};

function onEachFeature(feature, layer) {
  layer.bindPopup("<b>" + feature.properties.name + "</b>" +
  "<p><i class=\"fa fa-user fa-fw\"></i> " + feature.properties.mp + "</p>" +
  //"<p><i class=\"fa fa-certificate fa-fw\"></i> " + feature.properties.party + " Party</p>" +
  "<p><i class=\"fa fa-pencil fa-fw\"></i> " + feature.properties.signature_count + " signatures</p>");
}

var geojson = L.geoJson(extents, {style: myStyle, onEachFeature: onEachFeature}).addTo(map);

//Center map view on geojson
map.fitBounds(geojson.getBounds());
