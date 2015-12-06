/**
 * Created by Igor on 06.12.2015.
 */

var getCookie = function (name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

var csrfSafeMethod = function (method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

var sameOrigin = function (url) {
  var host = document.location.host;
  var protocol = document.location.protocol;
  var sr_origin = "//" + host;
  var origin = protocol + sr_origin;
  // Allow absolute or scheme relative URLs to same origin
  return (url == origin || url.slice(0, origin.length + 1) == origin + "/") ||
    (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + "/") ||
    // or any other URL that isn't scheme relative or absolute i.e relative.
    !(/^(\/\/|http:|https:).*/.test(url));
};

(function() {
  ymaps.ready(init);
  var myMap;

  csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  function init() {
    myMap = new ymaps.Map("map", {
      center: [55.8, 37.64],
      zoom: 7
    });

    myMap.events.add('boundschange', function (event) {
      var coord = event.get('newBounds');
      console.log(coord);
      $.ajax({
        type: 'POST',
        url: '/api/events/get_near_location',
        data: {
          lat_sw: coord[0][0],
          lng_sw: coord[0][1],
          lat_ne: coord[1][0],
          lng_ne: coord[1][1],
        },
        success: parseEvents,
        datatype: 'json'
      });
    });

    $.ajax({
      type: 'POST',
      url: '/api/events/get_near_location',
      data: {
        lat_sw: 53.90215977088745,
        lng_sw: 32.41050781249998,
        lat_ne: 57.61565200939664,
        lng_ne: 42.73765624999998,
      },
      success: parseEvents,
      datatype: 'json'
    });
  }

  function parseEvents(data) {
    console.log(data);
    myMap.geoObjects.removeAll();
    data['events'].forEach(function (item) {
      myMap.geoObjects
        .add(new ymaps.Placemark([item['lat'], item['lng']], {
          balloonContent: item['title']
        }, {
          preset: 'islands#icon',
          iconColor: '#0095b6'
        }));
    });
  }
})();
