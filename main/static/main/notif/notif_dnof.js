setInterval(function(){
    $.get('/notif/dnof/badge/',function(data) {
        document.getElementById("notifdnofbadge").innerHTML = data.value;
    });
    $.get('/notif/dnof/cpvreq/',function(data) {
        document.getElementById("notifdnofcpvreq").innerHTML = data.value;
    });
    $.get('/notif/dnof/cpv/',function(data) {
        document.getElementById("notifdnofcpv").innerHTML = data.value;
    });
    $.get('/notif/dnof/inv/',function(data) {
        document.getElementById("notifdnofinv").innerHTML = data.value;
    });
}, 5000);
