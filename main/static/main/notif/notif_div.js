setInterval(function () {
    $.get('/notif/div/badge/', function (data) {
        document.getElementById("notifdivbadge").innerHTML = data.value;
    });

    $.get('/notif/div/proj/', function (data) {
        document.getElementById("notifdivpp").innerHTML = data.value;
    });

    $.get('/notif/div/cpv/', function (data) {
        document.getElementById("notifdivcpv").innerHTML = data.value;
    });

    $.get('/notif/div/eval/', function (data) {
        document.getElementById("notifdiveval").innerHTML = data.value;
    });

}, 5000);
