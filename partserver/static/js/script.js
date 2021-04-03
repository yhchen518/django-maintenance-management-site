function startTime() {
    var today = new Date();
    var month = today.getMonth() + 1;
    var day = today.getDate();
    var year = today.getFullYear();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    month = checkTime(month);
    day = checkTime(day);
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('datetime').innerHTML =
    month + "/" + day + "/" + year + " " + h + ":" + m + ":" + s;
    var t = setTimeout(startTime, 500);
}
function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}