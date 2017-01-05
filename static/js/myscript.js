$( "#my-button" ).click(function() {
  console.log($('#my-button').prop('value'));
  document.getElementById('my-button').innerHTML = 'Insert into butt'
>>>>>>> origin/master
});

var clock;

$(document).ready(function() {
  var clock;

  clock = $('.clock').FlipClock({
        clockFace: 'TwelveHourClock',
        }
    });

    // clock.setTime(220880);
    // clock.setCountdown(true);
    // clock.start();
});
