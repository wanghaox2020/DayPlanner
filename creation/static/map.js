const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
var map = L.map('map').setView([40.7342, -74.0033], 13);

var combine = L.layer

const value = JSON.parse(document.getElementById('coordinates').textContent);
console.log(value);
for(var i=0;i<value.length;i++){
    L.marker([value[i]["latitude"],value[i]["longitude"]]).bindPopup(value[i]["name"]).addTo(map)
}

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
