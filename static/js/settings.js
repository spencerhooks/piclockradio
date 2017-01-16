
// Setup a listener for change events to switches and sliders and send to server
document.addEventListener("change", changeListener)
function changeListener(o) {
  console.log("Target ID of changed: " + o.target.id)
  console.log(o.target.value)
  console.log(o.target.checked)

  // Handle volume slider
  // if (o.target.id === "volumeSlider") {
  //   myRequest(updateClock, "/change_volume/" + o.target.value)
  // }

}

// Load the settings from the data file and update html
function start() {
  myRequest(updateClock, "/get_time")
  // console.log("Starting up")
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

    // Update the alarm set time indicator
    document.getElementById('alarmTimeSettingInput').value = (JSON.parse(this.responseText)).alarm_time

  }
}
