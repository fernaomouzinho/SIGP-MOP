setInterval(function(){
    $.get('/notif/min/badge/',function(data) {
        document.getElementById("notifminbadge").innerHTML = data.value;
    });
    $.get('/notif/min/eval/',function(data) {
        document.getElementById("notifmineval").innerHTML = data.value;
    });
    $.get('/notif/min/cpv/',function(data) {
        document.getElementById("notifmincpv").innerHTML = data.value;
    });
    $.get('/notif/min/proc/',function(data) {
        document.getElementById("notifminproc").innerHTML = data.value;
    });
    $.get('/notif/min/inv/',function(data) {
        document.getElementById("notifmininv").innerHTML = data.value;
    });
    $.get('/notif/min/ver/',function(data) {
        document.getElementById("notifminver").innerHTML = data.value;
    });
}, 5000);