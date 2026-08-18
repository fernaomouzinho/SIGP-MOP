setInterval(function(){
    $.get('/notif/sup/badge/',function(data) {
        document.getElementById("notifsupbadge").innerHTML = data.value;
    });
    $.get('/notif/sup/inv/',function(data) {
        document.getElementById("notifsupinv").innerHTML = data.value;
    });
}, 3000);
