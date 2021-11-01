const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
var map = L.map('map').setView([40.7342, -74.0033], 13);
// var sushi = L.marker([40.68764, -73.9901]).bindPopup('Ki Sushi'),
//     coffee = L.marker([40.70247143757704, -73.9942601520649]).bindPopup('% Arabica'),
//     art = L.marker([40.70381, -73.98985]).bindPopup('Smack Mellon'),
//     dinner = L.marker([40.6882, -73.97953]).bindPopup('Las Santas');
// var combine = L.layerGroup([sushi, coffee, art, dinner]);

// var dayplan = combine.addTo(map);
var combine = L.layer

const value = JSON.parse(document.getElementById('coordinates').textContent);
console.log(value);
for(var i=0;i<value.length;i++){
    L.marker([value[i]["latitude"],value[i]["longitude"]]).bindPopup(value[i]["name"]).addTo(map)
}

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
