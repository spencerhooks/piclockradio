$( "#my-button" ).click(function() {
  console.log($('#my-button').prop('value'));
  document.getElementById('my-button').innerHTML = 'Insert into butt'
});

$(document).ready(function() {
  var clock;

  clock = $('.clock').FlipClock({
        clockFace: 'TwelveHourClock',
        showSeconds: false,
    });


    // clock.setCountdown(true);
    // clock.start();

});
