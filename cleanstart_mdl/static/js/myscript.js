
var theParent = document.querySelector("#clockParent")
theParent.addEventListener("click", doSomething, false)

function doSomething(e) {
    console.log("target ID " + e.target.id)
    console.log("type " + e.target.tagName)
    console.log("parent " + e.target.parentElement.tagName)
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
