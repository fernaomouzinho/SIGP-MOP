setInterval(function () {
    $.get('/notif/sec/badge/', function (data) {
        document.getElementById("notifsecbadge").innerHTML = data.value;
    });
    $.get('/notif/sec/ver/', function (data) {
        document.getElementById("notifsecver").innerHTML = data.value;
    });
    $.get('/notif/sec/insp/', function (data) {
        document.getElementById("notifsecinsp").innerHTML = data.value;
    });
}, 3000);
