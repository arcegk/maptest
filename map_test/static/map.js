function addAddress(latLng, map, geocoder){
    var lat = latLng.lat();
    var lon = latLng.lng();

    geocoder.geocode({'location': latLng}, function(result, status){
        if(status == 'OK'){
            if(result[0]){
                var address = result[0].formatted_address;

                addMarker(latLng, map);
                $("#addresses").prepend("<span>" + lat + ", " + lon + " " + address +"</span><br>");
                
                $.ajax({
                    url: '/add-address',
                    method: 'post',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({lat: lat, lon: lon , address: address}),
                });
            }
        }
    });
}

function addMarker(latLng, map){
    var infowindow = new google.maps.InfoWindow({
        content: "<strong>location:</strong>"+ latLng.lat()+ "," + latLng.lng()
    });

    var marker = new google.maps.Marker({
        position: latLng,
        map: map
    });
    
    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });
}

function myMap() {
    var mapProp= {
        center: new google.maps.LatLng(2.3318086, -74.4667872),
        zoom: 4,
    };
    
    var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
    var geocoder = new google.maps.Geocoder
    var infowindow = new google.maps.InfoWindow;

    var tbId = document.getElementById('table_id');

    var layer = new google.maps.FusionTablesLayer({
    query: {
      select: 'location',
      from: tbId.value
    },
    styles: [{
        markerOptions: {
            iconName: "large_red"
        }
    }]
    });
  layer.setMap(map);


    google.maps.event.addListener(map, 'click', function(e){
        addAddress(e.latLng, map, geocoder);
    });
}

