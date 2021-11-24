document.addEventListener("DOMContentLoaded", function () {
    const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    var map
    const value = JSON.parse(document.getElementById('coordinates').textContent);
    if (value.length >= 1) {
        map = L.map('map').setView([value[0]["latitude"], value[0]["longitude"]], 12);
    } else {
        map = L.map('map').setView([40.7342, -74.0033], 12);
    }
    for (var i = 0; i < value.length; i++) {
        L.marker([value[i]["latitude"], value[i]["longitude"]]).bindPopup(value[i]["name"]).addTo(map)
    }
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution
    }).addTo(map);
});


