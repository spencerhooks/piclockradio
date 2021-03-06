
// Setup a listener for input events to switches and sliders and send to server
document.addEventListener("change", changeListener);
function changeListener(o) {
  console.log("Target ID of changed: " + o.target.id)
  console.log(o.target.value)
  console.log(o.target.checked)

  // Handle alarm on/off switch
  if (o.target.id === "alarmSwitch") {
    myRequest(updateClock, "/alarm_on_off/" + o.target.checked)
  }

  // Handle sleep light switch (turns on light for 30 minutes and then fades off)
  if (o.target.id === "sleepLightSwitch") {
    myRequest(updateClock, "/sleep_light_on_off/" + o.target.checked)
  }

}

// // Setup listener for input events on the sleep light switch
// var sleepLightSwitchElement = document.querySelector("#sleepLightSwitch")
// sleepLightSwitchElement.addEventListener("change", sleepLight)
// function sleepLight(e) {
//   myRequest(updateClock, "/sleep_light_on_off/" + e.target.checked)
// }

// Setup listener for input events on the volume slider
var volumeSliderElement = document.querySelector("#volumeSlider")    // These can be simplified
volumeSliderElement.addEventListener("input", changeVolume)
function changeVolume(e) {
  console.log("volume slider moved")
  myRequest(updateClock, "/change_volume/" + e.target.value)
}

// Setup a listener for click events on the noise generator button
var noiseButtonElement = document.querySelector("#noiseButton")
noiseButtonElement.addEventListener("click", makeNoise)
function makeNoise(e) {
  myRequest(updateClock, "/generate_noise")
}

// Setup a listener for click events on the main clock face, used as a snooze button
var ClockElement = document.querySelector("#clockCard")
ClockElement.addEventListener("click", snooze)
function snooze(e) {
  myRequest(updateClock, "/snooze")
}

// Setup a listener for the mute button
var MuteButtonElement = document.querySelector("#muteButton")
MuteButtonElement.addEventListener("click", mute)
function mute(e) {
  myRequest(updateClock, "/mute")
}

// Loop for the clock to get the time every second
function start() {
  myRequest(updateClock, "/get_time")
  var t = setTimeout(start, 1000)
}

// Function to send requests to the server
function myRequest(callBackFunction, requestedURL) {
  var myrequest = new XMLHttpRequest()
  myrequest.onreadystatechange = callBackFunction
  myrequest.open("GET", requestedURL)
  myrequest.send()
}

// Function to convert 24 hour time format to a 12 hour time with no leading zero and am/pm added.
function formatTime(t){
  var h = parseInt(t.slice(0,2), 10)
  var m = parseInt(t.slice(3,5), 10)
	var suffix = h >= 12 ? "pm" : "am"

  m = m < 10 ? "0"+m : m  // Add leading zero if less than 10 minutes
	h = ((h + 11) % 12) + 1  // Convert from 24 hour to 12 hour

	return h+":"+m+suffix;
}

// Update all of UI elements with the data returned from the server. All variables are updated on every callback
function updateClock () {
  if (this.readyState == 4 && this.status == 200) {

    // Update clock time
    if ((JSON.parse(this.responseText)).indicate_snooze == false) {
      document.getElementById('clockText').innerHTML = formatTime((JSON.parse(this.responseText)).time)
    } else if ((JSON.parse(this.responseText)).indicate_snooze == true) {
      console.log("indicate snooze")
      document.getElementById('clockText').innerHTML = (JSON.parse(this.responseText)).time
    }

    // Update the alarm set time indicator
    document.getElementById('alarmInput').value = formatTime((JSON.parse(this.responseText)).alarm_time)

    // Update the noise generator button state
    if ((JSON.parse(this.responseText)).generating_noise == true) {
      document.getElementById('noiseImage').src = $SCRIPT_ROOT + "/static/images/waveform_color.png"
    } else if ((JSON.parse(this.responseText)).generating_noise == false) {
      document.getElementById('noiseImage').src = $SCRIPT_ROOT + "/static/images/waveform.png"
    }

    // Update the volume slider. **There's a bug when dragging the slider, need to fix this**
    if ((JSON.parse(this.responseText)).mute == true) {
      // document.getElementById('volumeSlider').MaterialSlider.change(0)
      document.getElementById('volumeSlider').MaterialSlider.disable()
      document.getElementById('muteIcon').style.color = "white"
    } else if ((JSON.parse(this.responseText)).mute == false) {
      document.getElementById('volumeSlider').MaterialSlider.enable()
      document.getElementById('volumeSlider').MaterialSlider.change((JSON.parse(this.responseText)).volume)
      document.getElementById('muteIcon').style.color = "#3F51B5"
    }

    // Update the alarm on/off switch
    if ((JSON.parse(this.responseText)).alarm_on_off == true) {
      document.getElementById('alarmSwitchSpan').style.color = "#3F51B5"
      document.getElementById('clockText').style.color = "#3F51B5"
      document.getElementById('alarmInput').style.color = "#3F51B5"
      document.getElementById('alarmInputLabel').style.color = "#3F51B5"
      document.getElementById('alarmSwitchLabel').MaterialSwitch.on()
    } else if ((JSON.parse(this.responseText)).alarm_on_off == false) {
      document.getElementById('alarmSwitchSpan').style.color = "white"
      document.getElementById('alarmInput').style.color = "white"
      document.getElementById('alarmInputLabel').style.color = "white"
      document.getElementById('clockText').style.color = "#B3B2B2"
      document.getElementById('alarmSwitchLabel').MaterialSwitch.off()
    }

    // Update the sleep light on/off switch
    if ((JSON.parse(this.responseText)).sleep_light_on_off == true) {
      document.getElementById('sleepLightSwitchSpan').style.color = "#3F51B5"
      document.getElementById('sleepLightSwitchLabel').MaterialSwitch.on()
    } else if ((JSON.parse(this.responseText)).sleep_light_on_off == false) {
      document.getElementById('sleepLightSwitchSpan').style.color = "white"
      document.getElementById('sleepLightSwitchLabel').MaterialSwitch.off()
    }

    // Change the background of the clock while indicating snooze
    if ((JSON.parse(this.responseText)).indicate_snooze == true) {
      document.getElementById('clockCard').style.backgroundColor = "#adb9ff"
    } else if ((JSON.parse(this.responseText)).indicate_snooze == false) {
      document.getElementById('clockCard').style.backgroundColor = "white"
    }

  }
}
