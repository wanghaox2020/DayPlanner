document.addEventListener("DOMContentLoaded", function () {
    const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

    var combine = L.layer
    var map
    const value = JSON.parse(document.getElementById('coordinates').textContent);
    console.log(value);
    if (value.length >= 1) {
        map = L.map('map').setView([value[0]["latitude"], value[0]["longitude"]], 13);
    } else {
        map = L.map('map').setView([40.7342, -74.0033], 13);
    }
    for (var i = 0; i < value.length; i++) {
        L.marker([value[i]["latitude"], value[i]["longitude"]]).bindPopup(value[i]["name"]).addTo(map)
    }
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution
    }).addTo(map);
});


