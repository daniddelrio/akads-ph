// DATEPICKER
$('#birthday').data('datepicker');
$(document).ready(function(){
  if (document.getElementById('birthday')) {
    document.getElementById('birthday').addEventListener('click', function() {
      let choice = $(this).val();
      console.log(choice);
      if (document.getElementById('hidden-birthday')) {
        document.getElementById('hidden-birthday').value = choice;
      }
    });
  }
});

$('#book-date').data('datepicker');
$(document).ready(function(){
  if (document.getElementById('book-date')) {
    document.getElementById('book-date').addEventListener('click', function() {
      let choice = $(this).val();
      console.log(choice);
      document.getElementById('hidden-date').value = choice;
    });
  }
});

// $(document).ready(function(){
//   document.getElementById('start').addEventListener('click', function() {
//     let choice = 'hidden' + $('#hidden-date').val();
//     console.log(choice);
//   });
// });


// TIMEPICKER
$(document).ready(function(){
  $('.timepicker').timepicker();
});
if (document.getElementById('start')) {
  document.getElementById('hours').addEventListener('change', function() {
    let choice = $('#start').val();
    console.log(choice.split(':'));
    console.log(typeof choice);
    arr = choice.split(':');
    let y = parseInt(arr[0]);
    z = parseInt($('#hours').val());
    console.log(z);
    x = y + z;
    if (y===12) {
      x = x -12;
    } else if (x>=12) {
      if (x===12) {
        x;
      } else {
        x = x -12;
      }
      let arr1 = arr[1].split(" ");
      if (arr1[1]==="AM") {
        arr1[1] = "PM";
      } else {
        arr1[1] = "AM";
      }
      arr[1] = arr1.join(" ");
    }
    if (x<10) {
      arr[0] = "0" + x.toString();
    } else {
      arr[0] = x.toString();
    }
    choice = arr.join(':');
    console.log(choice);
    if (document.getElementById('hidden-time')) {
      document.getElementById('hidden-time').value = choice;
    }
  });
  document.getElementById('start').addEventListener('change', function() {
    let choice = $('#start').val();
    console.log(choice.split(':'));
    console.log(typeof choice);
    arr = choice.split(':');
    let y = parseInt(arr[0]);
    z = parseInt($('#hours').val());
    console.log(z);
    x = y + z;
    if (y===12) {
      x = x -12;
    } else if (x>=12) {
      if (x===12) {
        x;
      } else {
        x = x -12;
      }
      let arr1 = arr[1].split(" ");
      if (arr1[1]==="AM") {
        arr1[1] = "PM";
      } else {
        arr1[1] = "AM";
      }
      arr[1] = arr1.join(" ");
    }
    if (x<10) {
      arr[0] = "0" + x.toString();
    } else {
      arr[0] = x.toString();
    }
    choice = arr.join(':');
    console.log(choice);
    if (document.getElementById('hidden-time')) {
      document.getElementById('hidden-time').value = choice;
    }
  });
}

// SELECT
$(document).ready(function(){
  $('select').formSelect();
});

// Get multiple select values as array
if (document.getElementById('location-select')) {
  document.getElementById('location-select').addEventListener('change', function() {
    let choice = $(this).val();
    console.log(choice.join());
    if (document.getElementById('hidden-loc')) {
      document.getElementById('hidden-loc').value = choice.join();
    }
  });
}

if (document.getElementById('location-select0')) {
  document.getElementById('location-select0').addEventListener('change', function() {
    let choice = $(this).val();
    console.log(choice.join());
    if (document.getElementById('hidden-loc0')) {
      document.getElementById('hidden-loc0').value = choice.join();
    }
  });
}

if (document.getElementById('subject-select')) {
  document.getElementById('subject-select').addEventListener('change', function() {
    let choice = $(this).val();
    console.log(choice.join());
    if (document.getElementById('hidden-subj')) {
      document.getElementById('hidden-subj').value = choice.join();
    }
  });
}

// MODAL
$(document).ready(function(){
  $('#modal1').modal();
  $('#modal1').modal('open');
});

$(document).ready(function(){
  $('#modal2').modal();
});

// DROPDOWN
document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.dropdown-trigger');
  var instances = M.Dropdown.init(elems);
});

// MAP
let map;
function initMap() {
  let page_check = document.getElementById('map-check');
    if (page_check) {
    let checker = page_check.getAttribute('stat');
    if (checker === 'tutor'){
      for (var i=1;i<20;i++){ // iterates over all the maps in the page, max of 20
        var m = 'map'+i; // get id of map in html
        console.log(m);
        map = new google.maps.Map(document.getElementById(m), {
          center: {
            lat: 14.58012,
            lng: 121.02225
          },
          zoom: 12,
          disableDefaultUI: true
        });
        var geocoder = new google.maps.Geocoder();
        geocodeAddress(geocoder, map, m);
      }
    } else if (checker === 'tutee') {
        map2 = new google.maps.Map(document.getElementById('map'), {
          center: {
            lat: 14.58012,
            lng: 121.02225
          },
          zoom: 12,
          disableDefaultUI: true
        });
        var geocoder2 = new google.maps.Geocoder();

        document.getElementById('location-select-book').addEventListener('change', function() {
          let choice = $(this).val();
          console.log(choice);
          document.getElementById('female').value = choice;
          geocodeAddress2(geocoder2, map2, choice);
        });
    }
  }
}

// GEOCODE
function geocodeAddress(geocoder, resultsMap, m) {
  var address = document.getElementById(m).getAttribute('location');
  console.log(address);
  geocoder.geocode({'address': address}, function(results, status) {
    if (status === 'OK') {
      resultsMap.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

// GEOCODE 2
function geocodeAddress2(geocoder2, resultsMap, choice) {
  var address = choice;
  geocoder2.geocode({'address': address}, function(results, status) {
    if (status === 'OK') {
      resultsMap.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

// CALENDAR
$(document).ready(function(){
  if (document.getElementById('hidden-event')) {
    let events_list = [];
    let eventsInfo_list = []
    let upcoming = $('#hidden-event').val().split('&');
    upcoming.pop();
    console.log(upcoming);
    for (let i = 0; i < upcoming.length; i++) {
      // console.log(upcoming[i]);
      let details = upcoming[i].split('|');
      let formatted_date = moment(details[0],"MMMM DD, YYYY").format('YYYY-MM-DD')
      // console.log(formatted_date);
      details.shift();
      let formatted_eventInfo = details.join(' - ');
      console.log(formatted_eventInfo);
      // console.log(formatted_eventInfo);

      events_list.push(formatted_date);
      console.log(events_list);
      eventsInfo_list.push(formatted_eventInfo.toString());
      console.log(eventsInfo_list);
    }

    $("#calendar").simpleCalendar({
      events: events_list, //List of event
      eventsInfo: eventsInfo_list
    });
  }
});

// if (document.getElementById('hidden-event')) {
//   let choice = $('#hidden-event').val();
//   console.log(choice);
// }
