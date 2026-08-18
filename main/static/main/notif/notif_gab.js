setInterval(function(){
    $.get('/notif/gab/badge/',function(data) {
        document.getElementById("notifgabbadge").innerHTML = data.value;
    });
    $.get('/notif/gab/cpv/',function(data) {
        document.getElementById("notifgabcpv").innerHTML = data.value;
    });
    $.get('/notif/gab/eval/',function(data) {
        document.getElementById("notifgabeval").innerHTML = data.value;
    });
    $.get('/notif/gab/proc/',function(data) {
        document.getElementById("notifgabproc").innerHTML = data.value;
    });
    $.get('/notif/gab/inv/',function(data) {
        document.getElementById("notifgabinv").innerHTML = data.value;
    });
}, 5000);