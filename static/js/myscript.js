function change()
{
    if (this.value=="button") this.value = "new button";
    else this.value = "button";
}

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
