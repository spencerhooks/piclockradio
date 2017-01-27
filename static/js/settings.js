
// Setup a listener for change events to switches and sliders and send to server
document.addEventListener("change", changeListener)
function changeListener(o) {
  console.log("Target ID of changed: " + o.target.id)
  console.log(o.target.value)
  console.log(o.target.checked)

  // Handle alarm time setting
  if (o.target.id === "alarmTimeSettingInput") {
    myRequest(updateClock, "/alarm_time_set/" + o.target.value)
  }

  // Handle alarm duration setting
  if (o.target.id === "alarmDurationSettingInput") {
    myRequest(updateClock, "/alarm_duration_set/" + o.target.value)
  }

  // Handle weekday auto alarm-on time setting
  if (o.target.id === "alarmResetTimeSettingInput") {
    myRequest(updateClock, "/alarm_reset_time_set/" + o.target.value)
  }

  // Handle alarm on/off switch
  if (o.target.id === "alarmAutoSetSwitch") {
    myRequest(updateClock, "/alarm_auto_set/" + o.target.checked)
  }

  // Handle sleep light duration
  if (o.target.id === "sleepTimeSettingInput") {
    myRequest(updateClock, "/sleep_time_set/" + o.target.value)
  }

  // Handle snooze duration
  if (o.target.id === "snoozeDurationSettingInput") {
    myRequest(updateClock, "/snooze_duration_set/" + o.target.value)
  }

  // Coffee pot on/off switch
  if (o.target.id === "coffeePotSwitch") {
    myRequest(updateClock, "/coffee_pot_set/" + o.target.checked)
  }

  // Sunrise on/off switch
  if (o.target.id === "sunriseSwitch") {
    myRequest(updateClock, "/sunrise_set/" + o.target.checked)
  }

}

// Load the settings from the data file and update html
function start() {
  myRequest(updateClock, "/get_time")
}

// Function to send requests to the server
function myRequest(callBackFunction, requestedURL) {
  var myrequest = new XMLHttpRequest()
  myrequest.onreadystatechange = callBackFunction
  myrequest.open("GET", requestedURL)
  myrequest.send()
}

// Update all of UI elements with the data returned from the server. All variables are updated on every callback
function updateClock () {
  if (this.readyState == 4 && this.status == 200) {

    // Initialize the alarm set time input
    document.getElementById('alarmTimeSettingInput').value = (JSON.parse(this.responseText)).alarm_time

    // Initialize the alarm duration input
    document.getElementById('alarmDurationSettingInput').value = (JSON.parse(this.responseText)).alarm_duration

    // Initialize the weekday auto alarm-on time input (time when the alarm is switched back on each day)
    document.getElementById('alarmResetTimeSettingInput').value = (JSON.parse(this.responseText)).alarm_reset_time

    // Initialize the weekday auto alarm-on time on/off switch
    if ((JSON.parse(this.responseText)).alarm_auto_reset == true) {
      document.getElementById('alarmAutoSetSwitchSpan').style.color = "#3F51B5"
      document.getElementById('alarmAutoSetSwitchLabel').MaterialSwitch.on()
    } else if ((JSON.parse(this.responseText)).alarm_auto_reset == false) {
      document.getElementById('alarmAutoSetSwitchSpan').style.color = "#B3B2B2"
      document.getElementById('alarmAutoSetSwitchLabel').MaterialSwitch.off()
    }

    // Initialize the sleep light duration input
    document.getElementById('sleepTimeSettingInput').value = (JSON.parse(this.responseText)).sleep_light_duration

    // Initialize the snooze duration input
    document.getElementById('snoozeDurationSettingInput').value = (JSON.parse(this.responseText)).snooze_duration

    // Initialize the coffee pot input
    if ((JSON.parse(this.responseText)).coffee_pot == true) {
      document.getElementById('coffeePotSwitchSpan').style.color = "#3F51B5"
      document.getElementById('coffeePotSwitchLabel').MaterialSwitch.on()
    } else if ((JSON.parse(this.responseText)).coffee_pot == false) {
      document.getElementById('coffeePotSwitchSpan').style.color = "#B3B2B2"
      document.getElementById('coffeePotSwitchLabel').MaterialSwitch.off()
    }



    // Initialize the sunrise input
    if ((JSON.parse(this.responseText)).sunrise == true) {
      document.getElementById('sunriseSwitchSpan').style.color = "#3F51B5"
      document.getElementById('sunriseSwitchLabel').MaterialSwitch.on()
    } else if ((JSON.parse(this.responseText)).sunrise == false) {
      document.getElementById('sunriseSwitchSpan').style.color = "#B3B2B2"
      document.getElementById('sunriseSwitchLabel').MaterialSwitch.off()
    }

  }
}
