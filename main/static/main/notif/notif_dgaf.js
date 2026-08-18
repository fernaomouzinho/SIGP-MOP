setInterval(function(){
    $.get('/notif/dgaf/badge/',function(data) {
        document.getElementById("notifdgafbadge").innerHTML = data.value;
    });
    $.get('/notif/dgaf/cpvreq/',function(data) {
        document.getElementById("notifdgafcpvreq").innerHTML = data.value;
    });
    $.get('/notif/dgaf/cpv/',function(data) {
        document.getElementById("notifdgafcpv").innerHTML = data.value;
    });
    $.get('/notif/dgaf/po/',function(data) {
        document.getElementById("notifdgafpo").innerHTML = data.value;
    });
    $.get('/notif/dgaf/proc/',function(data) {
        document.getElementById("notifdgafproc").innerHTML = data.value;
    });
    $.get('/notif/dgaf/inv/',function(data) {
        document.getElementById("notifdgafinv").innerHTML = data.value;
    });
}, 5000);

