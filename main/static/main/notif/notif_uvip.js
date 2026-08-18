setInterval(function () {
    $.get('/notif/uvip/badge/', function (data) {
        document.getElementById("notifuvipbadge").innerHTML = data.value;
    });
    $.get('/notif/uvip/eval/', function (data) {
        document.getElementById("notifuvipeval").innerHTML = data.value;
    });
    $.get('/notif/uvip/inv/', function (data) {
        document.getElementById("notifuvipinv").innerHTML = data.value;
    });
    $.get('/notif/uvip/ver/', function (data) {
        document.getElementById("notifuvipver").innerHTML = data.value;
    });
    $.get('/notif/uvip/insp/', function (data) {
        document.getElementById("notifuvipinsp").innerHTML = data.value;
    });
}, 3000);
