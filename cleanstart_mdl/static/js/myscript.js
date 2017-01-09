
document.addEventListener("change", changeListener)
function changeListener(o) {
  console.log("Target ID of changed: " + o.target.id)
  console.log(o.target.value)
  console.log(o.target.checked)
  if (o.target.id === "volumeSlider") {
    var request = new XMLHttpRequest()
    request.open("GET", "/change_volume/" + o.target.value)
    request.send()
  }
  if (o.target.id === "alarmSwitch") {
    if (o.target.checked) {
      document.getElementById('alarmSwitchSpan').style.color = "indigo"
    } else {
      document.getElementById('alarmSwitchSpan').style.color = "white"
    }
    var request = new XMLHttpRequest()
    request.open("GET", "/alarm_on_off/" + o.target.checked)
    request.send()
  }
  if (o.target.id === "sleepLightSwitch") {
    if (o.target.checked) {
      document.getElementById('sleepLightSwitchSpan').style.color = "indigo"
    } else {
      document.getElementById('sleepLightSwitchSpan').style.color = "white"
    }
    var request = new XMLHttpRequest()
    request.open("GET", "/sleep_light_on_off/" + o.target.checked)
    request.send()
  }
}

var noiseButtonElement = document.querySelector("#noiseButton")
noiseButtonElement.addEventListener("click", makeNoise)
function makeNoise(e) {
  console.log("make some noise")
  var request = new XMLHttpRequest()
  request.open("GET", "/play_pause")
  request.send()
}

// var theParent = document.querySelector("#clockParent")
// theParent.addEventListener("click", clickListener, false)
//
// function clickListener(e) {
//     console.log("target ID of clicked: " + e.target.id)
//     console.log("type " + e.target.tagName)
//     console.log("parent " + e.target.parentElement.tagName)
//     if (e.target !== e.currentTarget && e.target.id !== "ignore") {  // currentTarget is parent; ignore SPAN to avoid double call
//         var clickedItem = e.target.id
//         var checkBoxState = document.getElementById("alarmSwitch").checked
//         console.log("clicked on " + clickedItem + "  " + checkBoxState)
//         var request = new XMLHttpRequest()
//         request.open("GET", "/" + e.target.id, true)
//         request.send()
//     }
//     e.stopPropagation()  // stop propagation up the DOM to avoid redundant onclick actions
// }

function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    var amPM = "am"
    m = checkTime(m);
    s = checkTime(s);
    if (h >= 12) {
      amPM = "pm"
      if (h > 12) {
        h = h - 12
      }
    } else {
      amPM = "am"
    }
    document.getElementById('clockText').innerHTML =
    h + ":" + m + amPM;
    var t = setTimeout(startTime, 500);
}
function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}
