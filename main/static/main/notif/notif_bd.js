setInterval(function () {
    $.get('/notif/bd/badge/', function (data) {
        document.getElementById("notifbdbadge").innerHTML = data.value;
    });
    $.get('/notif/bd/eval/', function (data) {
        document.getElementById("notifbdeval").innerHTML = data.value;
    });
    $.get('/notif/bd/inv/', function (data) {
        document.getElementById("notifbdinv").innerHTML = data.value;
    });
    $.get('/notif/bd/ver/', function (data) {
        document.getElementById("notifbdver").innerHTML = data.value;
    });
}, 3000);
