setInterval(function () {
    $.get('/notif/eng/badge/', function (data) {
        document.getElementById("notifengbadge").innerHTML = data.value;
    });
    $.get('/notif/eng/ver/', function (data) {
        document.getElementById("notifengver").innerHTML = data.value;
    });
    $.get('/notif/eng/insp/', function (data) {
        document.getElementById("notifenginsp").innerHTML = data.value;
    });
}, 5000);
