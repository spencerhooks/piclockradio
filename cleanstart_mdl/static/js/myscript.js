
document.addEventListener("change", changeListener)
function changeListener(o) {
  console.log("Target ID of changed: " + o.target.id)
}

var theParent = document.querySelector("#clockParent")
theParent.addEventListener("click", doSomething, false)

function doSomething(e) {
    console.log("target ID of clicked: " + e.target.id)
    // console.log("type " + e.target.tagName)
    // console.log("parent " + e.target.parentElement.tagName)
    //if (e.target !== e.currentTarget && e.target.id !== "ignore") {  // currentTarget is parent; ignore SPAN to avoid double call
        //var clickedItem = e.target.id
        //var checkBoxState = document.getElementById("alarmSwitch").checked
        //console.log("clicked on " + clickedItem + "  " + checkBoxState)
        // var request = new XMLHttpRequest()
        // request.open("GET", "/" + e.target.id, true)
        // request.send()
    //}
    //e.stopPropagation()  // stop propagation up the DOM to avoid redundant onclick actions
}

function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    var amPM = "am"
    m = checkTime(m);
    s = checkTime(s);
    if (h >= 12) { amPM = "pm"} else { amPM = "am"}
    document.getElementById('clockText').innerHTML =
    h + ":" + m + amPM;
    var t = setTimeout(startTime, 500);
}
function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}
