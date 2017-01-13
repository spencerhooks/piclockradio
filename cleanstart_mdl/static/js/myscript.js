
// Setup a listener for change events to switches and sliders and send to server
document.addEventListener("change", changeListener)
function changeListener(o) {
  // console.log("Target ID of changed: " + o.target.id)
  // console.log(o.target.value)
  // console.log(o.target.checked)

  // Handle volume slider
  if (o.target.id === "volumeSlider") {
    myRequest(updateClock, "/change_volume/" + o.target.value)
  }

  // Handle alarm on/off switch
  if (o.target.id === "alarmSwitch") {
    myRequest(updateClock, "/alarm_on_off/" + o.target.checked)
  }

  // Handle sleep light switch (turns on light for 30 minutes and then fades off)
  if (o.target.id === "sleepLightSwitch") {
    myRequest(updateClock, "/sleep_light_on_off/" + o.target.checked)
  }
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
  console.log("mute")
  myRequest(updateClock, "/mute")
}

// Loop for the clock to get the time every second
function startTime() {
  myRequest(updateClock, "/get_time")
  var t = setTimeout(startTime, 1000)
}

// General purpose function to send requests to the server
function myRequest(callBackFunction, requestedURL) {
  var myrequest = new XMLHttpRequest()
  myrequest.onreadystatechange = callBackFunction
  myrequest.open("GET", requestedURL)
  myrequest.send()
}

// Update all of UI elements with the data returned from the server. All variables are updated on every callback
function updateClock () {
  if (this.readyState == 4 && this.status == 200) {
    // Update clock time
    document.getElementById('clockText').innerHTML = (JSON.parse(this.responseText)).time

    // Update the noise generator button state
    if ((JSON.parse(this.responseText)).generating_noise == true) {
      document.getElementById('noiseImage').src = $SCRIPT_ROOT + "/static/images/waveform_color.png"
    } else if ((JSON.parse(this.responseText)).generating_noise == false) {
      document.getElementById('noiseImage').src = $SCRIPT_ROOT + "/static/images/waveform.png"
    }

    // Update the volume slider. **There's a bug when dragging the slider, need to fix this**
    if ((JSON.parse(this.responseText)).mute == true) {
      document.getElementById('volumeSlider').MaterialSlider.change(0)
      document.getElementById('muteIcon').style.color = "white"
    } else if ((JSON.parse(this.responseText)).mute == false) {
      document.getElementById('volumeSlider').MaterialSlider.change((JSON.parse(this.responseText)).volume)
      document.getElementById('muteIcon').style.color = "#3F51B5"
    }

    // Update the alarm on/off switch
    if ((JSON.parse(this.responseText)).alarm_on_off == true) {
      document.getElementById('alarmSwitchSpan').style.color = "#3F51B5"
      document.getElementById('clockText').style.color = "#3F51B5"
      document.getElementById('alarmSwitchLabel').MaterialSwitch.on()
    } else if ((JSON.parse(this.responseText)).alarm_on_off == false) {
      document.getElementById('alarmSwitchSpan').style.color = "white"
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
  }
}
