var map = L.map('map', {
    zoomControl: false
}).setView([33.6844, 73.0479], 13);



// =========================
// SATELLITE LAYER
// =========================

L.tileLayer(
'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
{
    attribution: 'Tiles © Esri'
}).addTo(map);



// =========================
// LABEL LAYER
// =========================

L.tileLayer(
'https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}{r}.png',
{
    attribution: '© OpenStreetMap'
}).addTo(map);



// =========================
// STATE
// =========================

var markers = [];
var selectedArea = "";



// =========================
// CLICK MAP
// =========================

map.on('click', async function(e){

    let lat = e.latlng.lat;
    let lng = e.latlng.lng;



    // =========================
    // REVERSE GEOCODING
    // =========================

    let reverseUrl =
    `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`;

    let res = await fetch(reverseUrl);
    let data = await res.json();

    let areaName = data.display_name;
    selectedArea = areaName;



    // update UI
    document.getElementById("locationName")
    .innerHTML = "Location: " + areaName;



    // save for python use
    localStorage.setItem("selected_area", areaName);



    // =========================
    // MARKER
    // =========================

    let marker = L.marker([lat, lng])
    .addTo(map)
    .bindPopup(areaName);

    markers.push(marker);



    // keep only 2 markers
    if(markers.length > 2){
        markers.forEach(m => map.removeLayer(m));
        markers = [];
    }



    // =========================
    // DISTANCE CALC
    // =========================

    if(markers.length == 2){

        let p1 = markers[0].getLatLng();
        let p2 = markers[1].getLatLng();

        let distance =
        map.distance(p1, p2) / 1000;

        document.getElementById("distance")
        .innerHTML =
        "Distance: " +
        distance.toFixed(2) + " km";



        map.flyToBounds([
            [p1.lat, p1.lng],
            [p2.lat, p2.lng]
        ], {
            padding: [100, 100],
            duration: 2
        });
    }



    // =========================
    // WEATHER API
    // =========================

    let weatherUrl =
    `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lng}&current_weather=true`;

    let weatherRes = await fetch(weatherUrl);
    let weatherData = await weatherRes.json();

    let temp =
    weatherData.current_weather.temperature;

    let wind =
    weatherData.current_weather.windspeed;



    document.getElementById("weatherInfo")
    .innerHTML =
    `Weather: ${temp}°C | Wind ${wind} km/h`;
});



// =========================
// SEARCH FUNCTION
// =========================

async function searchPlace(){

    let query =
    document.getElementById("searchBox").value;

    if(!query) return;

    let url =
`https://nominatim.openstreetmap.org/search?format=json&q=${query}`;

    let res = await fetch(url);
    let data = await res.json();

    if(data.length > 0){

        let lat = parseFloat(data[0].lat);
        let lon = parseFloat(data[0].lon);



        map.flyTo([lat, lon], 15, {
            duration: 2
        });



        L.marker([lat, lon])
        .addTo(map)
        .bindPopup(query)
        .openPopup();

    }
}



// =========================
// ENTER KEY SUPPORT
// =========================

document.getElementById("searchBox")
.addEventListener("keypress", function(e){

    if(e.key === "Enter"){
        searchPlace();
    }
});

function getLocation() {

    if (!navigator.geolocation) {
        alert("Geolocation not supported");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        async function(position) {

            let lat = position.coords.latitude;
            let lon = position.coords.longitude;

            // move map
            map.flyTo([lat, lon], 15, {
                duration: 2
            });

            // marker
            let marker = L.marker([lat, lon])
            .addTo(map)
            .bindPopup("📍 You are here")
            .openPopup();

            // reverse geocoding (get area name)
            let url =
`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`;

            let res = await fetch(url);
            let data = await res.json();

            let area = data.display_name;

            document.getElementById("locationName")
            .innerHTML = "Location: " + area;

            // save for Python
            localStorage.setItem("current_location", area);

        },

        function(error) {
            alert("Location access denied or failed");
        }
    );
}