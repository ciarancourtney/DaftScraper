/**
 * Created by danmalone on 02/04/2014.
 */

    var map;
    var geocoder;
    var markersArray = [];

    function clearOverlays() {
        for (var i = 0; i < markersArray.length; i++) {
            markersArray[i].setMap(null);
        }
        markersArray.length = 0;
    }

    function get(param1, param2, param3) {
        $.get(
                "http://127.0.0.1:8080/api/rentals",
                {lat: param1, long: param2, county: param3},
                function (data) {
                    alert('page content: ' + data);
                }
        );
    }

    function initialize() {
        var mapOptions = {
            center: new google.maps.LatLng(53.344103999999990000, -6.267493699999932000),
            zoom: 12
        };
        map = new google.maps.Map(document.getElementById("map-canvas"),
                mapOptions);
        geocoder = new google.maps.Geocoder();

        var latLng;

        var county;
        google.maps.event.addListener(map, 'click', function (event) {
            latLng = event.latLng;
            geocoder.geocode({'latLng': event.latLng}, function (results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    var location = results[0].formatted_address;
                    alertify.log(results[0].address_components[4].long_name, 10000);
                    county = results[0].address_components[4].long_name;

                    alertify.confirm('Estimate prices for: ' + location + "?", function (e) {
                        if (e) {
                            // user clicked "ok"
                            map.setCenter(latLng);
                            var marker = new google.maps.Marker({
                                position: map.getCenter(),
                                map: map
//                            title: 'Click to zoom'

                            });
                            clearOverlays()
                            markersArray.push(marker);

                            get(latLng.lat(), latLng.lng(), county);
                        } else {
                            // user clicked "cancel"
                        }
                    });
                }
                else {
                    alertify.error("failed to find location, try zooming in", 10000);
                }
            });


        });
    }
    google.maps.event.addDomListener(window, 'load', initialize);


